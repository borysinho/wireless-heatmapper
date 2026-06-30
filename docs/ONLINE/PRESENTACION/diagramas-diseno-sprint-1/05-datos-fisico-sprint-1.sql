-- ============================================================
-- Wireless HeatMapper — Esquema PostgreSQL 15
-- Sprint 1 — Estado final tras aplicar todas las migraciones Alembic:
--   073ed4d23a33 (init vacía)
--   → d4e5f6a7b8c9 (crear tabla usuario)
--   → e5f6a7b8c9d0 (ultimo_acceso + refresh_token + proyecto stub)
--   → f6a7b8c9d0e1 (tabla cliente + proyecto.cliente_id FK)
--   → 83b6c2b1a08c (proyecto.descripcion)
--   → b1c2d3e4f5a6 (ENUM estado_proyecto, migra VARCHAR → ENUM)
-- Base de datos: heatmapper_db
-- Generado desde: 05-datos-fisico-sprint-1.puml
-- ============================================================

-- ─── Tipo ENUM ───────────────────────────────────────────────
-- Creado por migración b1c2d3e4f5a6 (antes de ALTER TABLE proyecto)

CREATE TYPE estado_proyecto AS ENUM (
    'nuevo',
    'en_progreso',
    'completado',
    'archivado'
);

-- ─── Tabla: usuario ──────────────────────────────────────────
-- Migración d4e5f6a7b8c9 + columna ultimo_acceso en e5f6a7b8c9d0

CREATE TABLE usuario (
    id            SERIAL          NOT NULL,
    nombre        VARCHAR(120)    NOT NULL,
    email         VARCHAR(255)    NOT NULL,
    password_hash VARCHAR(255)    NOT NULL,
    rol           VARCHAR(30)     NOT NULL    DEFAULT 'tecnico',
    activo        BOOLEAN         NOT NULL    DEFAULT TRUE,
    created_at    TIMESTAMPTZ                 DEFAULT now(),
    ultimo_acceso TIMESTAMPTZ,
    CONSTRAINT pk_usuario PRIMARY KEY (id)
);

CREATE INDEX        ix_usuario_id    ON usuario (id);
CREATE UNIQUE INDEX ix_usuario_email ON usuario (email);

-- ─── Tabla: refresh_token ────────────────────────────────────
-- Migración e5f6a7b8c9d0

CREATE TABLE refresh_token (
    id          SERIAL      NOT NULL,
    token       VARCHAR(64) NOT NULL,
    usuario_id  INTEGER     NOT NULL,
    expires_at  TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT now(),
    CONSTRAINT pk_refresh_token PRIMARY KEY (id),
    CONSTRAINT fk_refresh_token_usuario_id FOREIGN KEY (usuario_id)
        REFERENCES usuario (id) ON DELETE CASCADE
);

CREATE INDEX        ix_refresh_token_id         ON refresh_token (id);
CREATE UNIQUE INDEX ix_refresh_token_token      ON refresh_token (token);
CREATE INDEX        ix_refresh_token_usuario_id ON refresh_token (usuario_id);

-- ─── Tabla: cliente ──────────────────────────────────────────
-- Migración f6a7b8c9d0e1

CREATE TABLE cliente (
    id         SERIAL       NOT NULL,
    nombre     VARCHAR(100) NOT NULL,
    activo     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ           DEFAULT now(),
    CONSTRAINT pk_cliente        PRIMARY KEY (id),
    CONSTRAINT uq_cliente_nombre UNIQUE      (nombre)
);

CREATE INDEX ix_cliente_id ON cliente (id);

-- ─── Tabla: proyecto ─────────────────────────────────────────
-- Migración e5f6a7b8c9d0 (stub inicial) +
--   f6a7b8c9d0e1 (agrega cliente_id, elimina cliente texto) +
--   83b6c2b1a08c (agrega descripcion) +
--   b1c2d3e4f5a6 (estado: VARCHAR → ENUM, default 'nuevo')

CREATE TABLE proyecto (
    id               SERIAL           NOT NULL,
    nombre           VARCHAR(200)     NOT NULL,
    descripcion      VARCHAR(500),
    estado           estado_proyecto  NOT NULL    DEFAULT 'nuevo',
    tecnico_id       INTEGER          NOT NULL,
    cliente_id       INTEGER,
    ultima_actividad TIMESTAMPTZ                  DEFAULT now(),
    cantidad_puntos  INTEGER          NOT NULL    DEFAULT 0,
    created_at       TIMESTAMPTZ                  DEFAULT now(),
    CONSTRAINT pk_proyecto PRIMARY KEY (id),
    CONSTRAINT fk_proyecto_tecnico_id FOREIGN KEY (tecnico_id)
        REFERENCES usuario (id),
    CONSTRAINT fk_proyecto_cliente_id FOREIGN KEY (cliente_id)
        REFERENCES cliente (id)
);

CREATE INDEX ix_proyecto_id         ON proyecto (id);
CREATE INDEX ix_proyecto_tecnico_id ON proyecto (tecnico_id);
CREATE INDEX ix_proyecto_cliente_id ON proyecto (cliente_id);
