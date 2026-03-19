from typing import Any

def success_resp(data: Any = None, msg: str = "ok"):
    return {"code": 200, "data": data, "msg": msg}

def error_resp(code: int = 400, msg: str = "error"):
    return {"code": code, "data": None, "msg": msg}
