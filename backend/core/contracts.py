from pydantic import BaseModel,Field
class AudioAnalysis(BaseModel):
    duration:float|None=None
    bpm:float|None=None
    beats:list[float]=Field(default_factory=list)
    downbeats:list[float]=Field(default_factory=list)
    sections:list[dict]=Field(default_factory=list)
    onsets:list[float]=Field(default_factory=list)
    lyrics:list[dict]=Field(default_factory=list)
    energy_curve:list[float]=Field(default_factory=list)
class RenderRequest(BaseModel):
    project_id:str;scene_id:str;asset_versions:list[str]=Field(default_factory=list);model:str='provider-neutral';params:dict=Field(default_factory=dict);prompt:str='';seed:int|None=None
