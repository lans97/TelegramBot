import asyncio
from aiogram import types, Dispatcher
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile
from aiogram.filters import Filter, CommandStart

from io import BytesIO

from cdabot.routers import func_router, msgEq
from cdabot.utilities import *

from secretos import sensores

# Números sensores
pm25 = 9  # P.M. 2.5
pm10 = 8  # P.M. 10
ozono = 7  # Ozono
co = 2  # CO
temperatura = 12  # Temperatura
humedad = 3 # Humedad

# Actividad Resumen
@func_router.message(msgEq('📚 Resumen'))
async def resumen(message: Message):
    await message.answer("Calculando resumen...")
    device = "IBERO2"
    result = analyze_environment(device)
    if result == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
    else:
        await message.answer(result)

# Actividad ICA
@func_router.message(msgEq('🚦 Categoria ICA'))
async def categoria_ICA(message: Message):
    await message.answer("Calculando ICA...")
    device = "METEORO1"
    dato = categoria_aire_f("METEORO1")
    if dato == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
    else:
        await message.answer(dato)

# Actividad Temperatura Hoy
@func_router.message(msgEq('🌇 Hoy'))
async def temperatura_hoy(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", temperatura, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)
    # Se envía el valor máximo
    await message.answer(f"Temperatura más alta: {max_value} °C")

# Actividad Temperatura Semanal
@func_router.message(msgEq('🌃 Semanal'))
async def temperatura_semanal(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", temperatura, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)
    # Se envía el valor máximo
    await message.answer(f"Temperatura más alta: {max_value} °C")

# Actividad Humedad Hoy
@func_router.message(msgEq('🚿 Hoy'))
async def humedad_hoy(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", humedad, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)
    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value}%")

# Actividad Humedad Semanal
@func_router.message(msgEq('🌊 Semanal'))
async def humedad_semanal(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", humedad, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value}%")

# Actividad PM2.5 Hoy
@func_router.message(msgEq('🕒 Hoy'))
async def pm2_5_hoy(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", pm25, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ug/m3")

# Actividad PM25 Semanal
@func_router.message(msgEq('📅 Semanal'))
async def pm2_5_semanal(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", pm25, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ug/m3")

# Actividad PM10 Hoy
@func_router.message(msgEq('😤 Hoy'))
async def pm10_hoy(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", pm10, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ug/m3")

# Actividad PM10 Semanal
@func_router.message(msgEq('🧹 Semanal'))
async def pm10_semanal(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", pm10, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ug/m3")

# Actividad O2 Hoy
@func_router.message(msgEq('🕕 Hoy'))
async def o2_hoy(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", ozono, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ppb")

# Actividad O2 Semanal
@func_router.message(msgEq('🕡 Semanal'))
async def o2_semanal(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", ozono, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ppb")

# Actividad CO Hoy
@func_router.message(msgEq('🛵 Hoy'))
async def co_hoy(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", co, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ppb")

# Actividad CO Semanal
@func_router.message(msgEq('✈️ Semanal'))
async def co_semanal(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBERO2"
    res = generar_grafica("IBERO2", co, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ppb")

# Actividad musica loop
@func_router.message(msgEq('🎧 Reproducir Música'))
async def play_music(message: Message):
    #play_obj = wave_obj.play()
    await message.answer("🎵 Reproduciendo música...")

# Actividad detener musica
@func_router.message(msgEq('⏹ Detener Música'))
async def stop_music(message: Message):
    #mixer.music.stop()  # Stop playing the music
    await message.answer("⏹ Música detenida")

def setup(dp: Dispatcher):
    dp.include_router(func_router)