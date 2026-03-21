from project.extensions import db
from models import FichaTecnica, FichaTecnicaInsumos, FichaTecnicaProcesos, ProductoTerminado


class FichaTecnicaRepository:

    @staticmethod
    def get_all():
        return FichaTecnica.query.order_by(FichaTecnica.fecha_alta.desc()).all()

    @staticmethod
    def clonar_ficha(id_ficha_origen, id_pt_destino, id_usuario_actual):
        try:
            # toma ficha madre (base)
            ficha_origen = FichaTecnica.query.get(id_ficha_origen)
            if not ficha_origen:
                return False

            # nuevo encabezafo
            nueva_ficha = FichaTecnica(
                id_pt=id_pt_destino,
                costo_produccion=ficha_origen.costo_produccion,
                id_usuario=id_usuario_actual
            )

            db.session.add(nueva_ficha)

            # guarda solo encabezado ficha tec
            db.session.flush()

            # clon de materiales insumo
            for insumo in ficha_origen.insumos:
                nuevo_insumo = FichaTecnicaInsumos(
                    id_ficha_tecnica=nueva_ficha.id_ficha_tecnica,
                    id_mp=insumo.id_mp,
                    etapa=insumo.etapa,
                    cantidad_requerida=insumo.cantidad_requerida,
                    observacion_material=insumo.observacion_material
                )
                db.session.add(nuevo_insumo)
            # clon de proceso
            for proceso in ficha_origen.procesos:
                nuevo_proceso = FichaTecnicaProcesos(
                    id_ficha_tecnica=nueva_ficha.id_ficha_tecnica,
                    etapa=proceso.etapa,
                    descripcion_instruccion=proceso.descripcion_instruccion,
                    maquinaria_sugerida=proceso.maquinaria_sugerida,
                    observaciones_seguridad=proceso.observaciones_seguridad
                )
                db.session.add(nuevo_proceso)

            # ligamos a punto (prod con talla)
            pt_destino = ProductoTerminado.query.get(id_pt_destino)
            if pt_destino:
                pt_destino.id_ficha_tecnica = nueva_ficha.id_ficha_tecnica
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error al clonar Ficha Técnica: {e}")
            return False

    @staticmethod
    def actualizar_costo_total(id_ficha):
        try:
            ficha = FichaTecnica.query.get(id_ficha)
            if not ficha:
                return False

            nuevo_costo = 0.00
            for insumo in ficha.insumos:
                precio_mp = insumo.materia_prima_rel.costo_unitario
                nuevo_costo += float(insumo.cantidad_requerida) * float(precio_mp)

            ficha.costo_produccion = nuevo_costo
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error al calcular costo: {e}")
            return False