# ⚡ Simulador de Factura de la Luz

**Autor:** Alejandro Murillo  
**Actividad:** AS1 – API REST con FastAPI (Parte 1 y Parte 2)

## URL pública

- **Aplicación web:** https://NOMBRE-DEL-SERVICIO.onrender.com
- **Documentación Swagger:** https://NOMBRE-DEL-SERVICIO.onrender.com/docs

> Desplegado en el plan gratuito de Render. Si el servicio lleva un rato sin usarse, la primera carga puede tardar alrededor de un minuto.

## Descripción

Aplicación web con una API REST hecha en **FastAPI** que estima el importe de una factura eléctrica doméstica.

El usuario introduce el titular, la potencia contratada, el consumo en kWh, los días del periodo y si tiene discriminación horaria o bono social. La API valida los datos con **Pydantic** y devuelve:

- El importe total estimado (término de potencia, término de energía, impuesto eléctrico, alquiler del contador e IVA).
- El consumo medio diario.
- Una clasificación del consumo (Bajo / Medio / Alto) con un consejo de ahorro.

**Problema que resuelve:** saber cuánto va a costar la factura antes de que llegue y si el consumo del hogar es razonable.

## Estructura del proyecto

```
├── static/
│   └── app.js          # Frontend: envía el formulario a la API con fetch()
├── app.py              # Servidor FastAPI, CORS y endpoints
├── schemas.py          # Modelos Pydantic de entrada y salida
├── logica.py           # Motor de cálculo (simula el modelo de IA)
├── index.html          # Formulario web
└── requirements.txt    # Dependencias
```

## Endpoints

| Método | Ruta | Descripción |
| ------ | ---- | ----------- |
| GET | `/` | Página web del simulador |
| GET | `/api/info` | Estado del servicio |
| POST | `/api/calcular-factura` | Cálculo de la factura |
| GET | `/docs` | Documentación Swagger UI |

## Qué he hecho

### 1. Arquitectura modular

He separado el backend en tres ficheros, cada uno con una única responsabilidad:

- `schemas.py` define **qué datos** entran y salen.
- `logica.py` decide **cómo se calcula** el resultado.
- `app.py` solo **recibe las peticiones** y llama a la lógica.

Así, si en el futuro se sustituye el cálculo por un modelo de Machine Learning real, solo habría que cambiar `logica.py`. La API y el frontend se quedarían igual.

### 2. Validación con Pydantic

**Esquema de entrada (`DatosFactura`):**

| Campo | Tipo | Restricción | Obligatorio |
| ----- | ---- | ----------- | ----------- |
| `titular` | texto | entre 2 y 50 caracteres | Sí |
| `potencia_kw` | decimal | entre 1 y 15 kW | Sí |
| `consumo_kwh` | decimal | entre 0 y 5000 kWh | Sí |
| `dias` | entero | entre 1 y 62 días | Sí |
| `discriminacion_horaria` | booleano | — | No (por defecto `false`) |
| `bono_social` | booleano | — | No (por defecto `false`) |

Todos los campos tienen descripción con `Field`, por lo que aparecen documentados en Swagger. Si se envía un dato fuera de rango (por ejemplo, una potencia de 40 kW), FastAPI responde automáticamente con un **error 422** y no se ejecuta el cálculo.

**Esquema de salida (`ResultadoFactura`):**
- Veredicto: `nivel_consumo` (Bajo / Medio / Alto).
- Métrica principal: `importe_total` en euros.
- Desglose: `termino_potencia`, `termino_energia`, `impuestos` y `consumo_medio_diario`.
- Explicación: `mensaje` con un consejo de ahorro.

El endpoint usa `response_model=ResultadoFactura`, así que la respuesta siempre se filtra y se ajusta a este esquema.

### 3. Lógica de inferencia (simulación del modelo)

`logica.py` simula un modelo con reglas y cálculos parecidos a los de una factura real:

