
import pytest
from models import cadastrar_produto

def test_nome_produto_vazio():
    with pytest.raises(ValueError, match="O nome do produto é obrigatório"):
        cadastrar_produto("", 10, 5)

def test_quantidade_negativa():
    with pytest.raises(ValueError, match="As quantidades não podem ser negativas"):
        cadastrar_produto("Arroz", -5, 2)

def test_estoque_minimo_negativo():
    with pytest.raises(ValueError, match="As quantidades não podem ser negativas"):
        cadastrar_produto("Feijão", 10, -2)

def test_quantidade_invalida():
    with pytest.raises(ValueError, match="As quantidades devem ser números inteiros"):
        cadastrar_produto("Macarrão", "dez", 5)

import sqlite3
import database
import models


def test_cadastrar_produto_no_banco(tmp_path, monkeypatch):
    # Cria um banco temporário para o teste
    banco_teste = tmp_path / "estoque_teste.db"

    # Substitui o caminho do banco original
    monkeypatch.setattr(database, "DATABASE", banco_teste)

    # Cria as tabelas no banco temporário
    database.criar_tabelas()

    # Substitui a função de conexão usada pelo models
    monkeypatch.setattr(models, "conectar", database.conectar)

    # Cadastra um produto
    produto_id = models.cadastrar_produto("Arroz 5kg", 20, 5)

    # Consulta o produto cadastrado
    with database.conectar() as conexao:
        produto = conexao.execute(
            "SELECT * FROM produto WHERE id = ?",
            (produto_id,)
        ).fetchone()

    # Verifica se os dados foram salvos corretamente
    assert produto is not None
    assert produto["nome"] == "Arroz 5kg"
    assert produto["quantidade"] == 20
    assert produto["estoque_minimo"] == 5
def test_nome_produto_none():
    with pytest.raises(ValueError, match="O nome do produto é obrigatório"):
        cadastrar_produto(None, 10, 5)


def test_nome_produto_numerico():
    with pytest.raises(ValueError, match="O nome do produto é obrigatório"):
        cadastrar_produto(123, 10, 5)