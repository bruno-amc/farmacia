# importação do módulo para usar datas nos descontos e cadastro de clientes
from datetime import datetime

# importação do PANDAS para salvar as listas em arquivos CSV
import pandas as pd

# Criação das classes e dos respectivos construtores __init__

class Medicamento:
    def __init__(self, nome, principal_composto, laboratorio, descricao, preco, tipo_medicamento, necessita_receita=False):
        """
        Construtor da classe de Medicamentos.

        :param nome: Str >> Nome do medicamento.
        :param principal_composto: Str >> Composto do medicamento.
        :param laboratorio: Str >> Laboratório fabricante do medicamento.
        :param descricao: Str >> Descrição do medicamento.
        :param preco: Float >> Valor do medicamento.
        :param necessita_receita: Boolean >> Verificar a necessidade ou não de receita.
        """
        self.nome = nome
        self.principal_composto = principal_composto
        self.laboratorio = laboratorio
        self.descricao = descricao
        self.preco = preco
        self.tipo_medicamento = tipo_medicamento
        self.necessita_receita = necessita_receita

class Cliente:
    def __init__(self, cpf, nome, data_nascimento):
        """
        Construtor da classe Cliente.

        :param cpf: Str >> CPF do cliente.
        :param nome: Str >> Nome do cliente.
        :param data_nascimento: Date dd/mm/aaaa >> Data de nascimento do cliente.
        """
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = self.converter_data(data_nascimento)

    def converter_data(self, data_str):
        """
        Realizar a conversão de string em date
        :param data_str: Valor recebido em string para a data.
        :return: Data do tipo date.
        """
        try:
            data = datetime.strptime(data_str, '%d/%m/%Y') # strptime da biblioteca datetime
            return data.date()  # Converte para um objeto de data
        except ValueError:
            print("Formato de data inválido. Use o formato 'dd/mm/aaaa'.")
            return None # valor para conversão falha

class Laboratorio:
    def __init__(self, nome, endereco, telefone, cidade, estado):
        """
        Construtor da classe laboratório.

        :param nome: Str >> Nome do laboratório.
        :param endereco: Str >> Endereço do laboratório.
        :param telefone: Str >> Telefone do laboratório.
        :param cidade: Str >> Cidade do laboratório.
        :param estado: Str >> Cidade do laboratório
        """
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.cidade = cidade
        self.estado = estado

class Venda: # init inicia os atributos e o valor total soma os produtos vendidos pela expressão geradora produto.preco
    def __init__(self, data_hora, produtos, cliente):
        """
        Construtor da classe Venda. Inicializa atributos e a variável `valor_total` que soma
        os produtos vendidos pela expressão geradora `produto.preco`.

        :param data_hora: Data e hora da venda.
        :param produtos: Produtos envolvidos na venda.
        :param cliente: Cliente da transação.
        """
        self.data_hora = data_hora
        self.produtos = produtos
        self.cliente = cliente
        self.valor_total = sum(produto.preco for produto in produtos) # Soma o preço de todos os produtos

# Inicializando listas vazias que irão receber as operações da farmácia.

# Lista de clientes cadastrados.
clientes = []

# Lista de medicamentos cadastrados.
medicamentos = []

# Lista de laboratórios cadastrados.
laboratorios = []

# Lista das vendas realizadas.
vendas = []

# Lista dos medicamentos controlados.
medicamentos_controlados = []

def cadastrar_cliente():
    """
    Realizar o cadastro de clientes.
    Recebe inputs de CPF, Nome, Data de nascimento, que são os parâmetros da classe Clientes.
    """
    cpf = input("CPF do cliente: ")
    nome = input("Nome do cliente: ")
    data_nascimento = input("Data de nascimento do cliente: ")
    cliente = Cliente(cpf, nome, data_nascimento)
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")


def cadastrar_laboratorio():
    """
    Realizar o cadastro de laboratórios.
    Recebe inputs de Nome, Endereço, Telefone, Cidade e Estado que são os parâmetros da classe Laboratório.
    """
    nomelab = input("Nome do laboratório: ")
    enderecolab = input("Endereço do Laboratório: ")
    telefonelab = input("Telefone  do Laboratório: ")
    cidadelab = input("Cidade do Laboratório: ")
    estadolab = input("Estado do Laboratório: ")
    lab = Laboratorio(nomelab, enderecolab, telefonelab, cidadelab, estadolab)
    laboratorios.append(lab)
    print("Laboratório cadastrado com sucesso!")


