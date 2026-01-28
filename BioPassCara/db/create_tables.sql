-- Crea la base de datos 'biopass_db' manualmente en pgAdmin o consola primero.
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    foto_bytes BYTEA NOT NULL, -- Foto completa
    cara_bytes BYTEA NOT NULL  -- Solo el recorte de la cara para entrenar
);