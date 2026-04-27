from conexao import conectar
from flask import Flask, jsonify, request


class clientes():
    def buscar_clientes():
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT id, nome, telefone, email FROM clientes ORDER BY id")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()


    def cadastrar_cliente(nome, telefone, email):
        
        if not nome or not telefone or not email:
            return jsonify("Preencha nome, telefone e email."), 400
            

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)",
                (nome, telefone, email),
            )
            conn.commit()
            return jsonify("Cliente cadastrado com sucesso no banco."), 201
        except Exception as erro:
            conn.rollback()
            return jsonify(f"Erro ao cadastrar cliente: {erro}"), 500
        finally:
            cursor.close()
            conn.close()


