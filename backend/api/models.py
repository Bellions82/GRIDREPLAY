from pydantic import BaseModel,Field
class ProjectCreate(BaseModel):
    title:str=Field(min_length=1,max_length=200)
    schema_version:str='4.1'
class RenderJobResponse(BaseModel):
    job_id:str
    state:str
    fingerprint:str
