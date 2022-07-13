CREATE TABLE IF NOT EXISTS bancos (
    id serial PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    ano INTEGER,
    trimestre VARCHAR (255),
    categoria VARCHAR (255),
    tipo VARCHAR (255),
    cnpj VARCHAR (255),
    instituicao_financeira VARCHAR (255),
    indice DECIMAL,
    qtde_reclamacoes_reguladas_procedentes INTEGER,
    qtde_reclamacoes_reguladas_outras INTEGER,
    qtde_de_reclamacoes_nao_reguladas INTEGER,
    qtde_total_reclamacoes INTEGER,
    qtde_total_clientes_spa_ccs_e_scr INTEGER,
    qtde_clientes_spa_ccs INTEGER,
    qtde_clientes_spa_scr INTEGER
);

CREATE TABLE IF NOT EXISTS lista_tarifas (
    id serial PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    cnpj VARCHAR (255),
    codigo_servico VARCHAR(255),
    data_vigencia VARCHAR(255),
    periodicidade VARCHAR(255),
    servico VARCHAR(255),
    tipo_valor VARCHAR(255),
    unidade VARCHAR(255),
    valor_maximo VARCHAR(255)
);



