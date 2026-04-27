from datetime import datetime, timedelta
from flask import jsonify
from clientes import clientes
from conexao import conectar


class filmes():
    def buscar_filmes(somente_disponiveis=False):
        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            query = "SELECT id, titulo, genero, ano, disponivel FROM filmes"
            if somente_disponiveis:
                query += " WHERE disponivel = TRUE"
            query += " ORDER BY id"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def cadastrar_filme(titulo, genero, ano):
        if not titulo or not genero or not ano:
            return jsonify({"erro": "Título, gênero e ano são obrigatórios"}), 400

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO filmes (titulo, genero, ano, disponivel) VALUES (%s, %s, %s, %s)",
                (titulo, genero, ano, True),
            )
            conn.commit()
            return jsonify({"mensagem": "Filme cadastrado com sucesso no banco."}), 201
        except Exception as erro:
            conn.rollback()
            return jsonify({"erro": f"Erro ao cadastrar filme: {erro}"}), 500
        finally:
            cursor.close()
            conn.close()


    def alugar_filme(cliente_id, filme_id):
        if not cliente_id or not filme_id:
            return jsonify({"erro": "cliente_id e filme_id são obrigatórios"}), 400

        try:
            dados_clientes = clientes.buscar_clientes()
        except Exception as erro:
            return jsonify({"erro": f"Erro ao buscar clientes: {erro}"}), 500

        cliente_escolhido = next((cliente for cliente in dados_clientes if cliente["id"] == cliente_id), None)
        if cliente_escolhido is None:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        try:
            dados_filmes = filmes.buscar_filmes(somente_disponiveis=True)
        except Exception as erro:
            return jsonify({"erro": f"Erro ao buscar filmes: {erro}"}), 500

        filme_escolhido = next((filme for filme in dados_filmes if filme["id"] == filme_id), None)
        if filme_escolhido is None:
            return jsonify({"erro": "Filme não encontrado ou indisponível"}), 404

        hoje = datetime.now()
        data_devolucao = hoje + timedelta(days=3)

        if data_devolucao.weekday() == 6:
            data_devolucao += timedelta(days=1)

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO alugueis (cliente_id, filme_id, data_aluguel, data_devolucao, devolvido)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (cliente_id, filme_id, hoje, data_devolucao, False),
            )
            cursor.execute(
                "UPDATE filmes SET disponivel = %s WHERE id = %s",
                (False, filme_id),
            )
            conn.commit()
            return jsonify(
                {
                    "mensagem": "Filme alugado com sucesso.",
                    "data_devolucao": data_devolucao.strftime("%d/%m/%Y"),
                }
            ), 201
        except Exception as erro:
            conn.rollback()
            return jsonify({"erro": f"Erro ao registrar aluguel: {erro}"}), 500
        finally:
            cursor.close()
            conn.close()

    def devolver_filme(aluguel_id):
        if not aluguel_id:
            return jsonify({"erro": "aluguel_id é obrigatório"}), 400

        conn = conectar()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    a.id,
                    a.filme_id,
                    a.devolvido,
                    c.nome AS cliente,
                    f.titulo AS filme
                FROM alugueis a
                JOIN clientes c ON a.cliente_id = c.id
                JOIN filmes f ON a.filme_id = f.id
                WHERE a.id = %s
                """,
                (aluguel_id,),
            )
            aluguel = cursor.fetchone()

            if not aluguel:
                return jsonify({"erro": "Aluguel não encontrado"}), 404

            if aluguel["devolvido"]:
                return jsonify({"erro": "Esse aluguel já foi devolvido"}), 400

            cursor.execute(
                "UPDATE alugueis SET devolvido = %s WHERE id = %s",
                (True, aluguel_id),
            )
            cursor.execute(
                "UPDATE filmes SET disponivel = %s WHERE id = %s",
                (True, aluguel["filme_id"]),
            )
            conn.commit()
            return jsonify(
                {
                    "mensagem": "Filme devolvido com sucesso.",
                    "cliente": aluguel["cliente"],
                    "filme": aluguel["filme"],
                }
            ), 200
        except Exception as erro:
            conn.rollback()
            return jsonify({"erro": f"Erro ao registrar devolução: {erro}"}), 500
        finally:
            cursor.close()
            conn.close()
