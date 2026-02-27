CREATE TABLE IF NOT EXISTS usuarios_voz (
    id SERIAL PRIMARY KEY, [cite: 82]
    username VARCHAR(50) UNIQUE NOT NULL, [cite: 83]
    passphrase_text TEXT NOT NULL,
    intentos_fallidos INT DEFAULT 0, [cite: 85]
    bloqueado_hasta TIMESTAMP NULL [cite: 86]
);

CREATE TABLE IF NOT EXISTS log_accesos_voz (
    id SERIAL PRIMARY KEY, [cite: 90]
    usuario_id INT REFERENCES usuarios_voz(id) ON DELETE CASCADE, [cite: 91]
    fecha_intento TIMESTAMP DEFAULT CURRENT_TIMESTAMP, [cite: 91]
    resultado_json JSONB NOT NULL [cite: 92]
);