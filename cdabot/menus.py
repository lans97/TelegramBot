from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Menus

# Creación del menu principal
menu_principal_inter = ReplyKeyboardBuilder()
menu_principal_inter.button(text='🩺 Calidad del aire')
menu_principal_inter.button(text='🌎 Estación meteorológica')
menu_principal_inter.button(text='🎧 ¿Quiénes somos?')
menu_principal_inter.adjust(1)

# Creación del menú secundario "Calidad del aire"
submenu_calidad_inter = ReplyKeyboardBuilder()
submenu_calidad_inter.button(text='📚 Resumen')
submenu_calidad_inter.button(text='🚦 Categoria ICA')
submenu_calidad_inter.button(text='🚦 Contaminantes')
submenu_calidad_inter.button(text='Menú inicial 🏠')
submenu_calidad_inter.adjust(1)

# Creación del menú secundario "Estación meteorológica"
submenu_estacion_inter = ReplyKeyboardBuilder()
submenu_estacion_inter.button(text='🌡 Temperatura')
submenu_estacion_inter.button(text='💧 Lluvia')
submenu_estacion_inter.button(text='💧 Viento')
submenu_estacion_inter.button(text='🛡️ Radiación')
submenu_estacion_inter.button(text='Menú inicial 🏠')
submenu_estacion_inter.adjust(2, 2)

# Creación del menú secundario "Estación meteorológica (Contaminantes)"
submenu_conta_inter = ReplyKeyboardBuilder()
submenu_conta_inter.button(text='😤 PM 2.5')
submenu_conta_inter.button(text='🧹 PM 10')
submenu_conta_inter.button(text='🛡️ Ozono')
submenu_conta_inter.button(text='🧯 Monóxido de carbono')
submenu_conta_inter.button(text='Menú inicial 🏠')
submenu_conta_inter.adjust(2, 2)

# Creación del menú secundario "Temperatura"
submenu_tempe_inter = ReplyKeyboardBuilder()
submenu_tempe_inter.button(text='🌇 Hoy')
submenu_tempe_inter.button(text='🌃 Semanal')
submenu_tempe_inter.button(text='📥 Descargar CSV')
submenu_tempe_inter.button(text='Menú inicial 🏠')
submenu_tempe_inter.adjust(1)


# Creación del menú secundario "Lluvia"
submenu_lluvia_inter = ReplyKeyboardBuilder()
submenu_lluvia_inter.button(text='🚿 Hoy')
submenu_lluvia_inter.button(text='🌊 Semanal')
submenu_lluvia_inter.button(text='📥 Descargar CSV')
submenu_lluvia_inter.button(text='Menú inicial 🏠')
submenu_lluvia_inter.adjust(1)


# Creación del menú secundario "Viento"
submenu_viento_inter = ReplyKeyboardBuilder()
submenu_viento_inter.button(text='🪁 Hoy')
submenu_viento_inter.button(text='🪂 Semanal')
submenu_viento_inter.button(text='📥 Descargar CSV')
submenu_viento_inter.button(text='Menú inicial 🏠')
submenu_viento_inter.adjust(1)


# Creación del menú secundario "Radiación"
submenu_rad_inter = ReplyKeyboardBuilder()
submenu_rad_inter.button(text='☀ Hoy')
submenu_rad_inter.button(text='😎 Semanal')
submenu_rad_inter.button(text='📥 Descargar CSV')
submenu_rad_inter.button(text='Menú inicial 🏠')
submenu_rad_inter.adjust(1)


# Creación del menú secundario "PM2.5"
submenu_pm25_inter = ReplyKeyboardBuilder()
submenu_pm25_inter.button(text='🕒 Hoy')
submenu_pm25_inter.button(text='📅 Semanal')
submenu_pm25_inter.button(text='📥 Descargar CSV')
submenu_pm25_inter.button(text='Menú inicial 🏠')
submenu_pm25_inter.adjust(1)


# Creación del menú secundario "PM10"
submenu_pm10_inter = ReplyKeyboardBuilder()
submenu_pm10_inter.button(text='😤 Hoy')
submenu_pm10_inter.button(text='🧹 Semanal')
submenu_pm10_inter.button(text='📥 Descargar CSV')
submenu_pm10_inter.button(text='Menú inicial 🏠')
submenu_pm10_inter.adjust(1)


# Creación del menú secundario "O2"
submenu_o2_inter = ReplyKeyboardBuilder()
submenu_o2_inter.button(text='🕕 Hoy')
submenu_o2_inter.button(text='🕡 Semanal')
submenu_o2_inter.button(text='📥 Descargar CSV')
submenu_o2_inter.button(text='Menú inicial 🏠')
submenu_o2_inter.adjust(1)


# Creación del menú secundario "CO"
submenu_co_inter = ReplyKeyboardBuilder()
submenu_co_inter.button(text='🛵 Hoy')
submenu_co_inter.button(text='✈️ Semanal')
submenu_co_inter.button(text='📥 Descargar CSV')
submenu_co_inter.button(text='Menú inicial 🏠')
submenu_co_inter.adjust(1)


# Creación del menú secundario "🎧"
submenu_music_inter = ReplyKeyboardBuilder()
submenu_music_inter.button(text='🎧 Reproducir Audio')
submenu_music_inter.button(text='⏹ Detener Audio')
submenu_music_inter.button(text='Menú inicial 🏠')
submenu_music_inter.adjust(1)
