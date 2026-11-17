from database import conectar



def cadastrar_produto(nome, quantidade, estoque_minimo):
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome do produto é obrigatório.")

    nome = nome.strip()

    if len(nome) > 100:
        raise ValueError("O nome do produto não pode ultrapassar 100 caracteres.")

    if type(quantidade) is not int or type(estoque_minimo) is not int:
        raise ValueError("As quantidades devem ser números inteiros.")

    if quantidade < 0 or estoque_minimo < 0:
        raise ValueError("As quantidades não podem ser negativas.")

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO produto (nome, quantidade, estoque_minimo)
            VALUES (?, ?, ?)
            """,
            (nome, quantidade, estoque_minimo)
        )
        return cursor.lastrowid

def listar_produtos():
    with conectar() as conexao:
        produtos = conexao.execute(
            "SELECT * FROM produto ORDER BY nome"
        ).fetchall()

        return [dict(produto) for produto in produtos]


def buscar_produto(produto_id):
    with conectar() as conexao:
        produto = conexao.execute(
            "SELECT * FROM produto WHERE id = ?",
            (produto_id,)
        ).fetchone()

        return dict(produto) if produto else None


def movimentar_estoque(produto_id, tipo, quantidade):
    if tipo not in ("entrada", "saida"):
        raise ValueError("Tipo de movimentação inválido.")

    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError("A quantidade deve ser um inteiro positivo.")

    with conectar() as conexao:
        produto = conexao.execute(
            "SELECT quantidade FROM produto WHERE id = ?",
            (produto_id,)
        ).fetchone()

        if produto is None:
            raise ValueError("Produto não encontrado.")

        if tipo == "entrada":
            nova_quantidade = produto["quantidade"] + quantidade
        else:
            nova_quantidade = produto["quantidade"] - quantidade

            if nova_quantidade < 0:
                raise ValueError("Estoque insuficiente para esta saída.")

        conexao.execute(
            "UPDATE produto SET quantidade = ? WHERE id = ?",
            (nova_quantidade, produto_id)
        )

        conexao.execute(
            """
            INSERT INTO movimentacao
            (produto_id, tipo, quantidade)
            VALUES (?, ?, ?)
            """,
            (produto_id, tipo, quantidade)
        )

        return nova_quantidade


def listar_alertas():
    with conectar() as conexao:
        produtos = conexao.execute(
            """
            SELECT * FROM produto
            WHERE quantidade <= estoque_minimo
            ORDER BY nome
            """
        ).fetchall()

        return [dict(produto) for produto in produtos]
