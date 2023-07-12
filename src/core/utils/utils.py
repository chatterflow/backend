from sqlalchemy import select, case, join, Column, exists, or_, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from sqlalchemy.future import select


async def value_exists(db: AsyncSession, model: Any, coluna: Column, valor: Any) -> bool:
    async with db as session:
        consulta = select(exists().where(coluna == valor)).select_from(model)
        resultado = await session.execute(consulta)
        return resultado.scalar()

async def select_value(db: AsyncSession, model: Any, column: Column, value: Any):
    async with db as session:
        query = select(model).filter(column == value)
        result = await session.execute(query)
        resultValue = result.scalars().unique().one_or_none()
        return resultValue

async def select_everything(db: AsyncSession, model: Any):
    async with db as session:
        query = select(model)
        result = await session.execute(query)
        return result.scalars().all()

async def select_value_or(db: AsyncSession, Thread: Any, User: Any, column1: Column, value1: Any, column2: Column):
    subquery = select(
        Thread.id.label('thread_id'),
        case(
            (column1 == value1, column2),
            (column2 == value1, column1)
        ).label('other_participant_id')
    ).where(
        or_(column1 == value1, column2 == value1)
    ).subquery()

    async with db as session:
        query = select(
            subquery.c.thread_id,
            User.nome_completo.label('nome_completo'),
            subquery.c.other_participant_id
        ).select_from(
            join(User, subquery, User.id == subquery.c.other_participant_id)
        )

        result = await session.execute(query)
        result_rows = result.fetchall()
        result_list = [
            {
                'thread_id': row.thread_id,
                'nome_completo': row.nome_completo,
                'other_participant_id': row.other_participant_id
            }
            for row in result_rows
        ]
        return result_list
		

async def select_value_and_or(db: AsyncSession, model: Any, column1: Column, value1: Any, column2: Column, value2: Any): 
    async with db as session:
        query = select(model).where(or_(and_(column1 == value1, column2 == value2), and_(
            column1 == value2, column2 == value1)))
        result = await session.execute(query)
        resultValue = result.scalar()
        return resultValue
		

async def value_exists_and_or(db: AsyncSession, model: Any, column1: Column, value1: Any, column2: Column, value2: Any) -> bool:
    async with db as session:
        consulta = select(exists().where(or_(and_(column1 == value1, column2 == value2), and_(
            column1 == value2, column2 == value1)))).select_from(model)
        resultado = await session.execute(consulta)
        return resultado.scalar()
    

async def delete_value(db: AsyncSession, model: Any, column: Column, value: Any):
    async with db as session:
        query = delete(model).where(column == value)
        result = await session.execute(query)
        await session.commit()
        return result.rowcount

async def select_value_all_order_by(db: AsyncSession, model: Any, column: Column, value: Any, order_column: Column):
    async with db as session:
        query = select(model).filter(column == value).order_by(order_column)
        result = await session.execute(query)
        resultValue = result.scalars().all()
        return resultValue