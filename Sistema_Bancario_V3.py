import textwrap 
# Importa a biblioteca textwrap usada para formatar texto multi-linha.
# É usada, por exemplo, para melhorar a apresentação do extrato bancário.
from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty
# Importa funcionalidades relacionadas à criação de classes abstratas e métodos abstratos
# Isso é usado para definir classes base (como Transação) que definem comportamentos 
# que subclasses (como Saque e Deposito) devem implementar.
from datetime import datetime
# Importa a classe datetime usada para trabalhar com datas e horas
# É usada, por exemplo, para registrar a data e hora de uma transação bancária.

import datetime



class Cliente:
    """
    Classe que representa um cliente do banco.
    
    Atributos:
        endereço(str): Endereço do cliente.
        contas (list): Lista de contas do cliente.

    """
    
    
    def __init__(self, endereco):
        """
        Construtor da classe Cliente.

        Argumentos:
            endereco(str): Endereço do cliente.
        """
        self.endereco = endereco
        self.contas = []

        
    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação na conta do cliente.

        Argumentos:
            conta (Conta): na qual a transação será realizada.
            transacao (Transação): a ser realizada.

        """
        transacao.registrar(conta)


    def adicionar_conta(self, conta):
        self.contas.append(conta)



class PessoaFisica(Cliente):
    """
    Classe que representa um cliente pessoa física.

    Atributos:
        nome (str): Nome do cliente.
        data_nascimento (str): Data de nascimento do cliente.
        cpf (str): CPF do cliente.

    """
    

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """
    Classe que representa uma conta bancária.

    Atributos:
        _saldo (float): Saldo da conta.
        _numero (str): Número da conta.
        _agencia (str): Agência da conta.
        _cliente (Cliente): Cliente dono da conta.
        _historico (Historico): Histórico de transações da conta.
    
    """


    def __init__(self, numero, cliente):
       self._saldo = 0
       self._numero = numero
       self._agencia = "0001"
       self._cliente = cliente
       self._historico = Historico()

       """
       Construtor da classe Conta.

       Argumentos:
            numero (str): Número da conta.
            cliente (Cliente): Cliente dono da conta.
       
       """ 
       
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    """
        Cria uma nova instância da classe Conta.

        Argumentos:
            cliente (Cliente): Cliente dono da conta.
            numero (str): Número da conta.

        Retorna:
            Conta: Instância da classe Conta.
    """
              

    @property
    def saldo(self):
        return self._saldo
    """
        Retorna o saldo da conta.

        Retorna:
            float: Saldo da conta.
        """
       
           
    @property
    def numero(self):
        return self._numero
    """
        Retorna o número da conta.

        Retorna:
            str: Número da conta.
    """


    @property
    def agencia(self):
        return self._agencia
    """
        Retorna a agência da conta.

        Retorna:
            str: Agência da conta.
    """


    @property
    def cliente(self):
        return self._cliente
    """
        Retorna o cliente dono da conta.

        Retorna:
            Cliente: Cliente dono da conta.
    """


    @property
    def historico(self):
           return self._historico
    """
        Retorna o histórico de transações da conta.

        Retorna:
            Historico: Histórico de transações da conta.
    """


    def sacar(self, valor):
        """
        Realiza um saque na conta.

        Argumentos:
            valor (float): Valor a ser sacado.

        Retorna:
            bool: True se o saque for bem sucedido, False caso contrário
        """ 
        saldo = self.valor
        excedeu_saldo = valor > saldo   

        if excedeu_saldo:
            print("\n@@@ Operação faljou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False


    def depositar(self, valor):
        """
        Realiza um depósito na conta.

        Argumentos:
            valor (float): Valor a ser depositado.

        Retorna:
            bool: True se o depósito for bem sucedido, False caso contrário
        """
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        

class ContaCorrente(Conta):
    """
    Classe que representa uma conta corrente.

    Atributos:
        _limite (float): Limite da conta.
        _limite_saques (int): Limite de saques por dia.
    """
    
    
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        """
        Construtor da classe ContaCorrente.

        Argumentos:
            numero (str): Número da conta.
            cliente (Cliente): Cliente dono da conta.
            limite (float): Limite da conta (opcional, padrão 500).
            limite_saques (int): Limite de saques por dia (opcional, padrão 3).
        """
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques


    def sacar(self, valor):
        """
        Realiza um saque na conta corrente.

        Argumentos:
            valor (float): Valor a ser sacado.

        Retorna:
            bool: True se o saque for bem sucedido, False caso contrário
        """
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques
        
        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False
    

    def __str__(self):
        """
        Retorna a representação em string da conta.

        Retorna:
            str: Representação em string da conta.
        """
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
        

class Historico:
    """
    Classe que representa o histórico de transações de uma conta.

    Atributos:
        _transacoes (list): Lista de transações.
    """
    def __init__(self):
        """
        Construtor da classe Historico.
        """
        self._transacoes = []

    
    @property
    def transacoes(self):
        return self._transacoes
    

    def adicionar_transacao(self, transacao):
        now = datetime.datetime.now()
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,                 
                "data": now.strftime("%d-%m-%Y %H:%M:%S"),
                
            }
        )


class Transacao(ABC):
    """
    Classe abstrata que define o comportamento básico de uma transação bancária.

    Atributos (não implementados):
        valor (float): Valor da transação (a ser definido em subclasses).
    """    

    #Métodos (abstratos):
    @property
    @abstractproperty
    def valor(self):
        """Retorna o valor da transação."""
        pass


    @abstractclassmethod
    def registrar(self, conta):
        """Registra a transação na conta bancária."""
        pass


class Saque(Transacao):
    """
    Classe que representa uma transação de saque em conta bancária.

    Atributos:
        _valor (float): Valor a ser sacado.
    """
    def __init__(self, valor):
        self._valor = valor


    @property
    def valor(self):
        """Retorna o valor do saque."""
        return self._valor
    

    def register(self, conta):
        """Registra o saque na conta bancária.

            Argumentos:
                conta (Conta): Conta na qual o saque será realizado.
        """
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """
    Classe que representa uma transação de depósito em conta bancária.

    Atributos:
        _valor (float): Valor a ser depositado.
    """
    def __init__(self, valor):
        self._valor = valor
    

    @property
    def valor(self):
        return self._valor
    

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    """
    Exibe o menu principal do sistema bancário e retorna a opção escolhida pelo usuário.
    """
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    
    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


main()


nova_conta