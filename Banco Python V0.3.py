from abc import ABC,abstractclassmethod, abstractproperty

class Conta:
    def __init__(self, numero, usuario):
        self._numero = numero
        self._usuario = usuario
        self._saldo = 0
        self._agencia = "0001"
        self._historico = Historico()

    def sacar(self, valor):
        saldo = self._saldo

        Saldo_Insuficiente = saldo < valor
        Valor_Baixo = valor < 1
        Tudo_Certo = valor <= saldo

        if Saldo_Insuficiente:
            print("="*100)
            print(f"Sua operação falhou, pois seu saldo é de somente R${saldo}.")
            return False

        elif Valor_Baixo:
            print("="*100)
            print(f"O limite minimo de cada Saque é de R$1")
            return False
        
        elif Tudo_Certo:
            self._saldo -= valor
            
            print("="*100)
            print(f"Saque de R${valor} feito com sucesso")
            return True
        
        else:
            print("="*100)
            print(f"Sua operaçâo falhou, o valor inserido é invalido.")
            return False

    def depositar(self, valor):

        Valor_Baixo = valor <= 0
        Tudo_Certo = valor > 0

        if Valor_Baixo: 
            print("="*100) 
            print(f"O limite minimo de cada Deposito é de R$1")
            return False
        elif Tudo_Certo:
            self._saldo += valor
            print("="*100)
            print (f"Deposito feito com sucesso no valor de R$ {valor}!")
            return True
        else:
            print("="*100)
            print(f"Sua operaçâo falhou, o valor inserido é invalido.")
            return False

    @classmethod
    def nova_conta(cls, usuario, numero):
        return cls(numero, usuario)
    @property
    def numero(self):
        return self._numero
    @property
    def usuario(self):
        return self._usuario
    @property
    def saldo(self):
        return self._saldo
    @property
    def agencia(self):
        return self._agencia
    @property
    def historico(self):
        return self._historico