def cadastrar_medicamento():
    """
    Realizar o cadastro de medicamentos.
    Input de Strings com o nome do medicamento, composto, laboratório fabricante,
    descrição, tipo do medicamento (fito ou quimioterápico).
    Input float: preço do medicamento.
    Possui condicional para avaliar a necessidade de receita em quimioterápicos.
    """
    nome = input("Nome do medicamento: ")
    principal_composto = input("Principal composto: ")
    laboratorio = input("Nome do laboratorio: ")
    descricao = input("Descricao: ")
    tipo_medicamento = input("Tipo do medicamento (quimioterápico/fitoterápico): ").lower()
    preco = float(input("Preco (incluir casas decimais): "))  # Captura o preço como um número decimal

    if tipo_medicamento == 'quimioterápico':
        necessita_receita = input("Necessita receita? (S/N): ").lower() == 's' # caso seja 's' o código abaixo será executado
        medicamento = Medicamento(nome, principal_composto, laboratorio, descricao, preco, tipo_medicamento, necessita_receita)
    elif tipo_medicamento == 'fitoterápico':
        medicamento = Medicamento(nome, principal_composto, laboratorio, descricao, preco, tipo_medicamento)
    else:
        print("Tipo de medicamento inválido.")
        return

    medicamentos.append(medicamento)
    print("Medicamento cadastrado com sucesso!")

#realiza a venda usando o CPF do cliente para localizá-lo no cadastro
def realizar_venda():
    """
    Realizar venda através da identificação do cliente pelo CPF (Str).
    """
    cpf_cliente = input("CPF do cliente: ")
    cliente = None
    for c in clientes: # c como variável temporária
        if c.cpf == cpf_cliente:
            cliente = c
            break
    
    if cliente is None:
        print("Cliente não encontrado.")
        return
    
    data_nascimento_cliente = cliente.data_nascimento
    idade_cliente = (datetime.now().date() - data_nascimento_cliente).days // 365  # Calcula a idade do cliente

    produtos = []
    medicamentos_controlados = []  # Zerei a lista de medicamentos controlados para cada venda
    valor_total = 0  # Inicializo o valor_total como zero
    while True:
        nome_produto = input("Nome do produto (ou 'sair' para finalizar): ")
        if nome_produto.lower() == 'sair':
            break

        produto_encontrado = None
        for m in medicamentos:
            if m.nome == nome_produto:
                produto_encontrado = m
                break
        
        if produto_encontrado is None:
            print("Produto não encontrado.")
            continue

        produtos.append(produto_encontrado)
        valor_total += produto_encontrado.preco  # Adiciona o preço do produto ao valor_total
    
        # Verifica se o produto necessita de receita médica
        if produto_encontrado.necessita_receita:
            medicamentos_controlados.append(produto_encontrado)

    # Verifica se há medicamentos controlados na venda e emite alerta
    if medicamentos_controlados:
        print("Alerta: Verifique a receita para o seguinte medicamento controlado:")
        for medicamento in medicamentos_controlados:
            print(f"Nome: {medicamento.nome}")
    
    # Aplicação dos descontos
    if idade_cliente > 65:
        valor_total *= 0.8  # Desconto de 20% para clientes acima de 65 anos
    
    if valor_total > 150:
        valor_total *= 0.9  # Desconto de 10% para compras acima de 150 reais
    
    venda = Venda(data_hora=datetime.now(), produtos=produtos, cliente=cliente)
    venda.valor_total = valor_total  # Atualiza o valor total com os descontos aplicados
    vendas.append(venda)
    
    desconto_str = ""
    if idade_cliente > 65:
        desconto_str += "20% de desconto para clientes acima de 65 anos, "
    if valor_total > 150:
        desconto_str += "10% de desconto para compras acima de R$150, "
    
    print(f"Venda realizada com sucesso!\nDescontos aplicados: {desconto_str}\nValor Total: R${venda.valor_total:.2f}")

def emitir_relatorios():
    """
    Emissão de relatórios com as opções: 1. Clientes, 2.Todos os medicamentos, 3.Quimioterápicos,
    4. Fitoterápicos e 5. Dados de vendas no dia.

    """
    print("1. Listagem de clientes por ordem alfabética")
    print("2. Listagem de medicamentos por ordem alfabética")
    print("3. Listagem de medicamentos quimioterápicos")
    print("4. Listagem de medicamentos fitoterápicos")
    print("5. Estatísticas dos atendimentos realizados no dia")
    print("6. Listagem dos laboratórios cadastrados")
    
    opcao = int(input("Escolha uma opção: "))
    
    if opcao == 1:
        listar_clientes_ordenados()
    elif opcao == 2:
        listar_medicamentos_ordenados()
    elif opcao == 3:
        listar_medicamentos_quimioterapicos()
    elif opcao == 4:
        listar_medicamentos_fitoterapicos()
    elif opcao == 5:
        exibir_estatisticas_atendimentos()
    elif opcao == 6:
        exibir_laboratorios_cadastrados()
    else:
        print("Opção inválida!")


def listar_clientes_ordenados():
    """
    Realizar a ordenação da lista dos nomes dos clientes em ordem alfabética.
    """
    clientes_ordenados = sorted(clientes, key=lambda c: c.nome)  #função lambda para retornar os nomes dos clientes e ordenar com o sorted.
    for cliente in clientes_ordenados:
        print(f"CPF: {cliente.cpf}\nNome: {cliente.nome}\nData de Nascimento: {cliente.data_nascimento}\n")

def exibir_laboratorios_cadastrados():
    """
    Realizar a listagem dos laboratórios cadastrados.
    """
    labs_ordenados = sorted(laboratorios, key=lambda c: c.nome)  #função lambda para retornar os nomes dos laboratórios e ordenar com o sorted
    for lab in labs_ordenados:
        print(f"Nome do Laboratório: {lab.nome}\n")


