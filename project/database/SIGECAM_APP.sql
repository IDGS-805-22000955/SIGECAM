CREATE DATABASE IF NOT EXISTS SIGECAM_APP;
USE SIGECAM_APP;

DROP TABLE IF EXISTS `materias_primas`;
CREATE TABLE `materias_primas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo_interno` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `cantidad_stock` decimal(10,2) DEFAULT '0.00',
  `unidad_medida` enum('kg','lt','mt','pza','caja') DEFAULT 'pza',
  `costo_unitario` decimal(10,2) DEFAULT NULL,
  `lote` varchar(50) DEFAULT NULL,
  `fecha_caducidad` date DEFAULT NULL,
  `foto_path` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_interno` (`codigo_interno`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `materias_primas` WRITE;
INSERT INTO `materias_primas` VALUES (1,'MP001','Cuero vacuno full grain','Cuero de primera calidad para zapatos y carteras',150.50,'kg',450.00,'LOTE-CV-2024-01','2025-12-31',NULL,'2026-02-05 18:17:37'),(2,'MP002','Forro textil algodón','Forro de algodón para interior de calzado',200.00,'mt',85.50,'LOTE-FT-2024-02','2026-06-30',NULL,'2026-02-05 18:17:37'),(3,'MP003','Suela de hule natural','Suela antiderrapante para calzado casual',300.00,'pza',120.00,'LOTE-SH-2024-03',NULL,NULL,'2026-02-05 18:17:37'),(4,'MP004','Tacones de madera 5cm','Tacones de madera para calzado femenino',150.00,'pza',65.00,'LOTE-TM-2024-04',NULL,NULL,'2026-02-05 18:17:37'),(5,'MP005','Hebillas metálicas níquel','Hebillas de níquel para cinturones y bolsas',500.00,'pza',8.50,'LOTE-HM-2024-05',NULL,NULL,'2026-02-05 18:17:37'),(6,'MP006','Hilo de nylon resistente','Hilo especial para costura de calzado',50.00,'caja',320.00,'LOTE-HN-2024-06','2027-03-15',NULL,'2026-02-05 18:17:37'),(7,'MP007','Piel de cerdo para forro','Piel suave para forros interiores',80.25,'kg',280.00,'LOTE-PC-2024-07','2025-10-31',NULL,'2026-02-05 18:17:37'),(8,'MP008','Adhesivo de contacto','Pegamento especial para calzado',25.00,'lt',150.00,'LOTE-AD-2024-08','2024-11-30',NULL,'2026-02-05 18:17:37'),(9,'MP009','Ojillos metálicos varios','Ojillos de diferentes tamaños para calzado',1200.00,'pza',0.85,'LOTE-OJ-2024-09',NULL,NULL,'2026-02-05 18:17:37'),(10,'22000955','CHUPONES DE FIERRO','Chupones de fierro',22.00,'kg',123.00,NULL,NULL,'27584198-F07E-415B-AD38-126F5744A1CC_de_tamano_grande.jpeg','2026-02-05 18:52:59');
UNLOCK TABLES;



DROP TABLE IF EXISTS `movimientos_materia_prima`;
CREATE TABLE `movimientos_materia_prima` (
  `id` int NOT NULL AUTO_INCREMENT,
  `materia_prima_id` int NOT NULL,
  `tipo_movimiento` enum('entrada','salida','ajuste') NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `user_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_mov_mp` (`materia_prima_id`),
  KEY `fk_mov_mp_user` (`user_id`),
  CONSTRAINT `fk_mov_mp` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `fk_mov_mp_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `movimientos_materia_prima` WRITE;
UNLOCK TABLES;


