import textwrap


def menu():
    menu = """\n
    print("**********************************************")
    print("***********SISTEMA BANCARIO v2****************")
    print("**********************************************")

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


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Déposito: R${valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo #Valida se o valor do saque é positivo, não excede o saldo, o limite e o número máximo de saques.
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n" #Se todas as validações forem bem-sucedidas, atualiza o saldo, adiciona a transação ao extrato e incrementa o contador de saques.
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Digite o CPF (SOMENTE NÚMERO): ")
    usuario = filtrar_usuario(cpf, usuarios) # realizar a validação do usuario, pra vê se não existi

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return
    
    nome = input("Digite o nome completo: ")
    data_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuario (SOMENTE NÚMERO): ")
    usuario = filtrar_usuario(cpf,usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return{"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100) 
        print(textwrap.dedent(linha))

        
def main():
    LIMITE_SAQUES = 3 # Define o limite máximo de saques permitidos por período, definido como 3.
    AGENCIA = "0001"
    saldo = 0   # Armazena o saldo inicial da conta, inicialmente definido como 0.
    limite = 500 # Define o limite máximo de saque, fixado em 500.
    extrato = '' # Uma string vazia que armazenará o histórico das transações
    numero_saques = 0 #  Controla o número de saques realizados, inicializado em 0.
    usuarios = []
    contas = []

    while True:  # Loop principal do programa, na qual repete indefinidamente até que o usuário escolha a opção "sair".
        opcao = menu()

        if opcao == "d":
            valor = float(input("Digite o valor do déposito: "))
            saldo, extrato = depositar(saldo, valor, extrato) # chamando a função def depositar
        
        elif opcao == "s":
            valor = float(input("Digite o valor do saque: "))
            saldo, extrato = sacar (
                saldo= saldo,
                valor= valor,
                extrato = extrato, 
                limite= limite, 
                numero_saques= numero_saques, 
                limite_saques= LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()