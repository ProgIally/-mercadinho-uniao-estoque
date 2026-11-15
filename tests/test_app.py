
import pytest
import database
import models
from app import app


@pytest.fixture
def cliente(tmp_path, monkeypatch):
    # Banco temporário para não alterar o estoque real
    banco_teste = tmp_path / "teste_integracao.db"

    monkeypatch.setattr(database, "DATABASE", banco_teste)
    monkeypatch.setattr(models, "conectar", database.conectar)

    database.criar_tabelas()

    app.config.update(
        TESTING=True,
        SECRET_KEY="chave-teste"
    )

    with app.test_client() as cliente:
        yield cliente


def test_pagina_estoque(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert "Consulta de Estoque" in resposta.get_data(as_text=True)


def test_pagina_cadastro(cliente):
    resposta = cliente.get("/cadastro")
    assert resposta.status_code == 200


def test_pagina_movimentacao(cliente):
    resposta = cliente.get("/movimentacao")
    assert resposta.status_code == 200


def test_pagina_alertas(cliente):
    resposta = cliente.get("/alertas")
    assert resposta.status_code == 200
    assert "Alertas de Estoque" in resposta.get_data(as_text=True)


def test_cadastrar_produto_pela_rota(cliente):
    resposta = cliente.post("/cadastro", data={
        "nome": "Macarrao 500g",
        "quantidade": "20",
        "estoque_minimo": "5"
    }, follow_redirects=True)

    assert resposta.status_code == 200

    produtos = models.listar_produtos()
    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Macarrao 500g"
    assert produtos[0]["quantidade"] == 20


def test_movimentar_produto_pela_rota(cliente):
    produto_id = models.cadastrar_produto(
        "Arroz 5kg", 20, 5
    )

    resposta = cliente.post("/movimentacao", data={
        "produto_id": str(produto_id),
        "tipo": "saida",
        "quantidade": "10"
    }, follow_redirects=True)

    assert resposta.status_code == 200

    produtos = models.listar_produtos()
    assert produtos[0]["quantidade"] == 10


def test_bloquear_saida_insuficiente(cliente):
    produto_id = models.cadastrar_produto(
        "Feijao 1kg", 5, 2
    )

    resposta = cliente.post("/movimentacao", data={
        "produto_id": str(produto_id),
        "tipo": "saida",
        "quantidade": "10"
    }, follow_redirects=True)

    assert resposta.status_code == 200

    produtos = models.listar_produtos()
    assert produtos[0]["quantidade"] == 5
