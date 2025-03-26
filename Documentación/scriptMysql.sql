-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS detector_ia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Selección de la base de datos
USE detector_ia;

-- Creación de la tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    administrador BOOLEAN DEFAULT FALSE
) ENGINE=InnoDB;

-- Creación de la tabla equipos
CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Creación de la tabla datos
CREATE TABLE IF NOT EXISTS datos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_equipo INT NOT NULL,
    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    imagen LONGBLOB,
    texto TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (id_equipo) REFERENCES equipos(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Creación de la tabla horarios
CREATE TABLE IF NOT EXISTS horarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    dia INT NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Creación de índices para mejorar el rendimiento
CREATE INDEX idx_datos_usuario ON datos(id_usuario);
CREATE INDEX idx_datos_equipo ON datos(id_equipo);
CREATE INDEX idx_datos_fecha ON datos(fecha);
CREATE INDEX idx_horarios_usuario ON horarios(id_usuario);
CREATE INDEX idx_horarios_dia ON horarios(dia);

-- Inserción del usuario administrador inicial
-- El hash corresponde a la contraseña 'admin' - debe cambiarse después de la instalación
INSERT INTO usuarios (nombre, password_hash, administrador)
VALUES ('admin', '$2b$12$ZaJ3HCGKVl.SIU7MU/ZI3uMMXsxeiWJoLpE3.DEVwrP0wqXM15YRa', TRUE)
ON DUPLICATE KEY UPDATE nombre = nombre;