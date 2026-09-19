from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.core.config import settings
app=FastAPI(title='VideoForge API',version='4.1.0')
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(router,prefix='/api/v1')
@app.get('/api/v1/health')
async def health(): return {'status':'ok','service':'videoforge-api','version':'4.1.0'}
@app.get('/api/v1/ready')
async def ready(): return {'status':'ready'}
