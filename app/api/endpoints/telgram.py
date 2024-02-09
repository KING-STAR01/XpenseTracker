from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import SetWebhookResponse

from typing import Dict, Any

from api.telegramwrapper import TeleWrapper
from schemas import ExpenseRequest, UserSchema
from api.endpoints.expense import expense_add, get_session
from api.endpoints.users import user_get, user_add

router = APIRouter()


Token="dummy"
telegram_obj = TeleWrapper(Token)

@router.get("/set_webhook/{url:path}")
async def set_webhook(url: str):
    resp = await telegram_obj.set_webhook(url)
    if resp.status == 200:
        return {"message": "success"}
    else:
        return {"message": "failed to set webhook"}

async def create_user_if_not_exist(user, session):
    res = await user_get(user["user_id"], session)
    if not res:
        u = UserSchema(**user)
        res1 = await user_add(u, session)

@router.post("/post")
async def add_data(data: Dict[Any, Any], session: AsyncSession = Depends(get_session)):
    chat_id, is_update = telegram_obj.get_chatid_or_updateid(data)

    if not is_update:
        try:
            # iam getting expense obj get request and add to database
            exp, user = telegram_obj.get_expense_from_json(data)
            await create_user_if_not_exist(user, session)
            res = await expense_add(exp, session)
        except Exception as e:
            await telegram_obj.send_message(chat_id=chat_id, text="send message in **amount:{amount}-date:{date}-category:{category}-desc:{desc}** format")
            return {"message": f"Error: {e}"}
        await telegram_obj.send_message(chat_id=chat_id, text="expense added successfully")
        return {"message": "success"}
    else:
        await telegram_obj.send_message(chat_id=chat_id, text="updation is not allowed")
        return {"message": "failed"}
