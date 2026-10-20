from schemas import DatosFactura

PRECIO_POTENCIA_DIA = 0.11
PRECIO_ENERGIA = 0.15
PRECIO_ENERGIA_VALLE = 0.12
IMPUESTO_ELECTRICO = 0.0511
ALQUILER_CONTADOR_DIA = 0.027
IVA = 0.21
DESCUENTO_BONO_SOCIAL = 0.35


def calcular_factura(datos: DatosFactura) -> dict:
    precio_kwh = PRECIO_ENERGIA_VALLE if datos.discriminacion_horaria else PRECIO_ENERGIA

    termino_potencia = datos.potencia_kw * PRECIO_POTENCIA_DIA * datos.dias
    termino_energia = datos.consumo_kwh * precio_kwh
    subtotal = termino_potencia + termino_energia

    if datos.bono_social:
        subtotal = subtotal * (1 - DESCUENTO_BONO_SOCIAL)

    impuesto_electrico = subtotal * IMPUESTO_ELECTRICO
    alquiler = ALQUILER_CONTADOR_DIA * datos.dias
    base_imponible = subtotal + impuesto_electrico + alquiler
    iva = base_imponible * IVA
    total = base_imponible + iva

    consumo_diario = datos.consumo_kwh / datos.dias

    if consumo_diario < 5:
        nivel = "Bajo"
        mensaje = "Consumo eficiente, por debajo de la media de un hogar."
    elif consumo_diario <= 10:
        nivel = "Medio"
        mensaje = "Consumo dentro de la media de un hogar en España."
    else:
        nivel = "Alto"
        mensaje = "Consumo elevado: revisa electrodomésticos y climatización."

    if not datos.discriminacion_horaria and consumo_diario > 8:
        mensaje += " Te podría compensar una tarifa con discriminación horaria."

    return {
        "titular": datos.titular,
        "nivel_consumo": nivel,
        "importe_total": round(total, 2),
        "consumo_medio_diario": round(consumo_diario, 2),
        "termino_potencia": round(termino_potencia, 2),
        "termino_energia": round(termino_energia, 2),
        "impuestos": round(impuesto_electrico + iva, 2),
        "mensaje": mensaje,
    }
