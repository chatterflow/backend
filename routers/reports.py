from fastapi import HTTPException, APIRouter
from core.schemas.reportSchema import reportProblem
from core.database.reportsdb import db
from datetime import *

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Work in progress"}


@router.get("/{id}")
async def get_reports_by_id(id: str):
    message = db.get(id)
    if message:
        return message
    raise HTTPException(status_code=404, detail="Reports not found")


@router.post("/send_first_report")
async def send_first_report(sender_id: str, receiver_id: str, reportData: reportProblem):
    nThread = {
        "receiver_id": receiver_id,
        "reports": [
            {
                "title": reportData.title,
                "description": reportData.description,
                "date": datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),
                "sender_id": sender_id,
            }
        ]
    }
    db.insert(nThread)
    return {'message': 'Report sent sucessfully'}

# Append report
@router.post("/send_report")
async def send_report(report_thread_id: str, sender_id: str, reportData: reportProblem):
    report = db.fetch({"key": report_thread_id})
    if not report.items:
        raise HTTPException(status_code=404, detail="Report not found")
    report_doc = {
        "title": reportData.title,
        "description": reportData.description,
        "date": datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S"),
        "sender_id": sender_id,
    }
    append_report = {'reports': db.util.append(report_doc)}
    for i in report.items:
        key = i['key']
    db.update(append_report, key=key)
    return {'message': 'Report sent successfully'}
