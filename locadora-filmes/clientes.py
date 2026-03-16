clientes = []

def cadastrar_cliente():
    nome = input("Nome do Cliente\n")
    telefone = input("Telefone do Cliente\n")
    email = input("Email do Cliente\n")

    cliente = {
        "id": len(clientes) + 1,
        "nome": nome,
        "telefone": telefone,
        "email": email
    }

    clientes.append(cliente)
    print("Cliente cadastrado com sucesso")

def listar_clientes():
        if not clientes:
            print("Cliente não cadastrado")
            return
        
        for cliente in clientes:
            print(f'ID: {cliente["id"]} | Nome: {cliente["nome"]}')