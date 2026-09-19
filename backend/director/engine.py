class DirectorEngine:
    def build_scene_manifest(self,brief:dict)->dict:
        return {'schema_version':'4.1','scenes':[],'inputs':brief}
