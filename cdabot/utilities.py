import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import json
from googletrans import Translator

import os
import re
from io import BytesIO
from PIL import Image

from cdabot import smability
from secretos import sensores

import logging

logging.basicConfig(level=logging.ERROR)

file_handler = logging.FileHandler('cdaBot.log')
file_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logging.getLogger().addHandler(file_handler)


def sensor_avg_last_24hrs(device: str, idSensor: int) -> float:
    end = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    start = end - timedelta(days=1)
    try:
        data = smability.get_data(sensores[device], (idSensor, ), start, end)[0]
        if (len(data) > 0):
            sum = 0.0
            for el in data:
                sum += float(el["Data"])
            return sum/len(data)
        else:
            raise Exception("No data from API")

    except Exception as e:
        logging.error(e)
        return None

def sensor_avg_per_day(device: str, idSensor: int, n_days_ago: int = 1) -> float:
    end = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=n_days_ago)
    start = end - timedelta(days=1)

    try:
        data = smability.get_data(sensores[device], (idSensor, ), start, end)[0]
        if (len(data) > 0):
            sum = 0.0
            for el in data:
                sum += float(el["Data"])
            return sum/len(data)
        else:
            raise Exception("No data from API")

    except Exception as e:
        logging.error(e)
        return None

def analyze_environment(device: str) -> str:
    # Get all average values for the last 24 hrs
    pm25 = sensor_avg_last_24hrs(device, 9)  # P.M. 2.5
    if pm25 == None:
        return None
    pm10 = sensor_avg_last_24hrs(device, 8)  # P.M. 10
    if pm10 == None:
        return None
    ozone = sensor_avg_last_24hrs(device, 7)  # Ozono
    if ozone == None:
        return None
    co = sensor_avg_last_24hrs(device, 2)  # CO
    if co == None:
        return None
    temperature = sensor_avg_last_24hrs(device, 12)  # Temperatura
    if temperature == None:
        return None
    humidity = sensor_avg_last_24hrs(device, 3)  # Humedad
    if humidity == None:
        return None

    # Calculate evaluation scores for each parameter
    pm25eval = evaluate_pm25(pm25)
    pm10eval = evaluate_pm10(pm10)
    ozonoeval = evaluate_ozone(ozone)
    coeval = evaluate_co(co)
    temperaturaeval = evaluate_temperature(temperature)
    humedadeval = evaluate_humidity(humidity)

    # Calculate total score and corresponding quality
    total = pm25eval + pm10eval + ozonoeval + coeval + temperaturaeval + humedadeval
    calidadA = calculate_quality(total)

    return calidadA

def categoria_aire_f(device: str) -> str:
    
    try:
        data = smability.get_data(sensores[device], (1001, ), datetime.today(), datetime.today())[0]
    except Exception as e:
        logging.error(e)
        return None
        
    
    if len(data[0]) < 1:
        return None
    
    json_data = data[0]["Data"]

    data_dict = json.loads(json_data)
    
    descrip = data_dict["Description"]

    descrip = str(descrip)
    
    # Translate the description to Spanish
    translator = Translator()
    translated_descrip = translator.translate(descrip, dest='es').text

    colores = data_dict["Color"]
    colores = str(colores)

    if colores == '#00E400':
        combined_info = f"🟩 Categoría: Buena. {translated_descrip} "
    elif colores == "#00E400":
        combined_info = f"🟨 Categoría: Moderada. {translated_descrip} "
    elif colores == "#FF7E00":
        combined_info = f"🟧 Categoría: Insalubre para grupos sensibles. {translated_descrip} "
    elif colores == "#FF0000":
        combined_info = f"🟥 Categoría: Insalubre. {translated_descrip} "
    elif colores == "#8F3F97":
        combined_info = f"🟪 Categoría: Muy insalubre. {translated_descrip} "
    elif colores == "#7E0023":
        combined_info = f"⚠️ Categoría: Peligroso. {translated_descrip} "

    out_str = f"{datetime.now().isoformat(sep=" ", timespec="seconds")} {combined_info}"

    return out_str

def generar_grafica(device: str, sensor: int, days: int = 1) -> tuple[str, float]:
    if not os.path.exists("images"):
        os.mkdir("images")

    if days < 1:
        days = 1

    df = datetime.today().replace(minute=0, second=0, microsecond=0)
    d0 = df - timedelta(days=days)

    date_fmt = "%Y-%m-%d-%Hhrs"

    matches = find_filename_pattern("images", rf"reporte-{device}-{sensor}-{d0.strftime(date_fmt)}-{df.strftime(date_fmt)}-[\d+\.\d+]+\.png")
    if len(matches) == 0:
        try:
            data = smability.get_data(sensores[device], (sensor, ), d0, df)[0]
        except Exception as e:
            logging.error(e)
            return None
            
        if len(data) < 1:
            return None
        
        y = np.array([float(d["Data"]) for d in data])
        x = np.array([datetime.strptime(d["TimeStamp"], "%Y-%m-%dT%H:%M:%S") for d in data])

        max_value = np.max(y)

        img_name = f"reporte-{device}-{sensor}-{d0.strftime(date_fmt)}-{df.strftime(date_fmt)}-{max_value}.png"

        plt.plot(x, y)

        plt.savefig("images/" + img_name)
        
        plt.clf()
        img_path = "images/" + img_name
    else:
        img_path = "images/" + matches[0]
        max_value = float(re.findall(rf"([\d+\.\d]+)\.png", matches[0])[0])
        
    return (img_path, max_value)

def find_filename_pattern(directory: str, pattern: str) -> bool:
    matching_files = []
    for filename in os.listdir(directory):
        if re.match(pattern, filename):
            matching_files.append(filename)
    return matching_files

def evaluate_pm25(pm25):
    if pm25 < 12:
        return 1  # Bueno
    elif 12 <= pm25 <= 35.4:
        return 2  # Moderado
    elif 35.5 <= pm25 <= 55.4:
        return 3  # Insalubre para grupos sensibles
    else:
        return 4  # Insalubre para todos

def evaluate_pm10(pm10):
    if pm10 < 54:
        return 1  # Bueno
    elif 54 <= pm10 <= 154:
        return 2  # Moderado
    elif 155 <= pm10 <= 254:
        return 3  # Insalubre para grupos sensibles
    else:
        return 4  # Insalubre para todos

def evaluate_ozone(ozone):
    if ozone < 50:
        return 1  # Bueno
    elif 50 <= ozone <= 100:
        return 2  # Moderado
    elif 101 <= ozone <= 168:
        return 3  # Insalubre para grupos sensibles
    else:
        return 4  # Insalubre para todos

def evaluate_co(co):
    if co < 400:
        return 1  # Bueno
    elif 400 <= co <= 1000:
        return 2  # Moderado
    elif 1001 <= co <= 2000:
        return 3  # Insalubre para grupos sensibles
    else:
        return 4  # Insalubre para todos

def evaluate_temperature(temperature):
    if 20 <= temperature <= 25:
        return 1
    elif temperature > 25:
        return 2
    else:
        return 3

def evaluate_humidity(humidity):
    if 30 <= humidity <= 60:
        return 1
    else:
        return 2

def calculate_quality(total) -> str:
    if total < 11:
        return 'Resumen del día: Calidad buena 😀.'
    elif 11 <= total < 16:
        return 'Resumen del día: Calidad regular 😐.'
    else:
        return 'Resumen del día: Calidad mala 🙁.'
