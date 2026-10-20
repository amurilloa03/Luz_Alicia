from pydantic import BaseModel, Field


class DatosFactura(BaseModel):
    titular: str = Field(min_length=2, max_length=50, description="Nombre del titular del contrato")
    potencia_kw: float = Field(ge=1, le=15, description="Potencia contratada en kW (entre 1 y 15)")
    consumo_kwh: float = Field(ge=0, le=5000, description="Energía consumida en el periodo en kWh")
    dias: int = Field(ge=1, le=62, description="Días del periodo de facturación (entre 1 y 62)")
    discriminacion_horaria: bool = Field(default=False, description="¿Consume sobre todo en horas valle?")
    bono_social: bool = Field(default=False, description="¿Tiene derecho al bono social?")


class ResultadoFactura(BaseModel):
    titular: str
    nivel_consumo: str
    importe_total: float
    consumo_medio_diario: float
    termino_potencia: float
    termino_energia: float
    impuestos: float
    mensaje: str