class ContaCorrente(Conta):
    def __init__(self, numero, usuario, limite=500, limite_saques=3):
        super().__init__(numero, usuario)
        self._limite = limite
        self._limite_saques = limite_saques
        
    def sacar(self, valor):
        valor = int(valor)
        numero_de_saques = len([transacao for transacao in self.historico.transacoes() if transacao["Tipo"] == 'Saque'])
        numero_de_operações_feitas = len(self.historico.transacoes())

        muitos_saques= numero_de_saques >= 3
        muitas_operaçoes = numero_de_operações_feitas >= 10
        limite_do_valor = valor > self._limite

        if muitos_saques:
            print("="*100)
            print(f"A quantidade maxima de saques por dia foi alcançada que é de 3 saques.")
            return False
        elif muitas_operaçoes:
            print("="*100)
            print(f"Sua operaçâo falhou, pois o limite de operações que podem ser feitas por dia foi alcançado.")
            return False
        elif limite_do_valor:
            print("="*100)
            print(f"O limete maximo do valor de cada Saque é de 500")
            return False
        else:
            return super().sacar(valor)

    def depositar(self, valor):
        numero_de_operações_feitas = len(self.historico.transacoes())

        muitas_operaçoes = numero_de_operações_feitas >= 10

        if muitas_operaçoes:
            print("="*100)
            print(f"Sua operaçâo falhou, pois o limite de operações que podem ser feitas por dia foi alcançado.")
            return False
        else:
            return super().depositar(valor)
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.usuario.nome}
        """
        
class Historico:
    def __init__(self):
        self._transacoes = []
    
    def adicionar_transacao(self, tipo):
        self._transacoes.append({"Tipo": tipo.__class__.__name__, "Valor": tipo.valor})
    
    def transacoes(self):
        return self._transacoes

class Tipo(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Tipo):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Tipo):
    def __init__(self,Valor):
        self._valor = Valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Usuario:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    def realizar_transacao(self, tipo, valor):
        if tipo == "Saque":
            saque = Saque(valor)
            saque.registrar(self.contas[0])
        elif tipo == "Deposito":
            deposito = Deposito(valor)
            deposito.registrar(self.contas[0])
        else:
            print("="*100)
            print("Tipo de transação inválido.")

       
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Usuario):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf  

def recuperar_conta_cliente(usuario):
    if not usuario.contas:
        print("="*100)
        print("Cliente não possui conta!")
        return
    return usuario.contas[0]

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def filtrar_conta(pessoa):
    if not pessoa.contas:
        return   
    return pessoa.contas[0]

def sacar(usuarios):
    print("="*100)
    cpf = input("Informe o CPF do cliente: ")
    pessoa = filtrar_usuario(cpf, usuarios)
    if not pessoa:
        print("="*100)
        print("Conta não encontrada.")
        return
    else:
        conta_corrente1 = filtrar_conta(pessoa)
        if not conta_corrente1:
            print("="*100)
            print("Usuario não possui conta!")
            return
        else:
            print("="*100)
            valor = float(input("Informe o valor do saque: "))
            sucesso = conta_corrente1.sacar(valor)
            if sucesso :
                conta_corrente1.historico.adicionar_transacao(Saque(valor))
                return

def depositar(usuarios):
    print("="*100)
    cpf = input("Informe o CPF do cliente: ")
    pessoa = filtrar_usuario(cpf, usuarios)
    if not pessoa:
        print("="*100)
        print("Usuario não encontrada.")
        return
    else:
        conta_corrente1 = filtrar_conta(pessoa)
        if not conta_corrente1:
            print("="*100)
            print("Usuario não possui conta!")
            return
        else:
            print("="*100)
            valor = float(input("Informe o valor do deposito: "))
            sucesso = conta_corrente1.depositar(valor)
            if sucesso:
                conta_corrente1.historico.adicionar_transacao(Deposito(valor))
                return

def Extrato(usuarios):
    print("="*100)
    cpf = input("Informe o CPF do cliente: ")
    pessoa = filtrar_usuario(cpf, usuarios)
    if pessoa:
        conta_corrente1 = recuperar_conta_cliente(usuario = pessoa)
        if conta_corrente1 :
            print("="*100)
            for transacao in conta_corrente1.historico.transacoes():
                print(f"\n{transacao['Tipo']}:\n\t\t\t\t\tR$ {transacao['Valor']:.2f}")
            print(f"Saldo:\t\t\t\tR$ {conta_corrente1.saldo:.2f}")
            print(f"Operações feitas:\t\t{len(conta_corrente1.historico.transacoes())}/10")
        else:   
            print("="*100)
            print("Usuario não possui conta!")
            return
    else:
        print("="*100)
        print("Usuario não encontrado.")

def criar_usuario(usuarios):
    print("="*100)
    cpf = input("Digite seu CPF: ")
    if filtrar_usuario(cpf, usuarios):
        print("="*100)
        print("Já existe um usuario com este CPF.")
    else:
        print("="*100)
        nome = input("Digite seu nome: ")
        print("="*100)
        data_nascimento = input("Digite sua data de nascimento: ")
        print("="*100)
        endereco = input("Digite seu endereço: ")
        print("="*100)
        usuario = PessoaFisica(nome, data_nascimento, cpf, endereco)
        usuarios.append(usuario)
        print("Usuário criado com sucesso!")

def criar_conta(numero_conta, usuarios, contas):
    print("="*100)
    cpf = input("Digite o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("="*100)
        print("Esse usuario não existe.")
        return
    else:
        conta = ContaCorrente.nova_conta(usuario=usuario, numero=numero_conta)
        contas.append(conta)
        usuario.contas.append(conta)
        print("="*100)
        print("Conta criada com sucesso!")

def listar_usuarios(usuarios):
    if not usuarios:
        print("="*100)
        print("Não existem usuários cadastrados.")
    else:
        print("="*100)
        for usuario in usuarios:
            print(f"Nome: {usuario.nome}\n")
        print("="*100)

def listar_contas(contas):
    if not contas:
        print("="*100)
        print("Não existem contas cadastradas.")
    else:
        print("="*100)
        for conta in contas:
            print(f"Cliente: {conta.usuario.nome}")
        print("="*100)

def Banco():
    contas = []
    usuarios = []
    while True:
        opcao = int(input("""================================================MENU================================================
Insira que tipo de operação você deseja fazer: 
[1] Sacar 
[2] Depositar
[3] Extrato 
[4] Criar Usuario 
[5] Criar Conta
[6] Listar usuarios
[7] Listar contas                    
[8] Sair 
 => """))
        if opcao == 1:
           sacar(usuarios)
           
        elif opcao == 2:
           depositar(usuarios)

        elif opcao == 3:
            Extrato(usuarios)
         
        elif opcao == 4:
            criar_usuario(usuarios)
        elif opcao == 5:
           numero_conta = len(contas) + 1
           criar_conta(numero_conta, usuarios, contas)
        elif opcao == 6:
            listar_usuarios(usuarios)
            
        elif opcao == 7:
            listar_contas(contas)
        elif opcao == 8:
            print("="*100)
            print("Saindo do sistema...")
            break
        else:
            print("="*100)
            print("Opção inválida. Tente novamente.")
            
Banco()