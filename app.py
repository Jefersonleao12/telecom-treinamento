"""
app.py
-------
Ponto de entrada da plataforma. Cuida do Login e Cadastro.
As demais telas (Aulas, Provas, Certificado, Admin) ficam na pasta /pages
e o próprio Streamlit já cria o menu lateral automaticamente com elas.
"""

import streamlit as st
import auth

st.set_page_config(
    page_title="Plataforma de Treinamentos - Telecom",
    page_icon="📡",
    layout="centered",
)

# Garante que exista sempre uma variável de sessão para o usuário logado
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None


def tela_login():
    st.subheader("Entrar na plataforma")
    with st.form("form_login"):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        enviado = st.form_submit_button("Entrar", use_container_width=True)

    if enviado:
        sucesso, mensagem, usuario = auth.login(email, senha)
        if sucesso:
            st.session_state["usuario"] = usuario
            st.success(mensagem)
            st.rerun()
        else:
            st.error(mensagem)


def tela_cadastro():
    st.subheader("Criar minha conta")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome completo")
        email = st.text_input("E-mail")
        empresa = st.text_input("Empresa")
        senha = st.text_input("Senha (mínimo 6 caracteres)", type="password")
        enviado = st.form_submit_button("Cadastrar", use_container_width=True)

    if enviado:
        sucesso, mensagem, usuario = auth.cadastrar_usuario(nome, email, senha, empresa)
        if sucesso:
            st.session_state["usuario"] = usuario
            st.success(mensagem + " Você já está logado(a).")
            st.rerun()
        else:
            st.error(mensagem)


# ============================================================
# TELA PRINCIPAL
# ============================================================

st.title("📡 Plataforma de Treinamentos em Telecomunicações")

if st.session_state["usuario"] is not None:
    usuario = st.session_state["usuario"]
    st.success(f"Você está logado(a) como **{usuario['nome']}** ({usuario['tipo_usuario']}).")
    st.info("Use o menu à esquerda (ou o menu ☰ no celular) para acessar: "
            "**Aulas**, **Provas** e **Certificado**.")

    if st.button("Sair da conta"):
        st.session_state["usuario"] = None
        st.rerun()
else:
    aba_login, aba_cadastro = st.tabs(["🔐 Entrar", "📝 Criar Conta"])
    with aba_login:
        tela_login()
    with aba_cadastro:
        tela_cadastro()
        st.caption(
            "ℹ️ O primeiro usuário cadastrado no sistema vira automaticamente "
            "**Administrador/Instrutor**. Os demais entram como **Aluno**."
        )
