"""
Página: Certificado
---------------------
Verifica se o aluno foi aprovado no curso escolhido e, se sim, gera
(ou recupera) o certificado em PDF para download.
"""

import uuid

import streamlit as st
import database as db
from certificado import gerar_certificado_pdf

st.set_page_config(page_title="Certificado", page_icon="🎓", layout="centered")

if st.session_state.get("usuario") is None:
    st.warning("Você precisa entrar na sua conta primeiro.")
    st.stop()

usuario = st.session_state["usuario"]

st.title("🎓 Meu Certificado")

cursos = db.listar_cursos()
if not cursos:
    st.info("Ainda não há nenhum curso cadastrado.")
    st.stop()

nomes_cursos = {c["titulo"]: c for c in cursos}
titulo_escolhido = st.selectbox("Selecione o curso:", list(nomes_cursos.keys()))
curso = nomes_cursos[titulo_escolhido]

melhor_tentativa = db.melhor_tentativa(usuario["id"], curso["id"])

if not melhor_tentativa or not melhor_tentativa["aprovado"]:
    st.warning(
        "Você ainda não foi aprovado(a) neste curso. "
        "Complete as aulas e seja aprovado(a) na prova (página **Provas**) "
        "para liberar o certificado."
    )
    st.stop()

# Verifica se já existe um certificado emitido; se não existir, cria um novo
certificado_existente = db.buscar_certificado(usuario["id"], curso["id"])

if certificado_existente:
    codigo_validacao = certificado_existente["codigo_validacao"]
else:
    codigo_validacao = str(uuid.uuid4())[:8].upper()
    db.criar_certificado(usuario["id"], curso["id"], codigo_validacao)

st.success(f"✅ Você foi aprovado(a) com nota {melhor_tentativa['nota']:.1f}!")

pdf_bytes = gerar_certificado_pdf(
    nome_aluno=usuario["nome"],
    empresa=usuario.get("empresa", ""),
    nome_curso=curso["titulo"],
    nome_instrutor=curso["instrutor"],
    nota=melhor_tentativa["nota"],
    carga_horaria_texto="conforme conteúdo ministrado",
    codigo_validacao=codigo_validacao,
)

st.download_button(
    label="⬇️ Baixar Certificado em PDF",
    data=pdf_bytes,
    file_name=f"certificado_{curso['titulo'].replace(' ', '_')}.pdf",
    mime="application/pdf",
    use_container_width=True,
)

st.caption(f"Código de validação do certificado: **{codigo_validacao}**")
