from fastapi import APIRouter, Depends, HTTPException, status

from datetime import date
from typing import List, Optional

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import ExpenseRequest, ExpenseResponse
from core.sesson import async_session
from models import Expense
from typing import AsyncGenerator

router = APIRouter()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async session for database operations.
    """
    async with async_session() as session:
        yield session

async def expense_add(expense: ExpenseRequest, session: AsyncSession):
    async with session.begin():
        expense_obj = Expense(**expense.dict())
        session.add(expense_obj)
        await session.flush()
        await session.refresh(expense_obj)
        return expense_obj

async def expenses_get(session: AsyncSession):
    async with session.begin():
        result = await session.execute(select(Expense))
        return result.scalars().all()

async def expense_update(id, expense: ExpenseRequest, session: AsyncSession):
    async with session.begin():
        result = await session.get(Expense, id)
        if result:
            for key, val in expense.dict().items():
                setattr(result, key, val)
            await session.commit()
            return result
        else:
            raise HTTPException(status_code=404, detail="expense not found")


async def user_expenses_get(id: int, session: AsyncSession, from_date: Optional[date], to_date: Optional[date]):

    query = select(Expense)
    if from_date:
        query = query.where(Expense.created_at >= from_date)
    if to_date:
        query = query.where(Expense.created_at <= to_date)

    result = await session.execute(query)
    return result.scalars().all()    

@router.post("/add_expense", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def add_expense(expense: ExpenseRequest, session: AsyncSession = Depends(get_session)):

    res = await expense_add(expense, session)
    return res
    

@router.get("/get_expenses", response_model=List[ExpenseResponse])
async def get_expenses(session: AsyncSession = Depends(get_session)):

    res = await expenses_get(session)
    return res
    

@router.put("/update_expense/{id}", response_model=ExpenseResponse, status_code=status.HTTP_200_OK)
async def update_expense(id: int, expense: ExpenseRequest, session: AsyncSession = Depends(get_session)):
    
    res = await expense_update(id, expense, session)
    return res


@router.get("/get_user_expense/{id}", response_model=List[ExpenseResponse])
async def get_user_expenses(
    id: int,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    session: AsyncSession = Depends(get_session)
):
    res = await user_expenses_get(id,  session, from_date, to_date)
    return res

@router.get("/analyze")
async def analyze(id, session: AsyncSession = Depends(get_session)):
    ...