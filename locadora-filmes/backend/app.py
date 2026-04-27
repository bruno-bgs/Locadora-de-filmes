from flask import Flask, jsonify, request
from conexao import conectar
from datetime import datetime, timedelta
from clientes import clientes

app = Flask(__name__)


@app.after_request
def adicionar_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/")
def home():
    return jsonify({"mensagem": "API da locadora funcionando"})


@app.route("/filmes", methods=["GET"])
def listar_filmes_api():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, titulo, genero, ano, disponivel FROM filmes")
        filmes = cursor.fetchall()
        return jsonify(filmes)
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/clientes", methods=["GET"])
def listar_clientes_api():
    return jsonify(clientes.buscar_clientes())


@app.route("/filmes", methods=["POST"])
def cadastrar_filme_api():
    dados = request.get_json()

    titulo = dados.get("titulo")
    genero = dados.get("genero")
    ano = dados.get("ano")

    if not titulo or not genero or not ano:
        return jsonify({"erro": "Título, gênero e ano são obrigatórios"}), 400

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO filmes (titulo, genero, ano, disponivel) VALUES (%s, %s, %s, %s)",
            (titulo, genero, ano, True)
        )
        conn.commit()
        return jsonify({"mensagem": "Filme cadastrado com sucesso"}), 201
    except Exception as erro:
        conn.rollback()
        return jsonify({"erro": str(erro)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/clientes", methods=["POST"])
def cadastrar_cliente_api():
    dados = request.get_json()

    nome = dados.get("nome")
    telefone = dados.get("telefone")
    email = dados.get("email")
    return clientes.cadastrar_cliente(nome, telefone, email)


@app.route("/alugueis", methods=["POST"])
def alugar_filme_api():
    dados = request.get_json()

    cliente_id = dados.get("cliente_id")
    filme_id = dados.get("filme_id")

    if not cliente_id or not filme_id:
        return jsonify({"erro": "cliente_id e filme_id são obrigatórios"}), 400

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
        cliente = cursor.fetchone()

        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        cursor.execute("SELECT * FROM filmes WHERE id = %s", (filme_id,))
        filme = cursor.fetchone()

        if not filme:
            return jsonify({"erro": "Filme não encontrado"}), 404

        if not filme["disponivel"]:
            return jsonify({"erro": "Filme indisponível"}), 400

        hoje = datetime.now()
        data_devolucao = hoje + timedelta(days=3)

        if data_devolucao.weekday() == 6:
            data_devolucao += timedelta(days=1)

        cursor.execute(
            """
            INSERT INTO alugueis (cliente_id, filme_id, data_aluguel, data_devolucao, devolvido)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (cliente_id, filme_id, hoje, data_devolucao, False)
        )

        cursor.execute(
            "UPDATE filmes SET disponivel = %s WHERE id = %s",
            (False, filme_id)
        )

        conn.commit()

        return jsonify({
            "mensagem": "Filme alugado com sucesso",
            "data_devolucao": data_devolucao.strftime("%d/%m/%Y")
        }), 201

    except Exception as erro:
        conn.rollback()
        return jsonify({"erro": str(erro)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/alugueis", methods=["GET"])
def listar_alugueis_api():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                a.id,
                c.nome AS cliente,
                f.titulo AS filme,
                a.data_aluguel,
                a.data_devolucao,
                a.devolvido
            FROM alugueis a
            JOIN clientes c ON a.cliente_id = c.id
            JOIN filmes f ON a.filme_id = f.id
            ORDER BY a.id
        """)
        alugueis = cursor.fetchall()
        return jsonify(alugueis)
    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/devolucoes", methods=["POST"])
def devolver_filme_api():
    dados = request.get_json()
    aluguel_id = dados.get("aluguel_id")

    if not aluguel_id:
        return jsonify({"erro": "aluguel_id é obrigatório"}), 400

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, filme_id, devolvido
            FROM alugueis
            WHERE id = %s
            """,
            (aluguel_id,)
        )
        aluguel = cursor.fetchone()

        if not aluguel:
            return jsonify({"erro": "Aluguel não encontrado"}), 404

        if aluguel["devolvido"]:
            return jsonify({"erro": "Esse aluguel já foi devolvido"}), 400

        cursor.execute(
            "UPDATE alugueis SET devolvido = %s WHERE id = %s",
            (True, aluguel_id)
        )

        cursor.execute(
            "UPDATE filmes SET disponivel = %s WHERE id = %s",
            (True, aluguel["filme_id"])
        )

        conn.commit()
        return jsonify({"mensagem": "Filme devolvido com sucesso"}), 200

    except Exception as erro:
        conn.rollback()
        return jsonify({"erro": str(erro)}), 500
    finally:
        cursor.close()
        conn.close()



if __name__ == "__main__":
    app.run(debug=True)
