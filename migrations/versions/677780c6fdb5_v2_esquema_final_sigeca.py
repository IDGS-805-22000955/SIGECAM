"""v2_esquema_final_sigeca

Revision ID: 677780c6fdb5
Revises: 7b215d75143d
Create Date: 2026-03-19 14:14:20.495624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '677780c6fdb5'
down_revision = '7b215d75143d'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("SET FOREIGN_KEY_CHECKS = 0;")
    op.execute("DROP TABLE IF EXISTS token_blacklist, proveedor_materia_prima, producto_materia_prima, movimientos_producto_terminado, movimientos_materia_prima, proveedor, users, productos_terminados, persona, materias_primas;")
    op.execute("SET FOREIGN_KEY_CHECKS = 1;")

    op.execute("""
        CREATE TABLE Materia_Prima (
            id_mp INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            unidad_medida ENUM('Gramos', 'Metros', 'Piezas') NOT NULL,
            porcentaje_merma DECIMAL(5,2) NOT NULL DEFAULT 0.00,
            stock_actual DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            stock_minimo DECIMAL(10,2) NOT NULL DEFAULT 0.00
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Modelo_Zapato (
            id_modelo INT AUTO_INCREMENT PRIMARY KEY,
            codigo_modelo VARCHAR(50) NOT NULL UNIQUE,
            nombre VARCHAR(100) NOT NULL,
            color VARCHAR(50) NOT NULL,
            foto_modelo VARCHAR(255) NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Proveedor (
            id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
            razon_social VARCHAR(150) NOT NULL,
            rfc VARCHAR(20) NULL,
            telefono VARCHAR(20) NULL,
            email VARCHAR(100) NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Cliente (
            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
            nombre_completo VARCHAR(150) NOT NULL,
            rfc_datos VARCHAR(150) NULL,
            email VARCHAR(100) NULL,
            telefono VARCHAR(20) NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            rol ENUM('Admin', 'Ventas', 'Producción', 'Sistemas') NOT NULL,
            intentos_fallidos INT NOT NULL DEFAULT 0,
            ultimo_acceso DATETIME NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Empleados (
            id_empleado INT AUTO_INCREMENT PRIMARY KEY,
            nombre_completo VARCHAR(150) NOT NULL,
            codigo_gafete VARCHAR(50) NOT NULL UNIQUE,
            estacion_asignada ENUM('Cortado', 'Doblillado', 'Pespunte', 'Montado', 'Adornado') NOT NULL,
            estatus BOOLEAN NOT NULL DEFAULT TRUE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Producto_Terminado (
            id_pt INT AUTO_INCREMENT PRIMARY KEY,
            id_modelo INT NOT NULL,
            talla DECIMAL(4,1) NOT NULL,
            precio_venta DECIMAL(10,2) NOT NULL,
            stock_disponible INT NOT NULL DEFAULT 0,
            id_ficha_tecnica INT NULL,
            FOREIGN KEY (id_modelo) REFERENCES Modelo_Zapato(id_modelo) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Ficha_Tecnica (
            id_ficha_tecnica INT AUTO_INCREMENT PRIMARY KEY,
            id_pt INT NOT NULL,
            costo_produccion DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            FOREIGN KEY (id_pt) REFERENCES Producto_Terminado(id_pt) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        ALTER TABLE Producto_Terminado 
        ADD CONSTRAINT fk_pt_ficha 
        FOREIGN KEY (id_ficha_tecnica) REFERENCES Ficha_Tecnica(id_ficha_tecnica) ON DELETE SET NULL;
    """)

    op.execute("""
        CREATE TABLE Bitacora_Sistema (
            id_log INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NULL,
            nivel_evento ENUM('Informativo', 'Advertencia', 'Crítico', 'Error') NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Tokens_Seguridad (
            id_token INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            token_hash VARCHAR(255) NOT NULL,
            tipo ENUM('2FA', 'Recuperacion') NOT NULL,
            fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fecha_expiracion DATETIME NOT NULL,
            usado BOOLEAN NOT NULL DEFAULT FALSE,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Backups_Historial (
            id_backup INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            fecha_generacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ruta_archivo VARCHAR(255) NOT NULL,
            tamano_mb DECIMAL(8,2) NOT NULL,
            estatus ENUM('Exitoso', 'Fallido') NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Compras (
            id_compra INT AUTO_INCREMENT PRIMARY KEY,
            id_proveedor INT NOT NULL,
            id_usuario INT NOT NULL,
            fecha_compra DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            total_compra DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor) ON DELETE RESTRICT,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Pedidos (
            id_pedido INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente INT NOT NULL,
            id_usuario INT NOT NULL,
            fecha_pedido DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            estado_pedido ENUM('Pendiente', 'En Producción', 'Terminado', 'Entregado') NOT NULL DEFAULT 'Pendiente',
            FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE RESTRICT,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Ventas (
            id_venta INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NULL,
            id_cliente INT NULL,
            fecha_venta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            total_venta DECIMAL(10,2) NOT NULL,
            origen_venta ENUM('Mostrador', 'E-commerce') NOT NULL,
            id_transaccion_stripe VARCHAR(100) NULL,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE SET NULL,
            FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Corte_Caja (
            id_corte INT AUTO_INCREMENT PRIMARY KEY,
            id_usuario INT NOT NULL,
            fecha_apertura DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fecha_cierre DATETIME NULL,
            saldo_inicial DECIMAL(10,2) NOT NULL,
            total_ingresos_efectivo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            total_salidas_efectivo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            saldo_final_esperado DECIMAL(10,2) NOT NULL DEFAULT 0.00,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Orden_Produccion (
            id_op INT AUTO_INCREMENT PRIMARY KEY,
            id_pt INT NOT NULL,
            cantidad_pares INT NOT NULL,
            fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            estado_actual ENUM('Pendiente', 'Por Asignar', 'Cortado', 'Doblillado', 'Pespunte', 'Montado', 'Adornado', 'Terminado', 'Cancelado') NOT NULL DEFAULT 'Pendiente',
            FOREIGN KEY (id_pt) REFERENCES Producto_Terminado(id_pt) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Detalle_Ficha_Tecnica (
            id_detalle_ft INT AUTO_INCREMENT PRIMARY KEY,
            id_ficha_tecnica INT NOT NULL,
            id_mp INT NOT NULL,
            cantidad_requerida DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (id_ficha_tecnica) REFERENCES Ficha_Tecnica(id_ficha_tecnica) ON DELETE CASCADE,
            FOREIGN KEY (id_mp) REFERENCES Materia_Prima(id_mp) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Detalle_Compra (
            id_detalle_compra INT AUTO_INCREMENT PRIMARY KEY,
            id_compra INT NOT NULL,
            id_mp INT NOT NULL,
            cantidad DECIMAL(10,2) NOT NULL,
            costo_unitario DECIMAL(10,2) NOT NULL,
            subtotal DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (id_compra) REFERENCES Compras(id_compra) ON DELETE CASCADE,
            FOREIGN KEY (id_mp) REFERENCES Materia_Prima(id_mp) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Detalle_Pedido (
            id_detalle_pedido INT AUTO_INCREMENT PRIMARY KEY,
            id_pedido INT NOT NULL,
            id_pt INT NOT NULL,
            cantidad INT NOT NULL,
            FOREIGN KEY (id_pedido) REFERENCES Pedidos(id_pedido) ON DELETE CASCADE,
            FOREIGN KEY (id_pt) REFERENCES Producto_Terminado(id_pt) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Detalle_Venta (
            id_detalle_venta INT AUTO_INCREMENT PRIMARY KEY,
            id_venta INT NOT NULL,
            id_pt INT NOT NULL,
            cantidad INT NOT NULL,
            precio_venta_historico DECIMAL(10,2) NOT NULL,
            costo_produccion_historico DECIMAL(10,2) NOT NULL,
            subtotal DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta) ON DELETE CASCADE,
            FOREIGN KEY (id_pt) REFERENCES Producto_Terminado(id_pt) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Salida_Efectivo (
            id_salida INT AUTO_INCREMENT PRIMARY KEY,
            id_corte INT NOT NULL,
            id_usuario INT NOT NULL,
            id_proveedor INT NULL,
            monto DECIMAL(10,2) NOT NULL,
            concepto VARCHAR(255) NOT NULL,
            fecha_salida DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_corte) REFERENCES Corte_Caja(id_corte) ON DELETE CASCADE,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE RESTRICT,
            FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Autorizacion_Mermas (
            id_merma INT AUTO_INCREMENT PRIMARY KEY,
            id_op INT NOT NULL,
            id_mp INT NOT NULL,
            id_empleado INT NOT NULL,
            id_usuario_admin INT NULL,
            cantidad_merma DECIMAL(10,2) NOT NULL,
            motivo TEXT NOT NULL,
            estatus ENUM('Pendiente', 'Autorizada', 'Rechazada') NOT NULL DEFAULT 'Pendiente',
            FOREIGN KEY (id_op) REFERENCES Orden_Produccion(id_op) ON DELETE RESTRICT,
            FOREIGN KEY (id_mp) REFERENCES Materia_Prima(id_mp) ON DELETE RESTRICT,
            FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) ON DELETE RESTRICT,
            FOREIGN KEY (id_usuario_admin) REFERENCES Usuarios(id_usuario) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    op.execute("""
        CREATE TABLE Kardex (
            id_kardex INT AUTO_INCREMENT PRIMARY KEY,
            tipo_movimiento ENUM('Entrada', 'Salida') NOT NULL,
            id_mp INT NULL,
            id_pt INT NULL,
            cantidad DECIMAL(10,2) NOT NULL,
            fecha_movimiento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            id_usuario INT NOT NULL,
            FOREIGN KEY (id_mp) REFERENCES Materia_Prima(id_mp) ON DELETE RESTRICT,
            FOREIGN KEY (id_pt) REFERENCES Producto_Terminado(id_pt) ON DELETE RESTRICT,
            FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE RESTRICT
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

def downgrade():
    op.execute("SET FOREIGN_KEY_CHECKS = 0;")
    op.execute("DROP TABLE IF EXISTS Kardex, Autorizacion_Mermas, Salida_Efectivo, Detalle_Venta, Detalle_Pedido, Detalle_Compra, Detalle_Ficha_Tecnica, Orden_Produccion, Corte_Caja, Ventas, Pedidos, Compras, Backups_Historial, Tokens_Seguridad, Bitacora_Sistema, Ficha_Tecnica, Producto_Terminado, Empleados, Usuarios, Cliente, Proveedor, Modelo_Zapato, Materia_Prima;")
    op.execute("SET FOREIGN_KEY_CHECKS = 1;")
