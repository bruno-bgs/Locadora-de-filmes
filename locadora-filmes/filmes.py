from clientes import clientes
from datetime import datetime, timedelta

alugueis = []

filmes = [
    {"id": 1, "nome": "Matrix", "disponivel": True},
    {"id": 2, "nome": "Interestelar", "disponivel": True},
    {"id": 3, "nome": "Batman", "disponivel": True},
    {"id": 4, "nome": "Super-Homem", "disponivel": True},
    {"id": 5, "nome": "As Branquelas", "disponivel": True},
    {"id": 6, "nome": "Avatar", "disponivel": True}
]

# Essa função percorre a lista de filmes cadastrados e exibe as informações de cada um.
def listar_filmes():
    for filme in filmes:
        status = "Disponivel" if filme["disponivel"] else "Alugado"
        print(f'ID:{filme["id"]} | {filme["nome"]} | {status}')

# Essa função permite que um cliente alugue um filme disponível.
def alugar_filme():

    # Verifica se existem clientes cadastrados
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    
    # Mostra a lista de clientes
    print("\nClientes:")
    for cliente in clientes:
        print(f'{cliente["id"]} | {cliente["nome"]}')

    # Usuário escolhe o cliente 
    cliente_id = int(input("Escolha o ID do cliente: "))

    # Busca o cliente selecionado
    cliente_escolhido = None
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            cliente_escolhido = cliente
    
    # Validação do cliente
    if cliente_escolhido is None:
        print("Cliente não encontrado.")
        return
    
    # Mostra os filmes disponíveis
    print("\nFilmes Disponiveis")
    for filme in filmes:
        print(f'{filme["id"]} | {filme["nome"]}')

    filme_id = int(input("Escolha o ID do filme: "))

    # Busca o filme escolhido
    filme_escolhido = None
    for filme in filmes:
        if filme["id"] == filme_id and filme["disponivel"]:
            filme_escolhido = filme

    # Validação do filme
    if filme_escolhido is None:
        print("Filme não encontrado.")
        return
    
    hoje = datetime.now()

    data_devolucao = hoje + timedelta(days=3)

    # Evitar devolução no domingo
    if data_devolucao.weekday() == 6:
        data_devolucao = data_devolucao + timedelta(days=1)

    # Cria o registro do aluguel
    aluguel = {
            "cliente": cliente_escolhido["nome"],
            "filme": filme_escolhido["nome"],
            "data_aluguel": hoje,
            "data_devolucao": data_devolucao
        }

    alugueis.append(aluguel)

    filme_escolhido["disponivel"] = False

    print("\nFilme alugado com sucesso")
    print(f'Devolver até: {data_devolucao.strftime("%d/%m/%Y")}')
