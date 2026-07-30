-- ============================================================
-- SCHEMA DO BANCO DE DADOS - Plataforma de Treinamentos
-- Copie TODO este conteúdo e execute no "SQL Editor" do Supabase
-- (Menu lateral: SQL Editor > New query > colar > RUN)
-- ============================================================

-- Extensão necessária para gerar IDs únicos automaticamente
create extension if not exists "pgcrypto";

-- Tabela de usuários (alunos e administradores/instrutores)
create table if not exists usuarios (
    id uuid primary key default gen_random_uuid(),
    nome text not null,
    email text unique not null,
    senha_hash text not null,
    empresa text,
    tipo_usuario text not null default 'aluno', -- 'aluno' ou 'admin'
    criado_em timestamp with time zone default now()
);

-- Tabela de cursos
create table if not exists cursos (
    id uuid primary key default gen_random_uuid(),
    titulo text not null,
    descricao text,
    instrutor text not null,
    nota_minima_aprovacao numeric not null default 7.0,
    criado_em timestamp with time zone default now()
);

-- Tabela de aulas (vídeos) de cada curso
create table if not exists aulas (
    id uuid primary key default gen_random_uuid(),
    curso_id uuid references cursos(id) on delete cascade,
    titulo text not null,
    video_youtube_id text not null, -- apenas o ID do vídeo do YouTube
    ordem integer not null default 1,
    criado_em timestamp with time zone default now()
);

-- Progresso do aluno em cada aula (quais já assistiu/concluiu)
create table if not exists progresso_aulas (
    id uuid primary key default gen_random_uuid(),
    usuario_id uuid references usuarios(id) on delete cascade,
    aula_id uuid references aulas(id) on delete cascade,
    concluida boolean not null default false,
    data_conclusao timestamp with time zone,
    unique (usuario_id, aula_id)
);

-- Questões de prova de cada curso
create table if not exists questoes (
    id uuid primary key default gen_random_uuid(),
    curso_id uuid references cursos(id) on delete cascade,
    enunciado text not null,
    opcao_a text not null,
    opcao_b text not null,
    opcao_c text not null,
    opcao_d text not null,
    resposta_correta text not null check (resposta_correta in ('A','B','C','D')),
    criado_em timestamp with time zone default now()
);

-- Tentativas de prova realizadas pelos alunos
create table if not exists tentativas_provas (
    id uuid primary key default gen_random_uuid(),
    usuario_id uuid references usuarios(id) on delete cascade,
    curso_id uuid references cursos(id) on delete cascade,
    nota numeric not null,
    aprovado boolean not null,
    data timestamp with time zone default now()
);

-- Certificados emitidos
create table if not exists certificados (
    id uuid primary key default gen_random_uuid(),
    usuario_id uuid references usuarios(id) on delete cascade,
    curso_id uuid references cursos(id) on delete cascade,
    codigo_validacao text unique not null,
    data_emissao timestamp with time zone default now()
);

-- ============================================================
-- IMPORTANTE: por simplicidade, o app usa a chave "anon" do Supabase
-- e faz toda a validação de senha dentro do próprio Python (bcrypt).
-- Por isso deixamos o RLS (Row Level Security) desligado nestas
-- tabelas para o MVP funcionar sem configuração extra de políticas.
-- Se quiser reforçar a segurança depois, ative RLS e crie políticas.
-- ============================================================
alter table usuarios disable row level security;
alter table cursos disable row level security;
alter table aulas disable row level security;
alter table progresso_aulas disable row level security;
alter table questoes disable row level security;
alter table tentativas_provas disable row level security;
alter table certificados disable row level security;
