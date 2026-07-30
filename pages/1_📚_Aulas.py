"""
Página: Aulas
--------------
Lista os cursos disponíveis, mostra o player de vídeo (YouTube incorporado)
e permite ao aluno marcar cada aula como concluída, atualizando a barra
de progresso do curso.
"""

import streamlit as st
import database as db
import utils

st.set_page_config(page_title="Aulas", page_icon="📚", layout="centered")

# --- Proteção de acesso: só entra quem está logado ---
if st.session_state.get("usuario") is None:
    st.warning("Você precisa entrar na sua conta primeiro.")
    st.stop()

usuario = st.session_state["usuario"]

st.title("📚 Aulas do Curso")

cursos = db.listar_cursos()

if not cursos:
    st.info("Ainda não há nenhum curso cadastrado. Fale com o administrador.")
    st.stop()

nomes_cursos = {c["titulo"]: c for c in cursos}
titulo_escolhido = st.selectbox("Selecione o curso:", list(nomes_cursos.keys()))
curso = nomes_cursos[titulo_escolhido]

if curso.get("descricao"):
    st.caption(curso["descricao"])

aulas = db.listar_aulas_do_curso(curso["id"])

if not aulas:
    st.info("Este curso ainda não possui aulas cadastradas.")
    st.stop()

progresso = db.buscar_progresso(usuario["id"], curso["id"])
percentual = utils.calcular_progresso_percentual(progresso)

st.subheader("Seu progresso neste curso")
st.progress(int(percentual), text=f"{percentual}% concluído")

st.divider()

for aula in aulas:
    with st.container(border=True):
        st.markdown(f"### {aula['ordem']}. {aula['titulo']}")

        # Incorpora o vídeo do YouTube (funciona igual em celular e computador)
        video_id = aula["video_youtube_id"]
        st.video(f"https://www.youtube.com/watch?v={video_id}")

        concluida_atual = progresso.get(aula["id"], False)
        nova_marcacao = st.checkbox(
            "Marcar esta aula como concluída",
            value=concluida_atual,
            key=f"chk_{aula['id']}",
        )

        if nova_marcacao != concluida_atual:
            db.marcar_aula(usuario["id"], aula["id"], nova_marcacao)
            st.rerun()

if utils.todas_aulas_concluidas(progresso):
    st.success(
        "🎉 Você concluiu todas as aulas deste curso! "
        "Agora vá até a página **Provas** no menu ao lado para fazer a avaliação."
    )
