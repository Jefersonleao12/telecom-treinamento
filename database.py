"""
database.py
------------
Este arquivo centraliza TODA a comunicação com o banco de dados (Supabase).
Se um dia você quiser trocar de banco de dados, só precisa mexer aqui.
"""

import streamlit as st
from supabase import create_client, Client


@st.cache_resource(show_spinner=False)
def get_supabase_client() -> Client:
    """Cria (uma única vez) a conexão com o Supabase, usando as chaves
    guardadas em .streamlit/secrets.toml (ou nos 'Secrets' do Streamlit Cloud)."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase = get_supabase_client()


# ============================================================
# USUÁRIOS
# ============================================================

def contar_usuarios() -> int:
    resposta = supabase.table("usuarios").select("id", count="exact").execute()
    return resposta.count or 0


def buscar_usuario_por_email(email: str):
    resposta = (
        supabase.table("usuarios")
        .select("*")
        .eq("email", email.strip().lower())
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


def criar_usuario(nome: str, email: str, senha_hash: str, empresa: str, tipo_usuario: str):
    novo = {
        "nome": nome.strip(),
        "email": email.strip().lower(),
        "senha_hash": senha_hash,
        "empresa": empresa.strip(),
        "tipo_usuario": tipo_usuario,
    }
    resposta = supabase.table("usuarios").insert(novo).execute()
    return resposta.data[0] if resposta.data else None


def listar_usuarios():
    resposta = supabase.table("usuarios").select("*").order("criado_em").execute()
    return resposta.data


# ============================================================
# CURSOS
# ============================================================

def listar_cursos():
    resposta = supabase.table("cursos").select("*").order("criado_em").execute()
    return resposta.data


def buscar_curso(curso_id: str):
    resposta = supabase.table("cursos").select("*").eq("id", curso_id).execute()
    dados = resposta.data
    return dados[0] if dados else None


def criar_curso(titulo: str, descricao: str, instrutor: str, nota_minima: float):
    novo = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip(),
        "instrutor": instrutor.strip(),
        "nota_minima_aprovacao": nota_minima,
    }
    resposta = supabase.table("cursos").insert(novo).execute()
    return resposta.data[0] if resposta.data else None


# ============================================================
# AULAS
# ============================================================

def listar_aulas_do_curso(curso_id: str):
    resposta = (
        supabase.table("aulas")
        .select("*")
        .eq("curso_id", curso_id)
        .order("ordem")
        .execute()
    )
    return resposta.data


def criar_aula(curso_id: str, titulo: str, video_youtube_id: str, ordem: int):
    novo = {
        "curso_id": curso_id,
        "titulo": titulo.strip(),
        "video_youtube_id": video_youtube_id.strip(),
        "ordem": ordem,
    }
    resposta = supabase.table("aulas").insert(novo).execute()
    return resposta.data[0] if resposta.data else None


# ============================================================
# PROGRESSO DO ALUNO NAS AULAS
# ============================================================

def buscar_progresso(usuario_id: str, curso_id: str):
    """Retorna um dicionário {aula_id: True/False} com o progresso do aluno."""
    aulas = listar_aulas_do_curso(curso_id)
    if not aulas:
        return {}
    aula_ids = [a["id"] for a in aulas]
    resposta = (
        supabase.table("progresso_aulas")
        .select("aula_id, concluida")
        .eq("usuario_id", usuario_id)
        .in_("aula_id", aula_ids)
        .execute()
    )
    progresso = {a["id"]: False for a in aulas}
    for linha in resposta.data:
        progresso[linha["aula_id"]] = linha["concluida"]
    return progresso


def marcar_aula(usuario_id: str, aula_id: str, concluida: bool):
    """Marca ou desmarca uma aula como concluída (faz 'upsert')."""
    from datetime import datetime, timezone

    dados = {
        "usuario_id": usuario_id,
        "aula_id": aula_id,
        "concluida": concluida,
        "data_conclusao": datetime.now(timezone.utc).isoformat() if concluida else None,
    }
    supabase.table("progresso_aulas").upsert(dados, on_conflict="usuario_id,aula_id").execute()


# ============================================================
# QUESTÕES / PROVAS
# ============================================================

def listar_questoes_do_curso(curso_id: str):
    resposta = (
        supabase.table("questoes")
        .select("*")
        .eq("curso_id", curso_id)
        .execute()
    )
    return resposta.data


def criar_questao(curso_id, enunciado, opcao_a, opcao_b, opcao_c, opcao_d, resposta_correta):
    novo = {
        "curso_id": curso_id,
        "enunciado": enunciado.strip(),
        "opcao_a": opcao_a.strip(),
        "opcao_b": opcao_b.strip(),
        "opcao_c": opcao_c.strip(),
        "opcao_d": opcao_d.strip(),
        "resposta_correta": resposta_correta,
    }
    resposta = supabase.table("questoes").insert(novo).execute()
    return resposta.data[0] if resposta.data else None


def salvar_tentativa(usuario_id: str, curso_id: str, nota: float, aprovado: bool):
    novo = {
        "usuario_id": usuario_id,
        "curso_id": curso_id,
        "nota": nota,
        "aprovado": aprovado,
    }
    resposta = supabase.table("tentativas_provas").insert(novo).execute()
    return resposta.data[0] if resposta.data else None


def melhor_tentativa(usuario_id: str, curso_id: str):
    """Retorna a tentativa de maior nota do aluno naquele curso (ou None)."""
    resposta = (
        supabase.table("tentativas_provas")
        .select("*")
        .eq("usuario_id", usuario_id)
        .eq("curso_id", curso_id)
        .order("nota", desc=True)
        .limit(1)
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


# ============================================================
# CERTIFICADOS
# ============================================================

def buscar_certificado(usuario_id: str, curso_id: str):
    resposta = (
        supabase.table("certificados")
        .select("*")
        .eq("usuario_id", usuario_id)
        .eq("curso_id", curso_id)
        .execute()
    )
    dados = resposta.data
    return dados[0] if dados else None


def criar_certificado(usuario_id: str, curso_id: str, codigo_validacao: str):
    novo = {
        "usuario_id": usuario_id,
        "curso_id": curso_id,
        "codigo_validacao": codigo_validacao,
    }
    resposta = supabase.table("certificados").insert(novo).execute()
    return resposta.data[0] if resposta.data else None
