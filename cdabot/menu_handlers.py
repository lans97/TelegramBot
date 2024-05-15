from aiogram import types, Router, Dispatcher
from aiogram.types import Message
from aiogram.filters import Filter, CommandStart
from cdabot.menus import *

router = Router()

class msgEq(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text
    
    async def __call__(self, message: Message) -> bool:
        return message.text == self.my_text

# UI Handlers

# Inicio de la interfaz principal
@router.message(CommandStart())
async def send_main_menu(message: types.Message):
    await message.answer('🐺 ¡Hola! Soy tu asistente meteorológico de la Universidad Iberoamericana. Mi objetivo es brindarte información detallada sobre el clima y el tiempo en nuestro campus y sus alrededores. Desde pronósticos diarios hasta datos climáticos históricos, estoy aquí para mantenerte informado y ayudarte a planificar tu día de manera eficiente. ¡Bienvenido y disfruta de la precisión meteorológica a tu alcance!')
    await message.answer('Este es el menú principal, selecciona con un boton aquello que deseas conocer:', reply_markup=menu_principal_inter.as_markup())

# Definición de submenu "Calidad del aire"
@router.message(msgEq("🩺 Calidad del aire"))
async def send_submenu_r(message: types.Message):
    await message.answer('¿Qué deseas conocer? 🪁.', reply_markup=submenu_calidad_inter.as_markup())

# Definición de submenu "Estacion Mete"
@router.message(msgEq("🌎 Estación meteorológica"))
async def send_submenu_o(message: types.Message):
    await message.answer('¿Qué dato es de tu interés? 🌎', reply_markup=submenu_estacion_inter.as_markup())

# Definición de submenu "Contaminantes"
@router.message(msgEq("🚦 Contaminantes"))
async def send_submenu_o(message: types.Message):
    await message.answer('¿Qué dato es de tu interés? ', reply_markup=submenu_conta_inter.as_markup())

# Definición de submenu "Temperatura"
@router.message(msgEq("🌡 Temperatura"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar? 🌡', reply_markup=submenu_tempe_inter.as_markup())

# Definición de submenu "Humedad"
@router.message(msgEq("💧 Lluvia"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_lluvia_inter.as_markup())

# Definición de submenu "PM25"
@router.message(msgEq("😤 PM 2.5"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_pm25_inter.as_markup())

# Definición de submenu "PM10"
@router.message(msgEq("🧹 PM 10"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_pm10_inter.as_markup())

# Definición de submenu "Ozono"
@router.message(msgEq("🛡️ Ozono"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_o2_inter.as_markup())

# Definición de submenu "CO"
@router.message(msgEq("🧯 Monóxido de carbono"))
async def send_submenu_t(message: types.Message):
    await message.answer('¿Qué rango te gustaría analizar?', reply_markup=submenu_co_inter.as_markup())

# Definición de submenu "Resumen"
@router.message(msgEq("Menú inicial 🏠"))
async def send_hogar(message: types.Message):
    await message.answer('¿Qué te apetece conocer? 🔮', reply_markup=menu_principal_inter.as_markup())

# Definición de submenu "Musica"
@router.message(msgEq("🎧 ¿Quiénes somos?"))
async def send_musicc(message: types.Message):
    await message.answer('📻',reply_markup=submenu_music_inter.as_markup())
    
def setup(dp: Dispatcher):
    dp.include_router(router)