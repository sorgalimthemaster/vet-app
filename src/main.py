import os, sys
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from config.database import get_db_veterinaria
import uvicorn
from controllers.user_controller import router
from fastapi.middleware.cors import CORSMiddleware

description = f"""

    Creado con FastAPI.
    Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}

**Servicio para Veterinaria VetHearth.**
"""

show_docs = os.getenv("DOCS", "False").lower() == "true"

app = FastAPI()

def custom_openapi() -> dict:
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        for method_item in app.openapi_schema.get('paths').values():
            for param in method_item.values():
                responses = param.get('responses')
                if '422' in responses:
                    del responses['422']

    return app.openapi_schema

app = FastAPI(
    title="Vet-Api",
    description=description,
    version="1.0.0",
    openapi_tags="",
    docs_url="/docs" if show_docs else None,
    openapi_url="/openapi.json" if show_docs else None,
    redoc_url="/redoc" if show_docs else None)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.openapi = custom_openapi

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
