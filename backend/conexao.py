import mysql.connector

def conectar():
    conn = mysql.connector.connect(
    host="localhost",
    user="root",        
    password="root", # 
    database="locadora"
)
    print("Conectado com sucesso!") 
    return conn