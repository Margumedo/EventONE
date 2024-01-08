from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Comment
from typing import List
from app.schemas.schemas import ShowComment, CommentBase, UpdateComment
from app.db.database import get_async_session

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.get("/", response_model=List[ShowComment], status_code=200)
async def get_comments(db: AsyncSession = Depends(get_async_session)):
    query = select(Comment)
    query_result = await db.scalars(query)
    result = query_result.all()

    return result

@router.get("/{comment_id}", response_model=ShowComment, status_code=200)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(Comment).where(Comment.id == comment_id)
    query_result = await db.scalars(query)
    result = query_result.first()

    if not result:
        raise HTTPException(status_code=404, detail="Comment not found")

    return result

@router.post("/", response_model=ShowComment, status_code=201)
async def create_comment(comment: CommentBase, db: AsyncSession=Depends(get_async_session)):
    new_comment = Comment(
        content = comment.content.model_dump(),
        user_id = comment.user_id,
        event_id = comment.event_id
    ) 

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

@router.patch("/{comment_id}", response_model=ShowComment, status_code=202)
async def update_commet(comment_id: int, comment: UpdateComment, db: AsyncSession = Depends(get_async_session)):
    query = select(Comment).where(Comment.id == comment_id)
    query_result = await db.scalars(query)
    result = query_result.first()

    if not result:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    for key, value in comment.model_dump().items():
        if value is not None:
            #valido si el valor es serializable, es decir, lo convierto en un diccionario
            print("Entre aqui")
            setattr(result, key, value.model_dump() if hasattr(value, "model_dump") else value) 
        

    await db.commit()
    await db.refresh(result)
    return result

@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(Comment).where(Comment.id == comment_id)
    query_result = await db.scalars(query)
    result = query_result.first()

    if not result:
        raise HTTPException(status_code=404, detail="Comment not found")
    

    await db.delete(result)
    await db.commit()   
    return result