-- ⚠️ RESET: Borrar tablas antiguas para limpiar pedidos
DROP TABLE IF EXISTS items_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS productos;

-- Tabla de Productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT,
    activo BOOLEAN DEFAULT 1
);

-- Tabla de Pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_cliente TEXT,
    telefono TEXT,
    hora_recogida TEXT,
    estado TEXT DEFAULT 'pendiente', -- pendiente, listo, entregado
    canal TEXT DEFAULT 'MOSTRADOR',
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla Detalle Pedido
CREATE TABLE IF NOT EXISTS items_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    nombre_snapshot TEXT NOT NULL, -- Guardamos el nombre por si cambia el producto
    precio_snapshot REAL NOT NULL, -- Guardamos el precio del momento de la compra
    cantidad INTEGER NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
    FOREIGN KEY (producto_id) REFERENCES productos (id)
);

-- Datos iniciales: POLLERIA COMPLETA
INSERT INTO productos (nombre, precio, categoria) VALUES 
-- POLLOS
('Pollo a l''Ast', 14.00, 'POLLO'),
('Medio Pollo', 7.50, 'POLLO'),
('Cuarto de Pollo', 4.50, 'POLLO'),
('Conejo a l''Ast', 16.00, 'POLLO'),

-- FRITOS Y TAPAS
('Croquetas Pollo (u)', 1.20, 'FRITOS'),
('Croquetas Jamón (u)', 1.20, 'FRITOS'),
('Croquetas Setas (u)', 1.20, 'FRITOS'),
('Croquetas Cocido (u)', 1.20, 'FRITOS'),
('Nuggets (6u)', 3.50, 'FRITOS'),
('Alitas BBQ (6u)', 4.50, 'FRITOS'),
('Lágrimas Pollo', 4.00, 'FRITOS'),
('San Jacobo', 2.50, 'FRITOS'),
('Empanadillas (u)', 1.50, 'FRITOS'),

-- GUARNICIONES
('Patatas Fritas', 3.50, 'GUARNICION'),
('Patatas Bravas', 4.20, 'GUARNICION'),
('Patatas Alioli', 4.20, 'GUARNICION'),
('Pimientos Padrón', 4.00, 'GUARNICION'),
('Ensaladilla Rusa', 4.50, 'GUARNICION'),
('Escalivada', 5.00, 'GUARNICION'),

-- PLATOS PREPARADOS
('Canelone Carne (3u)', 5.50, 'PLATOS'),
('Canelone Espinacas', 5.50, 'PLATOS'),
('Lasaña Bolognesa', 6.00, 'PLATOS'),
('Macarrones Bolo', 4.50, 'PLATOS'),
('Albóndigas Jardinera', 5.50, 'PLATOS'),
('Fideuá', 6.00, 'PLATOS'),

-- BEBIDAS Y OTROS
('Coca-Cola', 1.80, 'BEBIDA'),
('Coca-Cola Zero', 1.80, 'BEBIDA'),
('Fanta Naranja', 1.80, 'BEBIDA'),
('Fanta Limón', 1.80, 'BEBIDA'),
('Agua 1.5L', 1.50, 'BEBIDA'),
('Cerveza Lata', 1.50, 'BEBIDA'),
('Vino Tinto', 4.50, 'BEBIDA'),
('Barra de Pan', 1.20, 'OTROS'),
('Salsa Alioli', 1.50, 'OTROS'),
('Salsa Brava', 1.50, 'OTROS');
