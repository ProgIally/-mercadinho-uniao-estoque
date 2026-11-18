import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import listar_produtos, cadastrar_produto, movimentar_estoque
from models import listar_alertas, excluir_produto
from dotenv import load_dotenv
from database import criar_tabelas

load_dotenv()
app = Flask(__name__)   
app.secret_key = os.environ["SECRET_KEY"]
criar_tabelas()


@app.route("/")
def inicio():
    produtos = listar_produtos()

    return render_template(
        "estoque.html",
        produtos=produtos
    )


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        try:
            nome = request.form["nome"].strip()
            quantidade = int(request.form["quantidade"])
            estoque_minimo = int(request.form["estoque_minimo"])

            cadastrar_produto(nome, quantidade, estoque_minimo)

            flash("Produto cadastrado com sucesso!", "sucesso")
            return redirect(url_for("inicio"))

        except (ValueError, KeyError) as erro:
            flash(f"Erro ao cadastrar produto: {erro}", "erro")

    return render_template("cadastro.html")


@app.route("/movimentacao", methods=["GET", "POST"])
def movimentacao():
    if request.method == "POST":
        try:
            produto_id = int(request.form["produto_id"])
            tipo = request.form["tipo"]
            quantidade = int(request.form["quantidade"])

            movimentar_estoque(produto_id, tipo, quantidade)

            flash("Movimentação realizada com sucesso!", "sucesso")
            return redirect(url_for("inicio"))

        except (ValueError, KeyError) as erro:
            flash(f"Erro na movimentação: {erro}", "erro")

    produtos = listar_produtos()

    return render_template(
        "movimentacao.html",
        produtos=produtos
    )

@app.route("/alertas")
def alertas():
    produtos = listar_alertas()

    return render_template(
        "alertas.html",
        produtos=produtos
    )

@app.route("/excluir/<int:produto_id>", methods=["POST"])
def excluir(produto_id):
    try:
        excluir_produto(produto_id)
        flash("Produto excluído com sucesso!", "sucesso")

    except ValueError as erro:
        flash(f"Erro ao excluir produto: {erro}", "erro")

    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)
