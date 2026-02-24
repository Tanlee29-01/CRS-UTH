from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.notification import Notification


router = APIRouter()


@router.get("/notifications", response_model=list[dict])
def list_notifications(
    db: Session = Depends(get_db), user=Depends(get_current_user)
):
    rows = (
        db.execute(select(Notification).where(Notification.user_id == user.id))
        .scalars()
        .all()
    )
    return [
        {
            "id": n.id,
            "title": n.title,
            "body": n.body,
            "read": n.read,
            "created_at": n.created_at,
        }
        for n in rows
    ]


@router.post("/notifications/{notification_id}/read", response_model=dict)
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    n = (
        db.execute(
            select(Notification).where(
                Notification.id == notification_id, Notification.user_id == user.id
            )
        )
        .scalars()
        .first()
    )
    if not n:
        return {"status": "not_found"}
    n.read = True
    db.commit()
    return {"status": "read"}
