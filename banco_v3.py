from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta: "Conta"):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self.__valor = valor

    @property
    def valor(self):
        return self.__valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.__valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor: float):
        self.__valor = valor
    
    @property
    def valor(self):
        return self.__valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.__valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self.__transacoes = []

    @property
    def transacoes(self):
        return self.__transacoes

    def adicionar_transacao(self, transacao: Transacao):
        self.__transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        })

class Conta:
    def __init__(self, numero: int, cliente):
        self.__saldo = 0
        self.__numero = numero
        self.__agencia = '0001'
        self.__cliente = cliente
        self.__historico = Historico()

    @property
    def saldo(self):
        return self.__saldo

    @property
    def numero(self):
        return self.__numero
    
    @property
    def agencia(self):
        return self.__agencia

    @property
    def cliente(self):
        return self.__cliente
    
    @property
    def historico(self):
        return self.__historico

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero, cliente)
    
    def sacar(self, valor: float):
        if valor > self.__saldo:
            print('Você não tem saldo suficiente!')

        elif valor > 0:
            self.__saldo -= valor
            print('Saque realizado com sucesso!')
            return True
        
        else:
            print('O valor informado é inválido!')

        return False

    def depositar(self, valor: float):
        if valor > 0:
            self.__saldo += valor
            print('Depósito realizado com sucesso!')
        else:
            print('O valor informado é inválido!')
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.__limite = limite
        self.__limite_saques = limite_saques

    def sacar(self, valor):
        # NOTE: Armazena o tamanho da lista das operações do tipo saque
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        
        if valor > self.__limite:
            print('O valor do saque excedeu o limite!')

        elif numero_saques >= self.__limite_saques:
            print('Número máximo de saques excedido!')

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            Conta Corrente:\t{self.numero}
            Titular:\t{self.cliente.get_nome}
        """

class Cliente:
    def __init__(self, endereco: str):
        self.__endereco = endereco
        self.__contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self.__contas.append(conta)

    @property
    def get_contas(self):
        return self.__contas

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf: str, nome: str, data_nascimento):
        super().__init__(endereco)
        self.__cpf = cpf
        self.__nome = nome
        self.__data_nascimento = data_nascimento

    @property
    def get_cpf(self):
        return self.__cpf
    
    @property
    def get_nome(self):
        return self.__nome

def menu():
    menu = f'{' MENU '.center(30, '-')}\n[1] Depositar\n[2] Sacar\n[3] Extrato\n[4] Criar usuário\n[5] Criar Conta Corrente\n[6] Listar contas\n[0] Sair\n-> '
    return int(input(menu))

def deposito(clientes):
    cpf = input('Informe o CPF do cliente (Apenas números): ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nCliente não encontrado!')
        return
    
    valor = float(input('Informe o valor de depósito: R$'))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def saque(clientes):
    cpf = input('Informe o CPF do cliente (Apenas números): ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nCliente não encontrado!')
        return
    
    valor = float(input('Informe o valor do saque: R$'))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def verifica_extrato(clientes):
    cpf = input('Informe o CPF do cliente (Apenas números): ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nCliente não encontrado!')
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print(' EXTRATO '.center(30, '='))
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = 'Não foram realizadas transações.'
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}'

    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
    print('='*30)

def criar_cliente(clientes):
    cpf = input('Informe o CPF do cliente (Apenas números): ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('\nJá existe um cliente com esse CPF!')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (logradouro, n° - bairro - cidade/sigla estado): ')

    cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
    print(cliente)

    clientes.append(cliente)
    print('\nCliente criado com sucesso!')

# NOTE: Verifica se já existe algum cliente com o CPF informado
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.get_cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.get_contas:
        print('\nEsse cliente não possui conta!')
        return
    
    # FIXME: Não permite cliente escolher a conta
    return cliente.get_contas[0]

def criar_conta_corrente(numero_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente (Apenas números): ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('\nCliente não encontrado, fluxo de criação de conta encerrado!')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print('\nConta criada com sucesso!')

def listar_contas(contas):
    for conta in contas:
        print('='*100)
        print(str(conta))

def main():
    clientes = []
    contas = []

    while True:

        opcao = menu()

        if opcao == 0:
            break

        elif opcao == 1:
            deposito(clientes)

        elif opcao == 2:
            saque(clientes)

        elif opcao == 3:
            verifica_extrato(clientes)

        elif opcao == 4:
            criar_cliente(clientes)

        elif opcao == 5:
            numero_conta = len(contas) + 1
            criar_conta_corrente(numero_conta, clientes, contas)

        elif opcao == 6:
            listar_contas(contas)

        else:
            print('\033[91mOperação inválida, informe novamente a operação desejada.\033[0m')

main()