DROP TABLE IF EXISTS `movimientos_producto_terminado`;
CREATE TABLE `movimientos_producto_terminado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_terminado_id` int NOT NULL,
  `tipo_movimiento` enum('entrada','salida','ajuste') NOT NULL,
  `cantidad` int NOT NULL,
  `motivo` varchar(255) DEFAULT NULL,
  `user_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_mov_pt` (`producto_terminado_id`),
  KEY `fk_mov_pt_user` (`user_id`),
  CONSTRAINT `fk_mov_pt` FOREIGN KEY (`producto_terminado_id`) REFERENCES `productos_terminados` (`id`),
  CONSTRAINT `fk_mov_pt_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `movimientos_producto_terminado` WRITE;
UNLOCK TABLES;


DROP TABLE IF EXISTS `persona`;
CREATE TABLE `persona` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido_paterno` varchar(100) NOT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `curp` varchar(18) DEFAULT NULL,
  `rfc` varchar(13) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `genero` enum('M','F','Otro') DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `celular` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `foto_path` varchar(255) DEFAULT NULL,
  `calle` varchar(150) DEFAULT NULL,
  `numero_exterior` varchar(10) DEFAULT NULL,
  `numero_interior` varchar(10) DEFAULT NULL,
  `colonia` varchar(100) DEFAULT NULL,
  `municipio` varchar(100) DEFAULT NULL,
  `estado` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `pais` varchar(100) DEFAULT 'México',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `curp` (`curp`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `persona` WRITE;
INSERT INTO `persona` VALUES (1,'ÁLVARO IVAN','GÓMEZ','PÉREZ',NULL,NULL,NULL,NULL,NULL,NULL,'alvaroivan1@icloud.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'México','2026-02-04 19:09:38','2026-02-04 19:09:38'),(2,'ALVARO','GÓMEZ','PÉREZ',NULL,NULL,NULL,NULL,NULL,NULL,'alvaro@consulthink.mx',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'México','2026-02-05 00:55:32','2026-02-05 00:55:32'),(5,'ALVARO','GÓMEZ',NULL,NULL,'GOPA970728H6A',NULL,NULL,'8126132158',NULL,'alvaro.gomez@consulthink.com',NULL,'Mar de Java 201A',NULL,NULL,'Santa María del Granjeno','León',NULL,NULL,'México','2026-02-05 04:24:43','2026-02-05 04:24:43'),(7,'Carlos','Hernández','Mendoza',NULL,NULL,NULL,NULL,'555-123-4567','555-987-6543','carlos@cueroexpress.com',NULL,'Av. Cuero','123',NULL,'Centro','León','Guanajuato','37000','México','2026-02-05 18:15:24','2026-02-05 18:15:24'),(8,'María','García','López',NULL,NULL,NULL,NULL,'477-234-5678','477-876-5432','maria@zapateria.mx',NULL,'Calle Zapato','456',NULL,'Industrial','Guadalajara','Jalisco','44100','México','2026-02-05 18:15:24','2026-02-05 18:15:24'),(9,'Roberto','Martínez','Sánchez',NULL,NULL,NULL,NULL,'33-345-6789','33-765-4321','roberto@insumoscalzado.com',NULL,'Boulevard Suela','789',NULL,'La Joya','Zapopan','Jalisco','45040','México','2026-02-05 18:15:24','2026-02-05 18:15:24'),(10,'Ana','Rodríguez','Pérez',NULL,NULL,NULL,NULL,'442-456-7890','442-654-3210','ana@marroquineria.com.mx',NULL,'Calle Piel','321',NULL,'Los Laureles','San Francisco del Rincón','Guanajuato','36450','México','2026-02-05 18:15:24','2026-02-05 18:15:24'),(11,'Atorbastatina','PRUEBA','PÉREZ',NULL,NULL,NULL,NULL,'8126132158',NULL,'79206@alumnos.utleon.edu.mx','048366F9-B66F-4ED3-AF34-6C0416F4A631_de_tamano_grande.jpeg','',NULL,NULL,'',NULL,NULL,'','México','2026-02-05 21:29:07','2026-02-05 21:58:20'),(12,'Celebrex','HERNANDEZ','PÉREZ',NULL,NULL,NULL,NULL,'8126132158',NULL,'alvaro.gomez@consulthink.com','048366F9-B66F-4ED3-AF34-6C0416F4A631_de_tamano_grande.jpeg',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'México','2026-02-06 16:11:52','2026-02-06 16:11:52');

UNLOCK TABLES;


DROP TABLE IF EXISTS `producto_materia_prima`;
CREATE TABLE `producto_materia_prima` (
  `producto_terminado_id` int NOT NULL,
  `materia_prima_id` int NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `unidad` enum('kg','lt','mt','pza','caja') DEFAULT 'pza',
  PRIMARY KEY (`producto_terminado_id`,`materia_prima_id`),
  KEY `fk_ptmp_mp` (`materia_prima_id`),
  CONSTRAINT `fk_ptmp_mp` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `fk_ptmp_producto` FOREIGN KEY (`producto_terminado_id`) REFERENCES `productos_terminados` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `producto_materia_prima` WRITE;
INSERT INTO `producto_materia_prima` VALUES (1,1,0.80,'kg'),(1,3,1.00,'pza'),(1,6,0.10,'caja'),(2,1,0.30,'kg'),(2,5,1.00,'pza'),(3,1,0.70,'kg'),(3,2,0.40,'mt'),(3,4,1.00,'pza'),(4,1,0.20,'kg'),(4,5,1.00,'pza');
UNLOCK TABLES;


DROP TABLE IF EXISTS `productos_terminados`;
CREATE TABLE `productos_terminados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo_sku` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `precio_venta` decimal(10,2) NOT NULL,
  `cantidad_stock` int DEFAULT '0',
  `lote_produccion` varchar(50) DEFAULT NULL,
  `fecha_fabricacion` date DEFAULT NULL,
  `foto_path` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo_sku` (`codigo_sku`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `productos_terminados` WRITE;
INSERT INTO `productos_terminados` VALUES (1,'PT001','Botín cowboy cuero','Botín estilo cowboy en cuero natural, suela de hule',1200.00,25,'LOTE-BOT-2024-01','2024-01-15',NULL,'2026-02-05 18:18:17'),(2,'PT002','Cartera ejecutiva negra','Cartera de cuero negro con múltiples compartimentos',450.00,40,'LOTE-CAR-2024-02','2024-02-10',NULL,'2026-02-05 18:18:17'),(3,'PT003','Zapato formal oxford','Zapato formal tipo oxford en color negro, suela de cuero',950.00,30,'LOTE-OXF-2024-03','2024-03-05',NULL,'2026-02-05 18:18:17'),(4,'PT004','Cinturón reversible café/negro','Cinturón reversible de cuero genuino, hebilla intercambiable',280.00,60,'LOTE-CIN-2024-04','2024-01-28',NULL,'2026-02-05 18:18:17'),(5,'22000955','BLUE CHANNEL','',456.00,4,'22000955','2000-12-12','048366F9-B66F-4ED3-AF34-6C0416F4A631_de_tamano_grande.jpeg','2026-02-05 18:54:21');
UNLOCK TABLES;



DROP TABLE IF EXISTS `proveedor`;
CREATE TABLE `proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `persona_id` int NOT NULL,
  `nombre_empresa` varchar(150) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `persona_id` (`persona_id`),
  CONSTRAINT `fk_proveedor_persona` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `proveedor` WRITE;
INSERT INTO `proveedor` VALUES (1,5,'Curvados León','2026-02-05 04:24:43'),(2,7,'Cuero Express de México','2026-02-05 18:16:55'),(3,8,'Zapatería y Marroquinería García','2026-02-05 18:16:55'),(4,9,'Insumos para Calzado Martínez','2026-02-05 18:16:55'),(5,10,'Marroquinería y Accesorios Rodríguez','2026-02-05 18:16:55');
UNLOCK TABLES;


DROP TABLE IF EXISTS `proveedor_materia_prima`;
CREATE TABLE `proveedor_materia_prima` (
  `proveedor_id` int NOT NULL,
  `materia_prima_id` int NOT NULL,
  `costo_unitario` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`proveedor_id`,`materia_prima_id`),
  KEY `fk_pmp_mp` (`materia_prima_id`),
  CONSTRAINT `fk_pmp_mp` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `fk_pmp_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `proveedor_materia_prima` WRITE;
INSERT INTO `proveedor_materia_prima` VALUES (1,1,440.00),(1,7,270.00),(1,10,123.00),(2,2,82.00),(2,3,115.00),(3,4,60.00),(3,8,145.00),(4,5,8.00),(4,6,310.00),(4,9,0.80);
UNLOCK TABLES;



DROP TABLE IF EXISTS `token_blacklist`;
CREATE TABLE `token_blacklist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `token` varchar(512) NOT NULL,
  `revoked_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_token_user` (`user_id`),
  CONSTRAINT `fk_token_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `token_blacklist` WRITE;
INSERT INTO `token_blacklist` VALUES (1,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDIzMzk4N30.BD0CS-YOZsBrumNBWgawGaeiKutUTf0YO_JKA2n33Oo','2026-02-04 19:09:48'),(2,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDIzODcxMX0.CqPr8rp3u-ltUXyU3uWv47L4OlhEHYIxyApp6KYsMKI','2026-02-04 20:37:19'),(3,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAyNTY2Mzh9.3BSnHiGu5urFuIbIfuqizT7DK-sn9AKUQvJ8j1230hA','2026-02-05 00:57:28'),(4,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDI1NjY5NH0.MPDfh4L1RSXk1yqlaPddL7e-OVCWlFtiKud2pCdqOhM','2026-02-05 00:58:21'),(5,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAyNTY3MTl9.4PRe1mr3AnI4BKz95s3vlDDB6ENKTdIzYnuEy5PhcGE','2026-02-05 00:59:49'),(6,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAyNTcwNTR9.t3p2_-e5jw0Nr0TzmKK5kwIQ_qaykAIVBDxhzq4w0n4','2026-02-05 01:04:25'),(7,2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAyNTczNjN9.oj8qW90RHbrFV3gNETYYRFONmQU5ttqMaaV3llqFHg0','2026-02-05 01:09:34'),(8,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAyNjcwOTl9.XDtWbvIG7HMV46zmmoli2QUtZzXXTpbzAbUV9OALKM4','2026-02-05 03:52:33'),(9,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAyNjcxNjN9.NrbY3WTDR5-J_ptxKMgfOh71_Xf6aTBwnhTfVZPR550','2026-02-05 03:59:38'),(10,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAyNjc4Mzd9.xVQwsHlLYKXwzUYdJP5r_XJaztI27D46ncuz-8W_IFc','2026-02-05 04:35:22'),(11,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAyNjk3MzJ9.kzkvsjuyxlPRWZkETbt7FkmIsXCludq85KQ5HZRRrxo','2026-02-05 04:48:10'),(12,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMTA4NTh9.H8Zv-hqxjUQV7woJ51TFP6vBbxZR0qukbXd4Qahyfw8','2026-02-05 16:37:34'),(13,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMTM1NDl9.FK5RbQYb-jAC8dsn_Eis4iaipQ1-XJ8XH1-kcuzobI0','2026-02-05 17:04:50'),(14,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMTY0Nzd9.ErJN8FVK4FoKeRS61bS5TUJjit_cVLU3wtmdQsWueVc','2026-02-05 18:30:54'),(15,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMTk4NjF9.GBAH_-rV_ofQ7EAP2XonolZU_fu-pOLJT8JEPIipc2s','2026-02-05 18:54:46'),(16,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMjIzNjJ9.122daeJCCUxuCjZVq0OlX3Kj0jIb9qSyHnExlrn_vQE','2026-02-05 19:58:29'),(17,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMzA1MTl9.8yxOOp8Vp7nn984GXUoIR0uwbO3FxYOY9v7hc0MKQbg','2026-02-05 21:29:51'),(18,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMzA3Nzl9.Og87BD5XU3OyITQCLFRYiBbJSMTO320CiU-4n5jdN14','2026-02-05 21:43:49'),(19,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMzE1NDF9.FebMSLl-DPmwN1azoAAY3K2mbg1LywYOJ5NkCm4XrVI','2026-02-05 21:58:27'),(20,6,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo2LCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMzIzMTN9.rTiWUD_mkX4Axn2zD9lyYIgduwZO4a3h7IzgBPZ6_Xo','2026-02-05 21:59:20'),(21,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMzI0MDB9.K80HmKj0Vjep4UE3Du_qFlZC-l2OEidzkPYfRmImK8o','2026-02-05 22:05:42'),(22,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzMzMwNDB9.zwXzlp7Ae26R5guiW4RchELKJOBpGoyZTEi1qIbgZAs','2026-02-05 22:17:06'),(23,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzOTQ1NzZ9.WucyVa7VMJcMXsABvoCrZ32WR8IHkNZCyy1WUlHGaCE','2026-02-06 15:35:29'),(24,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzOTU3NDF9.nujDEBPDWh574vZuuBS5oa3FCeb9KtpLoHg95rfMKPc','2026-02-06 15:35:48'),(25,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzOTY5NDh9.n2KUwq_NAXTJN75urFKb8Untwdw9tqcVk8UB7zXdtYY','2026-02-06 15:55:58'),(26,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzOTcxODZ9.bp4GtQMqHo7rMG1fo31jiSBTairP_pjo-gSYxDaLIno','2026-02-06 15:59:55'),(27,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzOTc4Nzd9.2WpQM-_wO188lrEqoolfuYfl9_XvzCNbWv5Uza1ciO4','2026-02-06 16:12:10'),(28,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDM5Nzk0Mn0.GhGn4csPgiypSkyYkbe0v5EQK2Oer_tgv2QWUjp21LM','2026-02-06 16:12:31'),(29,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDM5Nzk0Mn0.GhGn4csPgiypSkyYkbe0v5EQK2Oer_tgv2QWUjp21LM','2026-02-06 16:12:32'),(30,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDM5Nzk0Mn0.GhGn4csPgiypSkyYkbe0v5EQK2Oer_tgv2QWUjp21LM','2026-02-06 16:12:33'),(31,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDM5Nzk0Mn0.GhGn4csPgiypSkyYkbe0v5EQK2Oer_tgv2QWUjp21LM','2026-02-06 16:12:33'),(32,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDM5Nzk0Mn0.GhGn4csPgiypSkyYkbe0v5EQK2Oer_tgv2QWUjp21LM','2026-02-06 16:12:33'),(33,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDM5Nzk0Mn0.GhGn4csPgiypSkyYkbe0v5EQK2Oer_tgv2QWUjp21LM','2026-02-06 16:12:34'),(34,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDM5Nzk0Mn0.GhGn4csPgiypSkyYkbe0v5EQK2Oer_tgv2QWUjp21LM','2026-02-06 16:12:34'),(35,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzAzOTgxMTR9.Tv_rzgmdtZsjDlapSsySn1kW0FCSf5hi6gcGtxrugA4','2026-02-06 16:50:50'),(36,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzA0MDA5NTl9.4MN1h4ngKFRrTcDMMPGl7dClyWFG7mmcD2-af9Te5Do','2026-02-06 17:08:14'),(37,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDQwNDIzNX0.zT9iQz8GLrYg9gnYW_yzTxr3tHN_lPxCqFe68GucsQE','2026-02-06 18:07:32'),(38,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDQwNDkxNH0.-UqohE13Vop44csuijEVMuE_Lc9iLbQCAWHqm-8Wrgw','2026-02-06 18:08:44'),(39,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzA0MDQ5NDJ9.bu6pEgzUbut0eQpu1dgQMVkJUWJh7pzG2p3_3-OA5Fs','2026-02-06 18:09:15'),(40,1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJleHAiOjE3NzA0MDgzNzl9.onsKBcGKI6V07p02ehGrQLc7EfYeV8S9CEJclxaVU-c','2026-02-06 19:06:30'),(41,7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJyb2xlIjoidXNlciIsImV4cCI6MTc3MDQwODQwMH0.MZaeQ-QtOzfeMdL_nGXS17j5rVh5w1hpDUBX1mq32L0','2026-02-06 19:06:49');
UNLOCK TABLES;



DROP TABLE IF EXISTS `users`;*/;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user','client') DEFAULT 'client',
  `persona_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `fk_users_persona` (`persona_id`),
  CONSTRAINT `fk_users_persona` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


LOCK TABLES `users` WRITE;
INSERT INTO `users` VALUES (1,'alvaroivan1@icloud.com','$2b$12$GiarWtrDZLHj/WqveowdHeyK1gGjPmjBnmE0Wot32SAvSdiRlqsPG','admin',1,'2026-02-04 19:09:38'),(2,'alvaro@consulthink.mx','$2b$12$EtUAUQvObytaTDChjAMQD.8zKFktGX7EfpSEexpCmLNjpxSoXKVde','admin',2,'2026-02-05 00:55:32'),(6,'79206@alumnos.utleon.edu.mx','$2b$12$zqkMXt58wS4qwQYb90T9qeMvjyTa66HcyonLY6SnQSvRBldKn6HAa','admin',11,'2026-02-05 21:29:07'),(7,'alvaro.gomez@consulthink.com','$2b$12$ET1NFbcv9nB58.VqE3Nqi.7uju.aaxlyxuXsXHwu7amkxsAeI048q','user',12,'2026-02-06 16:11:52');
UNLOCK TABLES;
