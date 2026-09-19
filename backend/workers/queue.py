class JobQueue:
    def __init__(self,redis_url:str): self.redis_url=redis_url
    async def enqueue(self,job:dict)->str: return job['job_id']
