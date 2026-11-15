
import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "estoque.db"


def conectar():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    with conectar() as conexao:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS produto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0
                    CHECK (quantidade >= 0),
                estoque_minimo INTEGER NOT NULL DEFAULT 0
                    CHECK (estoque_minimo >= 0)
            );

            CREATE TABLE IF NOT EXISTS movimentacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL
                    CHECK (tipo IN ('entrada', 'saida')),
                quantidade INTEGER NOT NULL
                    CHECK (quantidade > 0),
                data TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id)
                    REFERENCES produto(id)
            );
        """)


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados criado com sucesso!")
