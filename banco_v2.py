from datetime import datetime

def menu():
    menu = f'{' MENU '.center(30, '-')}\n[1] Depositar\n[2] Sacar\n[3] Extrato\n[4] Criar usuário\n[5] Criar Conta Corrente\n[6] Listar contas\n[0] Sair\n-> '
    return int(input(menu))

def deposito(saldo: float, valor: float, extrato: str, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R${valor:.2f} | Data: {datetime.now().strftime('%d/%m/%Y')} | Hora: {datetime.now().strftime('%H:%M')}\n'
        print('\n\033[92mDepósito realizado com sucesso.\033[0m\n')
    else:
        print('\n\033[91mInforme um valor válido para depósito.\033[0m\n')

    return saldo, extrato

def saque(*, saldo: float, valor: float, extrato: str, limite_diario: int, numero_saques: int, limite_saques: int):
    if numero_saques != limite_saques:
        if valor > 0 and valor <= saldo:
            if valor <= limite_diario:
                saldo -= valor
                numero_saques += 1
                extrato += f'Saque: R${valor:.2f} | Data: {datetime.now().strftime('%d/%m/%Y')} | Hora: {datetime.now().strftime('%H:%M')}\n'
                print('\n\033[92mSaque realizado com sucesso.\033[0m\n')
            else:
                print('\n\033[91mVocê informou um valor acima do seu limite de saque.\033[0m\n')
        else:
            print('\n\033[91mVocê informou um valor inválido ou acima do seu saldo atual.\033[0m\n')
    else:
        print('\n\033[91mVocê atingiu o limite máximo de saque diário.\033[0m\n')

    return saldo, numero_saques, extrato

def verifica_extrato(saldo: float,/,*,extrato: str):
    return print(f'EXTRATO:\n\n{'Nenhuma operação realizada' if not extrato else extrato}\nSaldo da conta: R${saldo:.2f}\n')

def criar_usuario(usuarios: list):
    cpf = input('Informe seu CPF (apenas números): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n\033[91mEsse CPF já está cadastrado em um usuário!\033[0m\n')
        return
    
    nome = input('Informe seu nome: ')
    data_nascimento = input('Informe sua data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe seu endereço (logradouro, n° - bairro - cidade/sigla estado): ')

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print('\n\033[92mUsuário cadastrado com sucesso!\033[0m\n')

# NOTE: Verifica se já existe algum usuário com o CPF informado
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta_corrente(agencia, contas: list, usuarios: list):
    cpf = input('Informe seu CPF (apenas números): ')
    usuario = filtrar_usuario(cpf, usuarios)
    numero_da_conta = len(contas) + 1

    if usuario:
        contas.append({"agencia": agencia, "numero_da_conta": numero_da_conta, "usuario": usuario})
        print(f'\n\033[92mConta Corrente criada com sucesso para {usuario["nome"]}.\033[0m\n')
    else:
        print('\n\033[91mUsuário não encontrado.\033[0m\n')

def listar_contas(contas):
    if len(contas) != 0:
        for conta in contas:
            print(f'Agência: {conta["agencia"]}\nNúmero da conta: {conta["numero_da_conta"]}\nTitular: {conta["usuario"]["nome"]}\n')
    else:
        print('\n\033[91mAinda não tem nenhuma conta cadastrada no sistema.\033[0m\n')

def main():
    saldo = 0
    limite_diario = 500
    extrato = ''
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = '0001'
    usuario = []
    contas = []

    while True:

        opcao = menu()

        if opcao == 0:
            break

        elif opcao == 1:
            depositar = float(input('Informe o valor que deseja depositar: '))
            saldo, extrato = deposito(saldo, depositar, extrato)

        elif opcao == 2:
            sacar = float(input('Informe o valor que deseja sacar: '))
            saldo, numero_saques, extrato = saque(saldo=saldo, valor=sacar, extrato=extrato, limite_diario=limite_diario, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

        elif opcao == 3:
            verifica_extrato(saldo, extrato=extrato)

        elif opcao == 4:
            criar_usuario(usuario)

        elif opcao == 5:
            criar_conta_corrente(AGENCIA, contas, usuario)

        elif opcao == 6:
            listar_contas(contas)

        else:
            print('\033[91mOperação inválida, informe novamente a operação desejada.\033[0m')

main()