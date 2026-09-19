from fastapi import APIRouter
from pydantic import BaseModel,Field
from backend.core.fingerprint import render_fingerprint
from backend.core.state import RenderState
router=APIRouter()
class JobRequest(BaseModel):
    project_id:str
    scene_id:str
    asset_versions:list[str]=Field(default_factory=list)
    model:str='provider-neutral'
    params:dict=Field(default_factory=dict)
    prompt:str=''
    seed:int|None=None
@router.post('/render-jobs')
async def create_render_job(req:JobRequest):
    fp=render_fingerprint(req.model_dump())
    return {'job_id':f'job_{fp[:16]}','state':RenderState.CREATED,'fingerprint':fp}
