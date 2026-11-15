
import pytest
import database
import models


@pytest.fixture
def produto_teste(tmp_path, monkeypatch):
    # Cria um banco temporário
    banco_teste = tmp_path / "estoque_teste.db"
    monkeypatch.setattr(database, "DATABASE", banco_teste)

    # Cria as tabelas
    database.criar_tabelas()

    # Conecta o models ao banco temporário
    monkeypatch.setattr(models, "conectar", database.conectar)

    # Cadastra um produto com 20 unidades
    return models.cadastrar_produto("Arroz 5kg", 20, 5)


def test_entrada_estoque(produto_teste):
    models.movimentar_estoque(produto_teste, "entrada", 10)

    produto = models.buscar_produto(produto_teste)

    assert produto["quantidade"] == 30


def test_saida_estoque(produto_teste):
    models.movimentar_estoque(produto_teste, "saida", 5)

    produto = models.buscar_produto(produto_teste)

    assert produto["quantidade"] == 15


def test_saida_estoque_insuficiente(produto_teste):
    with pytest.raises(ValueError, match="Estoque insuficiente"):
        models.movimentar_estoque(produto_teste, "saida", 50)

    produto = models.buscar_produto(produto_teste)

    assert produto["quantidade"] == 20


def test_registro_movimentacao(produto_teste):
    models.movimentar_estoque(produto_teste, "entrada", 10)

    with database.conectar() as conexao:
        registro = conexao.execute(
            "SELECT * FROM movimentacao WHERE produto_id = ?",
            (produto_teste,)
        ).fetchone()

    assert registro is not None
    assert registro["tipo"] == "entrada"
    assert registro["quantidade"] == 10

def test_alerta_estoque_minimo(produto_teste):
    # Produto começa com 20 unidades e mínimo de 5
    models.movimentar_estoque(produto_teste, "saida", 15)

    alertas = models.listar_alertas()

    assert len(alertas) == 1
    assert alertas[0]["id"] == produto_teste
    assert alertas[0]["quantidade"] == 5


def test_alerta_estoque_abaixo_minimo(produto_teste):
    # Reduz o estoque de 20 para 3 unidades
    models.movimentar_estoque(produto_teste, "saida", 17)

    alertas = models.listar_alertas()

    assert len(alertas) == 1
    assert alertas[0]["quantidade"] == 3


def test_sem_alerta_estoque_normal(produto_teste):
    # Produto possui 20 unidades e mínimo de 5
    alertas = models.listar_alertas()

    assert len(alertas) == 0
