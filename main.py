import asyncio

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import cdabot.menu_handlers as menu_handlers
import cdabot.function_handlers as function_handlers

API_TOKEN = 'xxx'#Insertar llave
dp = Dispatcher()

menu_handlers.setup(dp)
function_handlers.setup(dp)


async def main() -> None:
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
