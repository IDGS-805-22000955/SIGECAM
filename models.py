from project.extensions import db
from datetime import datetime


class MateriaPrima(db.Model):
    __tablename__ = 'Materia_Prima'
    id_mp = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidad_medida = db.Column(db.Enum('Gramos', 'Metros', 'Piezas'), nullable=False)
    porcentaje_merma = db.Column(db.Numeric(5, 2), nullable=False, default=0.00)
    stock_actual = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    stock_minimo = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)


class ModeloZapato(db.Model):
    __tablename__ = 'Modelo_Zapato'
    id_modelo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_modelo = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    foto_modelo = db.Column(db.String(255), nullable=True)


class Proveedor(db.Model):
    __tablename__ = 'Proveedor'
    id_proveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    razon_social = db.Column(db.String(150), nullable=False)
    rfc = db.Column(db.String(20), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)


class Cliente(db.Model):
    __tablename__ = 'Cliente'
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    rfc_datos = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)


class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_usuario = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('Admin', 'Ventas', 'Producción', 'Sistemas'), nullable=False)
    intentos_fallidos = db.Column(db.Integer, nullable=False, default=0)
    ultimo_acceso = db.Column(db.DateTime, nullable=True)


class Empleado(db.Model):
    __tablename__ = 'Empleados'
    id_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    codigo_gafete = db.Column(db.String(50), nullable=False, unique=True)
    estacion_asignada = db.Column(db.Enum('Cortado', 'Doblillado', 'Pespunte', 'Montado', 'Adornado'), nullable=False)
    estatus = db.Column(db.Boolean, nullable=False, default=True)


class ProductoTerminado(db.Model):
    __tablename__ = 'Producto_Terminado'
    id_pt = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_modelo = db.Column(db.Integer, db.ForeignKey('Modelo_Zapato.id_modelo', ondelete='RESTRICT'), nullable=False)
    talla = db.Column(db.Numeric(4, 1), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock_disponible = db.Column(db.Integer, nullable=False, default=0)

    id_ficha_tecnica = db.Column(db.Integer, db.ForeignKey('Ficha_Tecnica.id_ficha_tecnica', ondelete='SET NULL'),
                                 nullable=True)
    ficha_tecnica_rel = db.relationship('FichaTecnica', foreign_keys=[id_ficha_tecnica], post_update=True)


class FichaTecnica(db.Model):
    __tablename__ = 'Ficha_Tecnica'
    id_ficha_tecnica = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pt = db.Column(db.Integer, db.ForeignKey('Producto_Terminado.id_pt', ondelete='CASCADE'), nullable=False)
    costo_produccion = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)


class BitacoraSistema(db.Model):
    __tablename__ = 'Bitacora_Sistema'
    id_log = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='SET NULL'), nullable=True)
    nivel_evento = db.Column(db.Enum('Informativo', 'Advertencia', 'Crítico', 'Error'), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class TokenSeguridad(db.Model):
    __tablename__ = 'Tokens_Seguridad'
    id_token = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='CASCADE'), nullable=False)
    token_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum('2FA', 'Recuperacion'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_expiracion = db.Column(db.DateTime, nullable=False)
    usado = db.Column(db.Boolean, nullable=False, default=False)


class BackupHistorial(db.Model):
    __tablename__ = 'Backups_Historial'
    id_backup = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='RESTRICT'), nullable=False)
    fecha_generacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ruta_archivo = db.Column(db.String(255), nullable=False)
    tamano_mb = db.Column(db.Numeric(8, 2), nullable=False)
    estatus = db.Column(db.Enum('Exitoso', 'Fallido'), nullable=False)


class Compra(db.Model):
    __tablename__ = 'Compras'
    id_compra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('Proveedor.id_proveedor', ondelete='RESTRICT'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='RESTRICT'), nullable=False)
    fecha_compra = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_compra = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)


class Pedido(db.Model):
    __tablename__ = 'Pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('Cliente.id_cliente', ondelete='RESTRICT'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='RESTRICT'), nullable=False)
    fecha_pedido = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    estado_pedido = db.Column(db.Enum('Pendiente', 'En Producción', 'Terminado', 'Entregado'), nullable=False,
                              default='Pendiente')


class Venta(db.Model):
    __tablename__ = 'Ventas'
    id_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='SET NULL'), nullable=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('Cliente.id_cliente', ondelete='SET NULL'), nullable=True)
    fecha_venta = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_venta = db.Column(db.Numeric(10, 2), nullable=False)
    origen_venta = db.Column(db.Enum('Mostrador', 'E-commerce'), nullable=False)
    id_transaccion_stripe = db.Column(db.String(100), nullable=True)


