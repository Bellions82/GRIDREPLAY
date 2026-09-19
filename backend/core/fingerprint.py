import hashlib,json
def render_fingerprint(payload:dict)->str:
    canonical=json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    return hashlib.sha256(canonical).hexdigest()
