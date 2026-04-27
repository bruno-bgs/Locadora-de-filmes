from conexao import conectar

conn = conectar()
cursor = conn.cursor()

print("Funcionando!")

conn.close()

# Inserir Cliente
nome = input("Digite o nome do cliente:")
email = input("Digite o email:")

cursor.execute(
    "INSERT INTO clientes (nome, email) VALUES (%s, %s)",
    (nome, email)
)

# Inserir filme
titulo = input("Digite o título do filme: ")
genero = input("Digite o gênero: ")
ano = int(input("Digite o ano: "))

cursor.execute(
    "INSERT INTO filmes (titulo, genero, ano) VALUES (%s, %s, %s)",
    (titulo, genero, ano)
)

conn.commit()

print("Dados inseridos com sucesso!")

conn.close()