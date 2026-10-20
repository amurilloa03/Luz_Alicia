from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from schemas import DatosFactura, ResultadoFactura
from logica import calcular_factura

app = FastAPI(
    title="Simulador de Factura de la Luz",
    description="API que estima el importe de una factura eléctrica y clasifica el nivel de consumo del hogar",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse, include_in_schema=False)
def inicio():
    return FileResponse("index.html")


@app.get("/api/info", tags=["Información"])
def info():
    """Devuelve el estado del servicio y cómo usarlo."""
    return {
        "servicio": "Simulador de Factura de la Luz",
        "estado": "activo",
        "version": "1.0.0",
        "endpoint_calculo": "POST /api/calcular-factura",
        "documentacion": "/docs",
    }


@app.post("/api/calcular-factura", response_model=ResultadoFactura, tags=["Factura"])
def calcular(datos: DatosFactura):
    """Calcula el importe estimado de la factura y el nivel de consumo."""
    return calcular_factura(datos)
