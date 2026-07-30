"""
auth.py
--------
Funções de cadastro e login. As senhas NUNCA são guardadas em texto puro:
usamos bcrypt para transformar a senha em um "hash" (código irreversível).
"""

import re
import bcrypt
import database as db


def validar_email(email: str) -> bool:
    padrao = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return re.match(padrao, email.strip()) is not None


def gerar_hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def conferir_senha(senha_digitada: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha_digitada.encode("utf-8"), senha_hash.encode("utf-8"))


def cadastrar_usuario(nome: str, email: str, senha: str, empresa: str):
    """Cadastra um novo usuário.
    Retorna (sucesso: bool, mensagem: str, usuario: dict|None).
    O PRIMEIRO usuário cadastrado no sistema vira automaticamente 'admin'
    (assim você mesmo cria a primeira conta de administrador sem precisar
    mexer direto no banco de dados)."""

    nome = nome.strip()
    empresa = empresa.strip()

    if not nome or not email or not senha or not empresa:
        return False, "Preencha todos os campos.", None

    if not validar_email(email):
        return False, "Digite um e-mail válido.", None

    if len(senha) < 6:
        return False, "A senha precisa ter pelo menos 6 caracteres.", None

    if db.buscar_usuario_por_email(email):
        return False, "Já existe uma conta com este e-mail.", None

    total_usuarios = db.contar_usuarios()
    tipo_usuario = "admin" if total_usuarios == 0 else "aluno"

    senha_hash = gerar_hash_senha(senha)
    usuario = db.criar_usuario(nome, email, senha_hash, empresa, tipo_usuario)

    if usuario is None:
        return False, "Não foi possível criar a conta. Tente novamente.", None

    return True, "Conta criada com sucesso!", usuario


def login(email: str, senha: str):
    """Tenta autenticar o usuário.
    Retorna (sucesso: bool, mensagem: str, usuario: dict|None)."""

    if not email or not senha:
        return False, "Preencha e-mail e senha.", None

    usuario = db.buscar_usuario_por_email(email)
    if usuario is None:
        return False, "E-mail ou senha incorretos.", None

    if not conferir_senha(senha, usuario["senha_hash"]):
        return False, "E-mail ou senha incorretos.", None

    return True, "Login realizado com sucesso!", usuario
