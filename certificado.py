"""
certificado.py
---------------
Gera o certificado em PDF usando a biblioteca ReportLab (gratuita).
O PDF é gerado inteiramente em memória (BytesIO), sem precisar salvar
nenhum arquivo no servidor.
"""

from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas


def gerar_certificado_pdf(
    nome_aluno: str,
    empresa: str,
    nome_curso: str,
    nome_instrutor: str,
    nota: float,
    carga_horaria_texto: str,
    codigo_validacao: str,
) -> BytesIO:
    """Monta o PDF do certificado e devolve os bytes prontos para download."""

    buffer = BytesIO()
    largura, altura = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    azul = HexColor("#0F6CBD")
    cinza_escuro = HexColor("#333333")

    # --- Moldura decorativa ---
    c.setStrokeColor(azul)
    c.setLineWidth(4)
    c.rect(1 * cm, 1 * cm, largura - 2 * cm, altura - 2 * cm)
    c.setLineWidth(1)
    c.rect(1.3 * cm, 1.3 * cm, largura - 2.6 * cm, altura - 2.6 * cm)

    # --- Título ---
    c.setFont("Helvetica-Bold", 34)
    c.setFillColor(azul)
    c.drawCentredString(largura / 2, altura - 4 * cm, "CERTIFICADO DE CONCLUSÃO")

    c.setFont("Helvetica", 14)
    c.setFillColor(cinza_escuro)
    c.drawCentredString(largura / 2, altura - 5.2 * cm, "Treinamento em Telecomunicações")

    # --- Texto principal ---
    c.setFont("Helvetica", 15)
    c.drawCentredString(largura / 2, altura - 7.5 * cm, "Certificamos que")

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(azul)
    c.drawCentredString(largura / 2, altura - 8.8 * cm, nome_aluno)

    c.setFont("Helvetica", 14)
    c.setFillColor(cinza_escuro)
    texto_empresa = f"da empresa {empresa}," if empresa else ""
    c.drawCentredString(largura / 2, altura - 9.8 * cm, texto_empresa)

    c.setFont("Helvetica", 15)
    linha1 = f"concluiu com aproveitamento o curso \"{nome_curso}\","
    c.drawCentredString(largura / 2, altura - 11 * cm, linha1)

    linha2 = f"com carga horária de {carga_horaria_texto}, obtendo nota final {nota:.1f}."
    c.drawCentredString(largura / 2, altura - 11.9 * cm, linha2)

    # --- Data de emissão ---
    data_emissao = datetime.now().strftime("%d/%m/%Y")
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(largura / 2, altura - 13.2 * cm, f"Emitido em {data_emissao}")

    # --- Assinatura do instrutor ---
    centro_x = largura / 2
    y_assinatura = 4.3 * cm

    c.setFont("Helvetica-Oblique", 20)
    c.setFillColor(azul)
    c.drawCentredString(centro_x, y_assinatura + 0.6 * cm, nome_instrutor)

    c.setStrokeColor(cinza_escuro)
    c.setLineWidth(0.8)
    c.line(centro_x - 4 * cm, y_assinatura, centro_x + 4 * cm, y_assinatura)

    c.setFont("Helvetica", 11)
    c.setFillColor(cinza_escuro)
    c.drawCentredString(centro_x, y_assinatura - 0.5 * cm, "Instrutor(a) Responsável")

    # --- Código de validação (rodapé) ---
    c.setFont("Helvetica", 9)
    c.setFillColor(cinza_escuro)
    c.drawCentredString(
        largura / 2, 1.7 * cm, f"Código de validação: {codigo_validacao}"
    )

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
