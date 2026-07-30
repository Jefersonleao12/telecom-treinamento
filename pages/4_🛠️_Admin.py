"""
Página: Admin
--------------
Painel restrito ao usuário com tipo_usuario == 'admin'.
Permite cadastrar cursos, aulas (vídeos do YouTube) e questões de prova,
sem precisar mexer diretamente no banco de dados.
"""

import streamlit as st
import database as db
import utils

st.set_page_config(page_title="Admin", page_icon="🛠️", layout="centered")

if st.session_state.get("usuario") is None:
    st.warning("Você precisa entrar na sua conta primeiro.")
    st.stop()

usuario = st.session_state["usuario"]

if usuario["tipo_usuario"] != "admin":
    st.error("Acesso restrito. Esta página é apenas para administradores/instrutores.")
    st.stop()

st.title("🛠️ Painel do Administrador")

aba_cursos, aba_aulas, aba_questoes, aba_alunos = st.tabs(
    ["➕ Cursos", "🎬 Aulas", "❓ Questões da Prova", "👥 Alunos"]
)

# ============================================================
# ABA: CURSOS
# ============================================================
with aba_cursos:
    st.subheader("Cadastrar novo curso")
    with st.form("form_novo_curso"):
        titulo = st.text_input("Título do curso")
        descricao = st.text_area("Descrição breve")
        instrutor = st.text_input("Nome do instrutor (aparece no certificado)")
        nota_minima = st.number_input(
            "Nota mínima para aprovação (0 a 10)", min_value=0.0, max_value=10.0, value=7.0, step=0.5
        )
        enviado = st.form_submit_button("Cadastrar curso", use_container_width=True)

    if enviado:
        if not titulo or not instrutor:
            st.error("Preencha ao menos o título e o instrutor.")
        else:
            db.criar_curso(titulo, descricao, instrutor, nota_minima)
            st.success(f"Curso '{titulo}' cadastrado com sucesso!")
            st.rerun()

    st.divider()
    st.subheader("Cursos já cadastrados")
    cursos = db.listar_cursos()
    if cursos:
        for c in cursos:
            st.write(f"- **{c['titulo']}** — Instrutor: {c['instrutor']} "
                     f"— Nota mínima: {c['nota_minima_aprovacao']}")
    else:
        st.caption("Nenhum curso cadastrado ainda.")

# ============================================================
# ABA: AULAS
# ============================================================
with aba_aulas:
    st.subheader("Cadastrar nova aula (vídeo)")
    cursos = db.listar_cursos()

    if not cursos:
        st.info("Cadastre um curso primeiro, na aba '➕ Cursos'.")
    else:
        nomes_cursos = {c["titulo"]: c for c in cursos}
        with st.form("form_nova_aula"):
            curso_escolhido = st.selectbox("Curso", list(nomes_cursos.keys()))
            titulo_aula = st.text_input("Título da aula")
            link_youtube = st.text_input(
                "Link do vídeo no YouTube (cole a URL completa, ex: "
                "https://www.youtube.com/watch?v=XXXXXXXXXXX)"
            )
            ordem = st.number_input("Ordem de exibição", min_value=1, value=1, step=1)
            enviado_aula = st.form_submit_button("Cadastrar aula", use_container_width=True)

        if enviado_aula:
            if not titulo_aula or not link_youtube:
                st.error("Preencha o título e o link do vídeo.")
            else:
                curso_id = nomes_cursos[curso_escolhido]["id"]
                video_id = utils.extrair_id_youtube(link_youtube)
                db.criar_aula(curso_id, titulo_aula, video_id, int(ordem))
                st.success(f"Aula '{titulo_aula}' cadastrada com sucesso!")
                st.rerun()

        st.divider()
        st.subheader("Aulas já cadastradas")
        curso_ver = st.selectbox(
            "Ver aulas do curso:", list(nomes_cursos.keys()), key="ver_aulas_curso"
        )
        aulas = db.listar_aulas_do_curso(nomes_cursos[curso_ver]["id"])
        if aulas:
            for a in aulas:
                st.write(f"- {a['ordem']}. {a['titulo']} (vídeo: {a['video_youtube_id']})")
        else:
            st.caption("Nenhuma aula cadastrada para este curso ainda.")

# ============================================================
# ABA: QUESTÕES
# ============================================================
with aba_questoes:
    st.subheader("Cadastrar nova questão de prova")
    cursos = db.listar_cursos()

    if not cursos:
        st.info("Cadastre um curso primeiro, na aba '➕ Cursos'.")
    else:
        nomes_cursos = {c["titulo"]: c for c in cursos}
        with st.form("form_nova_questao"):
            curso_escolhido_q = st.selectbox("Curso", list(nomes_cursos.keys()), key="curso_questao")
            enunciado = st.text_area("Enunciado da pergunta")
            opcao_a = st.text_input("Alternativa A")
            opcao_b = st.text_input("Alternativa B")
            opcao_c = st.text_input("Alternativa C")
            opcao_d = st.text_input("Alternativa D")
            resposta_correta = st.selectbox("Qual é a alternativa correta?", ["A", "B", "C", "D"])
            enviado_questao = st.form_submit_button("Cadastrar questão", use_container_width=True)

        if enviado_questao:
            campos = [enunciado, opcao_a, opcao_b, opcao_c, opcao_d]
            if not all(campos):
                st.error("Preencha todos os campos da questão.")
            else:
                curso_id = nomes_cursos[curso_escolhido_q]["id"]
                db.criar_questao(
                    curso_id, enunciado, opcao_a, opcao_b, opcao_c, opcao_d, resposta_correta
                )
                st.success("Questão cadastrada com sucesso!")
                st.rerun()

        st.divider()
        st.subheader("Questões já cadastradas")
        curso_ver_q = st.selectbox(
            "Ver questões do curso:", list(nomes_cursos.keys()), key="ver_questoes_curso"
        )
        questoes = db.listar_questoes_do_curso(nomes_cursos[curso_ver_q]["id"])
        if questoes:
            for i, q in enumerate(questoes, start=1):
                st.write(f"**{i}.** {q['enunciado']} (correta: {q['resposta_correta']})")
        else:
            st.caption("Nenhuma questão cadastrada para este curso ainda.")

# ============================================================
# ABA: ALUNOS
# ============================================================
with aba_alunos:
    st.subheader("Alunos cadastrados")
    usuarios = db.listar_usuarios()
    if usuarios:
        for u in usuarios:
            st.write(f"- **{u['nome']}** ({u['email']}) — {u['empresa']} — tipo: {u['tipo_usuario']}")
    else:
        st.caption("Nenhum usuário cadastrado ainda.")
