"""
题目相关API
"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.problem import Problem
from app.schemas.problem import ProblemCreate, ProblemUpdate, ProblemResponse
from app.api.v1.auth import get_current_user

router = APIRouter()


@router.post("", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
async def create_problem(
    problem_data: ProblemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建题目"""
    db_problem = Problem(
        **problem_data.dict(),
        user_id=current_user.id
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


@router.get("", response_model=List[ProblemResponse])
async def get_problems(
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取题目列表"""
    query = db.query(Problem).filter(Problem.user_id == current_user.id)
    
    if date_from:
        query = query.filter(Problem.date >= date_from)
    if date_to:
        query = query.filter(Problem.date <= date_to)
    
    problems = query.order_by(Problem.date.desc()).offset(skip).limit(limit).all()
    return problems


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(
    problem_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取单个题目"""
    problem = db.query(Problem).filter(
        Problem.id == problem_id,
        Problem.user_id == current_user.id
    ).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    
    return problem


@router.put("/{problem_id}", response_model=ProblemResponse)
async def update_problem(
    problem_id: int,
    problem_data: ProblemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新题目"""
    problem = db.query(Problem).filter(
        Problem.id == problem_id,
        Problem.user_id == current_user.id
    ).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    
    # 更新字段
    update_data = problem_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(problem, field, value)
    
    db.commit()
    db.refresh(problem)
    return problem


@router.delete("/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_problem(
    problem_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除题目"""
    problem = db.query(Problem).filter(
        Problem.id == problem_id,
        Problem.user_id == current_user.id
    ).first()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    
    db.delete(problem)
    db.commit()
    return None


@router.get("/date/{problem_date}", response_model=List[ProblemResponse])
async def get_problems_by_date(
    problem_date: date,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """根据日期获取题目列表"""
    problems = db.query(Problem).filter(
        Problem.user_id == current_user.id,
        Problem.date == problem_date
    ).order_by(Problem.created_at.desc()).all()
    
    return problems