def listar_medicamentos_ordenados():
    """
    Realizar a ordenação da lista dos nomes dos remédios em ordem alfabética.
    Gera a informação contendo o nome do medicamento, composto, laboratório e descrição.
    """
    medicamentos_ordenados = sorted(medicamentos, key=lambda m: m.nome)
    for medicamento in medicamentos_ordenados:
        print(f"Nome: {medicamento.nome}\nPrincipal Composto: {medicamento.principal_composto}\nLaboratório: {medicamento.laboratorio}\nDescrição: {medicamento.descricao}\n")

def listar_medicamentos_quimioterapicos():
    """
    Gerar a lista dos remédios quimioterápicos.
    Gera a informação contendo o nome do medicamento, composto, laboratório, descrição, se necessita de receita e preço.
    """
    for medicamento in medicamentos:
        if medicamento.tipo_medicamento == 'quimioterápico':
            print(f"Nome: {medicamento.nome}\nPrincipal Composto: {medicamento.principal_composto}\nLaboratório: {medicamento.laboratorio}\nDescrição: {medicamento.descricao}\nNecessita Receita: {medicamento.necessita_receita}\nPreço: R${medicamento.preco:.2f}\n")

def listar_medicamentos_fitoterapicos():
    """
    Gerar a lista do remédios fitoterápicos.
    Gera a informação contendo o nome do medicamento, composto, laboratório, descrição e preço.
    """
    for medicamento in medicamentos:
        if medicamento.tipo_medicamento == 'fitoterápico':
            print(f"Nome: {medicamento.nome}\nPrincipal Composto: {medicamento.principal_composto}\nLaboratório: {medicamento.laboratorio}\nDescrição: {medicamento.descricao}\nPreço: R${medicamento.preco:.2f}\n")

def exibir_estatisticas_atendimentos():
    """
    Realizar o processamento para gerar as estatisticas dos atentimentos.
    Try: Caso existam vendas. Except: Caso não existam vendas.
    """
    try:
        total_vendas = len(vendas) #qtd de vendas
        total_clientes_atendidos = len(set(venda.cliente for venda in vendas)) #set para qtd de clientes únicos (remove duplicatas)
        
        medicamentos_vendidos = {}
        total_receita_dia = 0
        
        for venda in vendas:
            for produto in venda.produtos:
                if produto.nome not in medicamentos_vendidos:
                    medicamentos_vendidos[produto.nome] = {"quantidade": 1, "valor_total": produto.preco}
                else:
                    medicamentos_vendidos[produto.nome]["quantidade"] += 1
                    medicamentos_vendidos[produto.nome]["valor_total"] += produto.preco
                total_receita_dia += produto.preco
        
        if medicamentos_vendidos:  # Verifica se há medicamentos vendidos
            medicamento_mais_vendido = max(medicamentos_vendidos, key=lambda m: medicamentos_vendidos[m]["quantidade"]) # retorna medicamentos m mais vendido
            print(f"Remédio mais vendido: {medicamento_mais_vendido}")
        else:
            print("Nenhum medicamento vendido.")
        
        print(f"Quantidade de pessoas atendidas: {total_clientes_atendidos}")
        print(f"Total de remédios quimioterápicos vendidos: {len([v for v in vendas if any(isinstance(p, Medicamento) and p.necessita_receita for p in v.produtos)])}")
        print(f"Total de remédios fitoterápicos vendidos: {len([v for v in vendas if any(isinstance(p, Medicamento) and not p.necessita_receita for p in v.produtos)])}")
        print(f"Total de vendas realizadas: {total_vendas}")
        print(f"Total de receita no dia: R${total_receita_dia:.2f}")
    except ValueError:
        print("Nenhuma venda realizada!")

def main():
    while True:
        print("1. Cadastrar cliente")
        print("2. Cadastrar medicamento")
        print("3. Realizar venda")
        print("4. Emitir relatorios")
        print("5. Cadastrar laboratórios")
        print("6. Sair")

        opcao = int(input("Escolha uma opcao: "))
        
        if opcao == 1:
            cadastrar_cliente()
        elif opcao == 2:
            cadastrar_medicamento()
        elif opcao == 3:
            realizar_venda()
        elif opcao == 4:
            emitir_relatorios()
        elif opcao == 5:
            cadastrar_laboratorio()
        elif opcao == 6:
            break
        else:
            print("Opcao invalida!")

if __name__ == "__main__":
    main()



# Extrair os nomes dos clientes em uma lista de dicionários
#dados = [{"Nome": cliente.nome} for cliente in clientes]
dados = [{"Nome": cliente.nome, "CPF": cliente.cpf, "DATA NASCIMENTO:": cliente.data_nascimento} for cliente in clientes]

# Crie um DataFrame a partir dos dados
dados_cadastro_clientes = pd.DataFrame(dados)

# Salve o DataFrame em um arquivo CSV
dados_cadastro_clientes.to_csv("clientes.csv", index=False)