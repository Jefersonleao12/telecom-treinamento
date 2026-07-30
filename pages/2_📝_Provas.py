"""
Página: Provas
---------------
Mostra o questionário do curso escolhido, calcula a nota automaticamente
ao enviar e grava a tentativa no banco de dados.
"""

import streamlit as st
import database as db

st.set_page_config(page_title="Provas", page_icon="📝", layout="centered")

if st.session_state.get("usuario") is None:
    st.warning("Você precisa entrar na sua conta primeiro.")
    st.stop()

usuario = st.session_state["usuario"]

st.title("📝 Avaliação do Curso")

cursos = db.listar_cursos()
if not cursos:
    st.info("Ainda não há nenhum curso cadastrado.")
    st.stop()

nomes_cursos = {c["titulo"]: c for c in cursos}
titulo_escolhido = st.selectbox("Selecione o curso:", list(nomes_cursos.keys()))
curso = nomes_cursos[titulo_escolhido]

questoes = db.listar_questoes_do_curso(curso["id"])

if not questoes:
    st.info("Este curso ainda não possui uma prova cadastrada.")
    st.stop()

nota_minima = float(curso.get("nota_minima_aprovacao", 7.0))
st.caption(f"Nota mínima para aprovação: **{nota_minima:.1f}** (de 0 a 10)")

# Mostra o melhor resultado já obtido, se existir
melhor = db.melhor_tentativa(usuario["id"], curso["id"])
if melhor:
    status = "✅ Aprovado" if melhor["aprovado"] else "❌ Reprovado"
    st.info(f"Sua melhor tentativa até agora: nota **{melhor['nota']:.1f}** — {status}")

st.divider()

with st.form("form_prova"):
    respostas_aluno = {}

    for i, questao in enumerate(questoes, start=1):
        st.markdown(f"**{i}. {questao['enunciado']}**")
        opcoes = {
            "A": questao["opcao_a"],
            "B": questao["opcao_b"],
            "C": questao["opcao_c"],
            "D": questao["opcao_d"],
        }
        escolha = st.radio(
            "Escolha uma alternativa:",
            options=list(opcoes.keys()),
            format_func=lambda letra, opcoes=opcoes: f"{letra}) {opcoes[letra]}",
            key=f"questao_{questao['id']}",
            index=None,
        )
        respostas_aluno[questao["id"]] = escolha
        st.write("")

    enviado = st.form_submit_button("Enviar prova e calcular nota", use_container_width=True)

if enviado:
    nao_respondidas = [qid for qid, resp in respostas_aluno.items() if resp is None]
    if nao_respondidas:
        st.error("Responda todas as questões antes de enviar a prova.")
    else:
        acertos = 0
        for questao in questoes:
            if respostas_aluno[questao["id"]] == questao["resposta_correta"]:
                acertos += 1

        total_questoes = len(questoes)
        nota_final = round((acertos / total_questoes) * 10, 1)
        aprovado = nota_final >= nota_minima

        db.salvar_tentativa(usuario["id"], curso["id"], nota_final, aprovado)

        st.subheader("Resultado")
        st.metric("Sua nota", f"{nota_final:.1f} / 10")
        st.write(f"Você acertou {acertos} de {total_questoes} questões.")

        if aprovado:
            st.success(
                "🎉 Parabéns, você foi **aprovado(a)**! "
                "Vá até a página **Certificado** no menu ao lado para emitir o seu certificado."
            )
            st.balloons()
        else:
            st.error(
                f"Você não atingiu a nota mínima ({nota_minima:.1f}). "
                "Revise as aulas e tente novamente."
            )
