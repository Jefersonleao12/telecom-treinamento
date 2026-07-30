"""
utils.py
---------
Funções pequenas e reutilizáveis usadas em várias páginas do sistema.
"""

import re


def extrair_id_youtube(url_ou_id: str) -> str:
    """Aceita um link completo do YouTube (várias variações) OU já o ID puro,
    e sempre devolve apenas o ID do vídeo (11 caracteres).

    Exemplos aceitos:
    - https://www.youtube.com/watch?v=ABC123xyz90
    - https://youtu.be/ABC123xyz90
    - https://www.youtube.com/embed/ABC123xyz90
    - ABC123xyz90 (já é o ID)
    """
    texto = url_ou_id.strip()

    padroes = [
        r"(?:v=|/embed/|youtu\.be/|/shorts/)([A-Za-z0-9_-]{11})",
    ]
    for padrao in padroes:
        encontrado = re.search(padrao, texto)
        if encontrado:
            return encontrado.group(1)

    # Se não bateu com nenhum padrão de link, assume que já é o ID puro
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", texto):
        return texto

    return texto  # devolve como está; a validação final é visual (o vídeo não carrega se estiver errado)


def calcular_progresso_percentual(progresso: dict) -> float:
    """Recebe o dicionário {aula_id: True/False} e retorna a % concluída (0 a 100)."""
    if not progresso:
        return 0.0
    total = len(progresso)
    concluidas = sum(1 for v in progresso.values() if v)
    return round((concluidas / total) * 100, 1)


def todas_aulas_concluidas(progresso: dict) -> bool:
    if not progresso:
        return False
    return all(progresso.values())
