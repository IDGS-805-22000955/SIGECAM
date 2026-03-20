"""v1_esquema_original

Revision ID: 7b215d75143d
Revises: 
Create Date: 2026-03-19 14:00:06.759815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b215d75143d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.execute("""
             CREATE TABLE `materias_primas`
             (
               `id`              int          NOT NULL AUTO_INCREMENT,
               `codigo_interno`  varchar(50)  NOT NULL,
               `nombre`          varchar(100) NOT NULL,
               `descripcion`     text,
               `cantidad_stock`  decimal(10, 2) DEFAULT '0.00',
               `unidad_medida`   enum('kg','lt','mt','pza','caja') DEFAULT 'pza',
               `costo_unitario`  decimal(10, 2) DEFAULT NULL,
               `lote`            varchar(50)    DEFAULT NULL,
               `fecha_caducidad` date           DEFAULT NULL,
               `foto_path`       varchar(255)   DEFAULT NULL,
               `created_at`      timestamp NULL DEFAULT CURRENT_TIMESTAMP,
               PRIMARY KEY (`id`),
               UNIQUE KEY `codigo_interno` (`codigo_interno`)
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)

  op.execute("""
             CREATE TABLE `persona`
             (
               `id`               int          NOT NULL AUTO_INCREMENT,
               `nombre`           varchar(100) NOT NULL,
               `apellido_paterno` varchar(100) NOT NULL,
               `apellido_materno` varchar(100) DEFAULT NULL,
               `curp`             varchar(18)  DEFAULT NULL,
               `rfc`              varchar(13)  DEFAULT NULL,
               `fecha_nacimiento` date         DEFAULT NULL,
               `genero`           enum('M','F','Otro') DEFAULT NULL,
               `telefono`         varchar(20)  DEFAULT NULL,
               `celular`          varchar(20)  DEFAULT NULL,
               `email`            varchar(100) DEFAULT NULL,
               `foto_path`        varchar(255) DEFAULT NULL,
               `calle`            varchar(150) DEFAULT NULL,
               `numero_exterior`  varchar(10)  DEFAULT NULL,
               `numero_interior`  varchar(10)  DEFAULT NULL,
               `colonia`          varchar(100) DEFAULT NULL,
               `municipio`        varchar(100) DEFAULT NULL,
               `estado`           varchar(100) DEFAULT NULL,
               `codigo_postal`    varchar(10)  DEFAULT NULL,
               `pais`             varchar(100) DEFAULT 'México',
               `created_at`       timestamp NULL DEFAULT CURRENT_TIMESTAMP,
               `updated_at`       timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               PRIMARY KEY (`id`),
               UNIQUE KEY `curp` (`curp`)
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)

  op.execute("""
             CREATE TABLE `productos_terminados`
             (
               `id`                int            NOT NULL AUTO_INCREMENT,
               `codigo_sku`        varchar(50)    NOT NULL,
               `nombre`            varchar(100)   NOT NULL,
               `descripcion`       text,
               `precio_venta`      decimal(10, 2) NOT NULL,
               `cantidad_stock`    int          DEFAULT '0',
               `lote_produccion`   varchar(50)  DEFAULT NULL,
               `fecha_fabricacion` date         DEFAULT NULL,
               `foto_path`         varchar(255) DEFAULT NULL,
               `created_at`        timestamp NULL DEFAULT CURRENT_TIMESTAMP,
               PRIMARY KEY (`id`),
               UNIQUE KEY `codigo_sku` (`codigo_sku`)
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)

  op.execute("""
             CREATE TABLE `users`
             (
               `id`         int          NOT NULL AUTO_INCREMENT,
               `email`      varchar(100) NOT NULL,
               `password`   varchar(255) NOT NULL,
               `role`       enum('admin','user','client') DEFAULT 'client',
               `persona_id` int          NOT NULL,
               `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
               PRIMARY KEY (`id`),
               UNIQUE KEY `email` (`email`),
               KEY          `fk_users_persona` (`persona_id`),
               CONSTRAINT `fk_users_persona` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`) ON DELETE CASCADE
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)

  op.execute("""
             CREATE TABLE `proveedor`
             (
               `id`             int NOT NULL AUTO_INCREMENT,
               `persona_id`     int NOT NULL,
               `nombre_empresa` varchar(150) DEFAULT NULL,
               `created_at`     timestamp NULL DEFAULT CURRENT_TIMESTAMP,
               PRIMARY KEY (`id`),
               UNIQUE KEY `persona_id` (`persona_id`),
               CONSTRAINT `fk_proveedor_persona` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`) ON DELETE CASCADE
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)

  op.execute("""
             CREATE TABLE `movimientos_materia_prima`
             (
               `id`               int            NOT NULL AUTO_INCREMENT,
               `materia_prima_id` int            NOT NULL,
               `tipo_movimiento`  enum('entrada','salida','ajuste') NOT NULL,
               `cantidad`         decimal(10, 2) NOT NULL,
               `motivo`           varchar(255) DEFAULT NULL,
               `user_id`          int            NOT NULL,
               `created_at`       timestamp NULL DEFAULT CURRENT_TIMESTAMP,
               PRIMARY KEY (`id`),
               CONSTRAINT `fk_mov_mp` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
               CONSTRAINT `fk_mov_mp_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)

  op.execute("""
             CREATE TABLE `movimientos_producto_terminado`
             (
               `id`                    int NOT NULL AUTO_INCREMENT,
               `producto_terminado_id` int NOT NULL,
               `tipo_movimiento`       enum('entrada','salida','ajuste') NOT NULL,
               `cantidad`              int NOT NULL,
               `motivo`                varchar(255) DEFAULT NULL,
               `user_id`               int NOT NULL,
               `created_at`            timestamp NULL DEFAULT CURRENT_TIMESTAMP,
               PRIMARY KEY (`id`),
               CONSTRAINT `fk_mov_pt` FOREIGN KEY (`producto_terminado_id`) REFERENCES `productos_terminados` (`id`),
               CONSTRAINT `fk_mov_pt_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)

  op.execute("""
             CREATE TABLE `producto_materia_prima`
             (
               `producto_terminado_id` int            NOT NULL,
               `materia_prima_id`      int            NOT NULL,
               `cantidad`              decimal(10, 2) NOT NULL,
               `unidad`                enum('kg','lt','mt','pza','caja') DEFAULT 'pza',
               PRIMARY KEY (`producto_terminado_id`, `materia_prima_id`),
               CONSTRAINT `fk_ptmp_mp` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
               CONSTRAINT `fk_ptmp_producto` FOREIGN KEY (`producto_terminado_id`) REFERENCES `productos_terminados` (`id`)
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)

  op.execute("""
             CREATE TABLE `proveedor_materia_prima`
             (
               `proveedor_id`     int NOT NULL,
               `materia_prima_id` int NOT NULL,
               `costo_unitario`   decimal(10, 2) DEFAULT NULL,
               PRIMARY KEY (`proveedor_id`, `materia_prima_id`),
               CONSTRAINT `fk_pmp_mp` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
               CONSTRAINT `fk_pmp_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`)
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)

  op.execute("""
             CREATE TABLE `token_blacklist`
             (
               `id`         int          NOT NULL AUTO_INCREMENT,
               `user_id`    int          NOT NULL,
               `token`      varchar(512) NOT NULL,
               `revoked_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
               PRIMARY KEY (`id`),
               CONSTRAINT `fk_token_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
             """)


def downgrade():
    op.execute("SET FOREIGN_KEY_CHECKS = 0;")
    op.execute("DROP TABLE IF EXISTS token_blacklist, proveedor_materia_prima, producto_materia_prima, movimientos_producto_terminado, movimientos_materia_prima, proveedor, users, productos_terminados, persona, materias_primas;")
    op.execute("SET FOREIGN_KEY_CHECKS = 1;")