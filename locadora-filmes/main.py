from clientes import cadastrar_cliente, listar_clientes
from filmes import listar_filmes
from filmes import alugar_filme

def menu():
    print("\nLocadora de Filmes")
    print("1 - Cadastrar Clientes")
    print("2 - Listar Clientes")
    print("3 - Ver filmes")
    print("4 - Alugar filme")
    print("0 - Sair")

while True:

        menu()
        opcao = input("Escolha uma opção: ")

        match opcao: 
             case "1": 
                cadastrar_cliente()
             case "2":
                listar_clientes()
             case "3":
                listar_filmes()
             case "4":
                alugar_filme()
             case "0":
                print("Encerrando o sistema...")
                break

             case _:
                print("Opção inválida.")
                
    