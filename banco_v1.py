menu = '''
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

-> '''

saldo = 0
limite_diario = 500
extrato = ''
numero_saques = 0
LIMITE_SAQUES = 3

def deposito(dinheiro: float):
    global saldo, extrato
    if dinheiro > 0:
        saldo += dinheiro
        extrato += f'\nDepósito: R${dinheiro:.2f}'
        return saldo, extrato
    else:
        print('Informe um valor válido para depósito.')

def saque(dinheiro: float):
    global saldo, numero_saques, extrato, LIMITE_SAQUES
    
    if numero_saques != LIMITE_SAQUES:
        if dinheiro > 0 and dinheiro <= saldo:
            if dinheiro <= limite_diario:
                saldo -= dinheiro
                numero_saques += 1
                extrato += f'\nSaque: R${dinheiro:.2f}'
                return saldo, numero_saques, extrato
            else:
                print('Você informou um valor acima do seu limite de saque.')
        else:
            print('Você informou um valor inválido ou acima do seu saldo atual.')
    else:
        print('Você atingiu o limite máximo de saque diário.')

def verifica_extrato():
    global extrato, saldo
    return print(f'EXTRATO:\n{'Nenhuma operação realizada' if not extrato else extrato}\nSaldo da conta: R${saldo:.2f}')

while True:

    opcao = int(input(menu))

    if opcao == 0:
        break

    elif opcao == 1:
        depositar = float(input('Informe o valor que deseja depositar: '))
        deposito(depositar)

    elif opcao == 2:
        sacar = float(input('Informe o valor que deseja sacar: '))
        saque(sacar)

    elif opcao == 3:
        verifica_extrato()

    else:
        print('Operação inválida, informe novamente a operação desejada.')