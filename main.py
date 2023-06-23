import logging
from dataclasses import dataclass

from pyrogram import Client

from settings import app_configs


@dataclass
class ForwarderMessageModel(object):
    id: int
    date: str


logger = logging.getLogger(__name__)


def backup_channel(app, new_channel: int, old_channel: int):
    history = app.get_chat_history(chat_id=old_channel)
    list_of_messages = []
    for _h in history:
        if _h.service is not None:
            continue
        list_of_messages.append(ForwarderMessageModel(date=_h.date, id=_h.id))
    for _m in reversed(list_of_messages):
        response = app.forward_messages(chat_id=new_channel,
                                        from_chat_id=old_channel,
                                        message_ids=_m.id)
        app.send_message(chat_id=new_channel,
                         reply_to_message_id=response.id,
                         text=f"Id: <code>{response.id}</code>\nДата публикации: <strong>{_m.date}</strong>")


if __name__ == '__main__':
    app = Client("my_account_tg", api_id=app_configs.APP_API_ID, api_hash=app_configs.APP_API_HASH)
    with app:
        backup_channel(app, new_channel=app_configs.NEW_CHANNEL_ID, old_channel=app_configs.OLD_CHANNEL_ID)
