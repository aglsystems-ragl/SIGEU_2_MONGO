from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.routes.evento_router import router as evento_router
from src.routes.usuario_router import router as usuario_router
from src.routes.facultad_router import router as facultad_router
from src.routes.unidad_academica_router import router as unidad_academica_router
from src.routes.programa_academico_router import router as programa_academico_router
from src.routes.lugar_router import router as lugar_router
from src.routes.organizacion_externa_router import router as organizacion_externa_router



app = FastAPI(
    title="SIGEU_2 API – Sistema de Gestión de Eventos UAO",
    version="1.0.0",
    description=("""
**PROYECTO SISTEMA DE GESTIÓN DE EVENTOS SIGEU**  
**BASE DE DATOS DOCUMENTAL**

**Integrantes del equipo**

- RODRIGO ANDRÉS GÓMEZ LÓPEZ. Código: 2247014  
- DAVID HERNÁNDEZ PAZ. Código: 2247003  
- DANIEL ALEXANDER BRAND GARCÍA. Código: 2246133  
- SEBASTIÁN MANRIQUE MEJIA. Código: 2246988  
- MICHAEL MACOWLI CARDONA RODRIGUEZ. Código: 2246268  

**UNIVERSIDAD AUTÓNOMA DE OCCIDENTE**  
Ingeniería de Datos e Inteligencia Artificial  
Santiago de Cali – 2025
"""),
)



@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# ---------------------
# 💡 CORS
# ---------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(evento_router)
app.include_router(usuario_router)
app.include_router(facultad_router)
app.include_router(unidad_academica_router)
app.include_router(programa_academico_router)
app.include_router(lugar_router)
app.include_router(organizacion_externa_router)