class CorteCaja(db.Model):
    __tablename__ = 'Corte_Caja'
    id_corte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='RESTRICT'), nullable=False)
    fecha_apertura = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime, nullable=True)
    saldo_inicial = db.Column(db.Numeric(10, 2), nullable=False)
    total_ingresos_efectivo = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    total_salidas_efectivo = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    saldo_final_esperado = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)


class OrdenProduccion(db.Model):
    __tablename__ = 'Orden_Produccion'
    id_op = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pt = db.Column(db.Integer, db.ForeignKey('Producto_Terminado.id_pt', ondelete='RESTRICT'), nullable=False)
    cantidad_pares = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    estado_actual = db.Column(
        db.Enum('Pendiente', 'Por Asignar', 'Cortado', 'Doblillado', 'Pespunte', 'Montado', 'Adornado', 'Terminado',
                'Cancelado'), nullable=False, default='Pendiente')


class DetalleFichaTecnica(db.Model):
    __tablename__ = 'Detalle_Ficha_Tecnica'
    id_detalle_ft = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_ficha_tecnica = db.Column(db.Integer, db.ForeignKey('Ficha_Tecnica.id_ficha_tecnica', ondelete='CASCADE'),
                                 nullable=False)
    id_mp = db.Column(db.Integer, db.ForeignKey('Materia_Prima.id_mp', ondelete='RESTRICT'), nullable=False)
    cantidad_requerida = db.Column(db.Numeric(10, 2), nullable=False)


class DetalleCompra(db.Model):
    __tablename__ = 'Detalle_Compra'
    id_detalle_compra = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_compra = db.Column(db.Integer, db.ForeignKey('Compras.id_compra', ondelete='CASCADE'), nullable=False)
    id_mp = db.Column(db.Integer, db.ForeignKey('Materia_Prima.id_mp', ondelete='RESTRICT'), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    costo_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)


class DetallePedido(db.Model):
    __tablename__ = 'Detalle_Pedido'
    id_detalle_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('Pedidos.id_pedido', ondelete='CASCADE'), nullable=False)
    id_pt = db.Column(db.Integer, db.ForeignKey('Producto_Terminado.id_pt', ondelete='RESTRICT'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)


class DetalleVenta(db.Model):
    __tablename__ = 'Detalle_Venta'
    id_detalle_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('Ventas.id_venta', ondelete='CASCADE'), nullable=False)
    id_pt = db.Column(db.Integer, db.ForeignKey('Producto_Terminado.id_pt', ondelete='RESTRICT'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_venta_historico = db.Column(db.Numeric(10, 2), nullable=False)
    costo_produccion_historico = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)


class SalidaEfectivo(db.Model):
    __tablename__ = 'Salida_Efectivo'
    id_salida = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_corte = db.Column(db.Integer, db.ForeignKey('Corte_Caja.id_corte', ondelete='CASCADE'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='RESTRICT'), nullable=False)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('Proveedor.id_proveedor', ondelete='SET NULL'), nullable=True)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    concepto = db.Column(db.String(255), nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class AutorizacionMerma(db.Model):
    __tablename__ = 'Autorizacion_Mermas'
    id_merma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_op = db.Column(db.Integer, db.ForeignKey('Orden_Produccion.id_op', ondelete='RESTRICT'), nullable=False)
    id_mp = db.Column(db.Integer, db.ForeignKey('Materia_Prima.id_mp', ondelete='RESTRICT'), nullable=False)
    id_empleado = db.Column(db.Integer, db.ForeignKey('Empleados.id_empleado', ondelete='RESTRICT'), nullable=False)
    id_usuario_admin = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='SET NULL'), nullable=True)
    cantidad_merma = db.Column(db.Numeric(10, 2), nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    estatus = db.Column(db.Enum('Pendiente', 'Autorizada', 'Rechazada'), nullable=False, default='Pendiente')


class Kardex(db.Model):
    __tablename__ = 'Kardex'
    id_kardex = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_movimiento = db.Column(db.Enum('Entrada', 'Salida'), nullable=False)
    id_mp = db.Column(db.Integer, db.ForeignKey('Materia_Prima.id_mp', ondelete='RESTRICT'), nullable=True)
    id_pt = db.Column(db.Integer, db.ForeignKey('Producto_Terminado.id_pt', ondelete='RESTRICT'), nullable=True)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_movimiento = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario', ondelete='RESTRICT'), nullable=False)