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
radiacion = 27 #Radiacion

# Actividad Resumen
@func_router.message(msgEq('📚 Resumen'))
async def resumen(message: Message):
    await message.answer("Calculando resumen...")
    device = "IBEROA"
    result = analyze_environment(device)
    if result == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
    else:
        await message.answer(result)

# Actividad ICA
@func_router.message(msgEq('🚦 Categoria ICA'))
async def categoria_ICA(message: Message):
    await message.answer("Calculando ICA...")
    device = "IBEROA"
    dato = categoria_aire_f(device)
    if dato == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
    else:
        image = FSInputFile('images/graph.png')
        await message.answer_photo(photo=image)
        await message.answer(dato)

# Actividad Temperatura Hoy
@func_router.message(msgEq('🌇 Hoy'))
async def temperatura_hoy(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBEROA"
    res = generar_grafica("IBEROA", temperatura, 1)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", temperatura, 7)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", humedad, 1)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", humedad, 7)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", pm25, 1)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", pm25, 7)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", pm10, 1)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", pm10, 7)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", ozono, 1)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", ozono, 7)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", co, 1)
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
    device = "IBEROA"
    res = generar_grafica("IBEROA", co, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} ppb")

# Actividad Radiacion Hoy
@func_router.message(msgEq('☀ Hoy'))
async def co_hoy(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBEROA"
    res = generar_grafica("METEORO1", radiacion, 1)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} W/m2")

# Actividad Radiacion Semanal
@func_router.message(msgEq('😎 Semanal'))
async def co_semanal(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBEROA"
    res = generar_grafica("METEORO1", radiacion, 7)
    if res == None:
        await message.answer(f"Parece haber un error con el dispositivo {device}. Intenta más tarde")
        return
    image_path, max_value = res
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

    # Se envía el valor máximo
    await message.answer(f"Valor más alto: {max_value} W/m2")

# Actividad Rosa Hoy
@func_router.message(msgEq('🪁 Hoy'))
async def co_semanal(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBEROA"
    create_windrose_plot("METEORO1", 1)
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

# Actividad Rosa Hoy
@func_router.message(msgEq('🪂 Semanal'))
async def co_semanal(message: Message):
    await message.answer("Generando gráfica...")
    # Función para graficar
    device = "IBEROA"
    create_windrose_plot("METEORO1", 7)
    image = FSInputFile(image_path)
    await message.answer_photo(photo=image)

# Generar CSV
@func_router.message(msgEq('📥 Descargar CSV'))
async def gen_csv(message: Message):
    # Función para enviar descargable
    files = sorted([f for f in os.listdir('Descargables') if f.endswith('.csv')], key=lambda x: os.path.getmtime(os.path.join('Descargables', x)))
    if files:
        await message.answer("Enviando último reporte...")
        reporte = FSInputFile('Descargables/reporte.csv')
        await message.answer_document(document=reporte)
    else:
         await message.answer("No ha generado ninguna solicitud. Elija algunas de las opciones que se encuentran en el menú. 🤖")
    

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
