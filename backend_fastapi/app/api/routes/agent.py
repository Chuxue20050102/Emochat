import time

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import schemas
from app.agent import agent_service
from app.core.database import get_db
from app.core.response import success_resp
from services.ai.utils import safe_print

router = APIRouter(prefix="/api/agent", tags=["5. Agent"])


@router.post("/run")
def run_agent(req: schemas.AgentRunRequest, db: Session = Depends(get_db)):
    started_at = time.perf_counter()
    payload = agent_service.run_agent(req, db)
    elapsed_ms = int((time.perf_counter() - started_at) * 1000)
    safe_print(
        f"[Agent Run Timing] user_id={req.user_id}, intent={payload.get('intent')}, elapsed_ms={elapsed_ms}"
    )
    return success_resp(data=payload)


@router.get("/traces")
def get_agent_traces(
    user_id: int = Query(..., description="User ID"),
    limit: int = Query(20, ge=1, le=100, description="Trace limit"),
    db: Session = Depends(get_db),
):
    payload = agent_service.get_agent_traces(user_id, limit, db)
    return success_resp(data=payload)
