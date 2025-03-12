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
            Titular:\t{self.cliente.nome}
        """

class Cliente:
    def __init__(self, endereco: str):
        self.__endereco = endereco
        self.__contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: Conta):
        self.__contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf: str, nome: str, data_nascimento):
        super().__init__(endereco)
        self.__cpf = cpf
        self.__nome = nome
        self.__data_nascimento = data_nascimento