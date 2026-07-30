# 📡 Plataforma de Treinamentos em Telecomunicações — Custo Zero

Sistema completo de treinamentos com login, aulas em vídeo, provas com correção
automática e certificado em PDF. Feito em **Python + Streamlit**, banco de dados
**Supabase (gratuito)** e vídeos hospedados no **YouTube (não listado)**.

---

## Estrutura de Arquivos

```
telecom-treinamento/
│
├── app.py                     # Tela de Login / Cadastro (página inicial)
├── auth.py                    # Lógica de autenticação (bcrypt)
├── database.py                # Toda a comunicação com o Supabase
├── certificado.py             # Geração do certificado em PDF (ReportLab)
├── utils.py                   # Funções auxiliares (ex: extrair ID do YouTube)
├── requirements.txt           # Bibliotecas Python necessárias
├── schema.sql                 # Script para criar as tabelas no Supabase
├── .gitignore                 # Impede que segredos vão para o GitHub
│
├── .streamlit/
│   ├── config.toml            # Tema visual do app
│   └── secrets.toml.example   # Modelo do arquivo de chaves secretas
│
└── pages/
    ├── 1_📚_Aulas.py           # Vídeos + progresso do curso
    ├── 2_📝_Provas.py          # Quiz com nota automática
    ├── 3_🎓_Certificado.py     # Emissão do certificado em PDF
    └── 4_🛠️_Admin.py           # Painel para cadastrar cursos/aulas/questões
```

> O Streamlit cria o menu lateral automaticamente com base nos arquivos
> dentro da pasta `pages/` — você não precisa programar nenhum menu.

---

## PASSO A PASSO — Colocando tudo no ar de graça

### Etapa 1 — Criar o banco de dados gratuito (Supabase)

1. Acesse **https://supabase.com** e crie uma conta gratuita (dá para entrar com GitHub).
2. Clique em **"New Project"**.
   - Escolha um nome (ex: `telecom-treinamento`).
   - Crie uma senha para o banco (guarde-a, mas ela **não** é a chave usada no app).
   - Escolha a região mais próxima (ex: South America - São Paulo).
3. Aguarde ~2 minutos até o projeto ficar pronto.
4. No menu lateral, clique em **"SQL Editor" > "New query"**.
5. Abra o arquivo `schema.sql` deste projeto, copie **todo o conteúdo**, cole no editor e clique em **"RUN"**.
   - Isso cria todas as tabelas (usuários, cursos, aulas, provas, certificados).
6. Agora vá em **"Project Settings" (ícone de engrenagem) > "API"**.
   - Copie o **"Project URL"** → isso vai virar `SUPABASE_URL`.
   - Copie a chave **"anon public"** → isso vai virar `SUPABASE_KEY`.

### Etapa 2 — Subir o código para o GitHub

1. Crie uma conta gratuita em **https://github.com** (se ainda não tiver).
2. Crie um novo repositório (ex: `telecom-treinamento`), pode ser **público ou privado**.
3. Envie todos os arquivos deste projeto para esse repositório
   (pelo site do GitHub em "Add file > Upload files", ou usando `git`).
   - **IMPORTANTE:** não suba o arquivo `secrets.toml` real (ele nem deve existir
     localmente fora do seu computador — as chaves reais só vão no passo 4 abaixo).

### Etapa 3 — Publicar no Streamlit Community Cloud (gratuito)

1. Acesse **https://share.streamlit.io** e entre com sua conta do GitHub.
2. Clique em **"New app"**.
3. Selecione o repositório que você acabou de criar.
4. Em **"Main file path"**, coloque: `app.py`
5. Clique em **"Advanced settings"** → **"Secrets"** e cole:

   ```toml
   SUPABASE_URL = "https://SEU-PROJETO.supabase.co"
   SUPABASE_KEY = "sua-chave-anon-public-aqui"
   ```

   (usando os valores reais que você copiou na Etapa 1).
6. Clique em **"Deploy"**. Em 1–2 minutos sua plataforma estará no ar, com uma
   URL gratuita do tipo `https://seu-app.streamlit.app`.

### Etapa 4 — Criar o primeiro usuário (administrador)

1. Acesse a URL do seu app.
2. Na aba **"Criar Conta"**, cadastre-se com seus dados.
3. Esse **primeiro cadastro se torna automaticamente Administrador/Instrutor**
   (a lógica já está pronta em `auth.py`).
4. Depois de logado, vá em **"🛠️ Admin"** no menu lateral e cadastre:
   - Um curso.
   - As aulas (vídeos) desse curso.
   - As questões da prova.

### Etapa 5 — Hospedar os vídeos das aulas (YouTube, gratuito)

1. Grave ou edite seu vídeo normalmente.
2. Envie o vídeo no **YouTube Studio** (studio.youtube.com) com a
   **visibilidade "Não listado"** (assim ele não aparece em buscas públicas,
   só quem tiver o link/curso consegue assistir).
3. Copie o link do vídeo (ex: `https://www.youtube.com/watch?v=XXXXXXXXXXX`).
4. Cole esse link direto no painel Admin ao cadastrar a aula — o sistema já
   extrai o ID automaticamente.

---

## Como os alunos vão usar

1. Acessam a URL do app → criam conta (empresa, nome, e-mail, senha).
2. Vão em **Aulas** → assistem aos vídeos e marcam cada um como concluído
   (a barra de progresso atualiza sozinha).
3. Vão em **Provas** → respondem o quiz → a nota é calculada automaticamente.
4. Se aprovados (nota ≥ mínima definida no curso), vão em **Certificado** →
   baixam o PDF com nome, empresa, curso, instrutor, nota e assinatura.

---

## Funciona em celular?

Sim. O Streamlit é responsivo por padrão: no celular, o menu lateral vira um
ícone "☰" no canto superior esquerdo, os vídeos e formulários se ajustam
automaticamente à tela.

---

## Limitações do plano gratuito (para você já saber)

- **Streamlit Community Cloud**: o app "dorme" após um tempo sem acesso e
  acorda em alguns segundos quando alguém entra de novo — normal e sem custo.
- **Supabase free**: até 500 MB de banco de dados (mais que suficiente para
  texto/notas/certificados — os vídeos ficam no YouTube, não aqui).
- **YouTube "Não listado"**: qualquer pessoa com o link consegue assistir,
  mesmo sem estar cadastrada na plataforma. Se quiser 100% restrito ao
  aluno logado, seria necessário um serviço pago de streaming — fora do
  escopo "custo zero".

---

## Como alterar/manter o sistema no futuro

- Quer mudar cores/visual → edite `.streamlit/config.toml`.
- Quer mudar textos das telas → edite os arquivos dentro de `pages/`.
- Quer mudar a nota mínima de um curso → já dá para fazer pelo próprio
  painel Admin, sem mexer em código.
- Quer adicionar um campo novo (ex: CPF do aluno) → adicione a coluna na
  tabela `usuarios` no Supabase e no formulário em `app.py`/`auth.py`.
