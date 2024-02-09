import aiohttp
from typing import Dict, Any
from schemas import ExpenseRequest
from datetime import datetime


class TeleWrapper:

    def __init__(self, token):
        self.token = token
        self.baseurl = f'https://api.telegram.org/bot{token}/'
    
    
    async def send_message(self, chat_id: int, text: str):
        """
        chat_id: int: chat id to send the message
        text: str: text to send
        """
        
        method = "sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.baseurl + method, data=payload) as resp:
                return resp

    async def set_webhook(self, url: str):
        """
        url: str: url to set the webhook
        eg:
            https://d6d2-203-192-251-167.ngrok-free.app/bot/post
        """

        method = "setWebhook"
        params = {"url": url}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.baseurl + method, params = params) as resp:
                return resp

    def get_chatid_or_updateid(self, dat: Dict[Any, Any]) -> int:
        """
        return the updateid or chat id
        """
        if 'message' in dat:
            return dat['message']['chat']['id'], False
        else:
            return dat['edited_message']['chat']['id'], True
        
    def get_expense_from_json(self, dat: Dict[Any, Any]) -> ExpenseRequest:
        """
        return the expense object from the json
        """

        id = dat['message']['message_id']
        user = dat['message']['from']['id']
        splitt = dat['message']['text'].split('-')
        data_dict = {item.split(':')[0]: item.split(':')[1] for item in splitt}
        data_dict['id'] = id
        # data_dict['user'] = user
        data_dict["created_at"] = data_dict["date"]
        data_dict["description"] = data_dict["desc"]
        data_dict.pop('date')
        data_dict["created_at"] = datetime.strptime(data_dict["created_at"], '%m/%d/%Y')
        data_dict.pop("desc")
        data_dict["username"] = dat["message"]["chat"]["username"]
        # data_dict["user_id"] = dat["message"]["from"]["id"]
        user = {"username": data_dict["username"], "user_id": dat["message"]["from"]["id"]}
        expense = ExpenseRequest(**data_dict)
        return expense, user

"""
{'amount': '120', 'date': '12/10/2024', 'category': 'fun', 'desc': 'test', 'id': 178, 'username': 'KING_STAR_0'}
https://api.telegram.org/bot6723763881:AAGp0HoQ7c45xQ7GzUGXCiAWLlPHHtG8JS4/setWebhook?url=https://e14c-203-192-253-220.ngrok-free.app/
"""
