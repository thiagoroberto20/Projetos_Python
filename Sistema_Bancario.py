print("\n**********************************************")
print("***********SISTEMA BANCARIO v1****************")
print("**********************************************")

menu = '''

    [d] Depositar
    [s] Sacar 
    [e] Extrato
    [q] Sair

=>'''

saldo = 0   # Armazena o saldo inicial da conta, inicialmente definido como 0.
limite = 500 # Define o limite máximo de saque, fixado em 500.
extrato = '' # Uma string vazia que armazenará o histórico das transações
numero_saques = 0 #  Controla o número de saques realizados, inicializado em 0.
LIMITE_SAQUES = 3 # Define o limite máximo de saques permitidos por período, definido como 3.

while True:  # Loop principal do programa, na qual repete indefinidamente até que o usuário escolha a opção "sair".

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do déposito: "))

        if valor > 0: # Valida se o valor do depósito é positivo.
            saldo += valor  # Se válido, atualiza o saldo e adiciona a transação ao extrato.
            extrato += f"Déposito: R${valor:.2f}\n" #

        else:
            print("Déposito falhou! O valor informado é inválido.") # Se inválido, exibe uma mensagem de erro.

    elif opcao == "s":
        valor = float(input("Infome o valor do saque: "))
        
        excedeu_saldo = valor > saldo #Valida se o valor do saque é positivo, não excede o saldo, o limite e o número máximo de saques.
        
        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n" #Se todas as validações forem bem-sucedidas, atualiza o saldo, adiciona a transação ao extrato e incrementa o contador de saques.
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")   # Se qualquer validação falhar, exibe a mensagem de erro correspondente.

    elif opcao == "e" : #Exibe o extrato das transações e o saldo atual da conta.
        print("\n***************** EXTRATO *****************")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("*******************************************")

    elif opcao == "q": #Encerra o loop e finaliza o programa.
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.") #Se a opção digitada não for nenhuma das válidas, exibe uma mensagem de erro e solicita que o usuário tente novamente.