1. **Término de potencia** = kW contratados × precio por kW/día × días.
2. **Término de energía** = kWh consumidos × precio del kWh. El precio es más barato con discriminación horaria (0,12 €/kWh en lugar de 0,15 €/kWh).
3. **Bono social**: descuento del 35 % sobre los términos de potencia y energía.
4. **Impuestos**: impuesto eléctrico (5,11 %), alquiler del contador e IVA (21 %).
5. **Clasificación del consumo** según la media diaria:
   - menos de 5 kWh/día → **Bajo**
   - entre 5 y 10 kWh/día → **Medio**
   - más de 10 kWh/día → **Alto**
6. **Recomendación**: si el consumo diario supera los 8 kWh y no tiene discriminación horaria, se le sugiere esa tarifa.

Los precios están definidos como constantes al principio del fichero para poder cambiarlos fácilmente.

### 4. Frontend

- `index.html` contiene el formulario. El diseño está hecho con Tailwind CSS (cargado por CDN).
- `static/app.js` recoge los datos al pulsar el botón y los envía en JSON con `fetch()` y `async/await` a `POST /api/calcular-factura`. Después muestra el resultado en una tarjeta de color: verde (Bajo), amarilla (Medio) o roja (Alto).
- La API tiene **CORS** configurado y FastAPI sirve también el HTML y el JavaScript, así que todo funciona desde una única URL.

### Flujo completo

```
Formulario (index.html)
   → app.js envía JSON con fetch()
   → app.py recibe la petición
   → schemas.py valida los datos (error 422 si no son válidos)
   → logica.py calcula la factura
   → schemas.py filtra la respuesta
   → app.js muestra el resultado
```

## Ejecución en local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Abrir `http://127.0.0.1:8000`.

## Despliegue en Render

1. Subir el proyecto a un repositorio público de GitHub (sin `.venv` ni `__pycache__`, excluidos con `.gitignore`).
2. En Render: **New → Web Service** y seleccionar el repositorio.
3. Configuración:
   - **Language:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
4. Render instala las dependencias, arranca el servidor y genera la URL pública.

Se usa `0.0.0.0` para aceptar conexiones externas y `$PORT` porque es Render quien asigna el puerto.

---

## Extra: despliegue de un modelo de IA en Render (clasificador perros/gatos)

Para comprobar si Render permite desplegar APIs con modelos de IA, se ha desplegado el repositorio del clasificador de imágenes de perros y gatos.

**URL pública:** https://NOMBRE-DEL-CLASIFICADOR.onrender.com

**Resultado:** ✅ Funciona. El modelo carga y clasifica correctamente las imágenes en el plan gratuito.

### Cómo se ha desplegado

1. Descargar el repositorio de Hugging Face, con Git LFS para que se descargue el archivo real del modelo:
   ```bash
   git lfs install
   git clone https://huggingface.co/spaces/acamarac02/perros-gatos-clasificador
   ```
2. Render no puede leer repositorios de Hugging Face, así que se sube a un repositorio propio de GitHub:
   ```bash
   cd perros-gatos-clasificador
   git remote set-url origin https://github.com/amurilloa03/REPO.git
   git push -u origin main
   ```
3. En Render: **New → Web Service** y seleccionar el repositorio. Como el proyecto incluye un `Dockerfile`, Render construye la imagen con Docker e instala las dependencias (FastAPI, TensorFlow, Pillow…).
4. **Instance Type:** Free.
5. **Puerto:** la aplicación arranca en el puerto 7860, el de Hugging Face. Render lo detecta automáticamente y reinicia el despliegue para usarlo. Si no lo detecta, se puede fijar añadiendo la variable de entorno `PORT=7860` en **Environment**.

### Observaciones

- Render gratuito no tiene GPU: TensorFlow muestra el aviso `Could not find cuda drivers... GPU will not be used` y funciona con CPU, que es suficiente para este modelo.
- El modelo cabe en los 512 MB de RAM del plan gratuito.
- La instalación de TensorFlow ocupa unos 570 MB, por lo que el primer build tarda varios minutos.
- Como en cualquier servicio gratuito de Render, tras un rato sin uso el servicio se duerme y la primera petición tarda en responder.

**Conclusión:** Render es una opción válida y gratuita para desplegar en el futuro APIs con modelos de IA ligeros que funcionen en CPU.
