import matplotlib.pyplot as plt
import matplotlib as mpl
import mplcyberpunk

import pandas as pd

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

def sensor_data_per_day(device: str, idSensor: int, n_days_ago: int = 1) -> list:
    start = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=n_days_ago)
    if n_days_ago == 0:
        end = datetime.today()
    else:
        end = start + timedelta(days=1)

    try:
        data = smability.get_data(sensores[device], (idSensor, ), start, end)[0]
        if (len(data) > 0):
            return data
        else:
            raise Exception("No data from API")

    except Exception as e:
        logging.error(e)
        return None


def sensor_avg_per_day(device: str, idSensor: int, n_days_ago: int = 0) -> float:
    try:
        data = sensor_data_per_day(device, idSensor, n_days_ago)
        sum = 0.0
        for el in data:
            sum += float(el["Data"])
        return sum/len(data)

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
    
    d0 = datetime.today()
    try:
        data = smability.get_data(sensores[device], (1001, ), d0, d0)[0]
    except Exception as e:
        logging.error(e)
        return None
        
    
    if len(data[0]) < 1:
        return None
    
    json_data = data[0]["Data"]

    data_dict = json.loads(json_data)
    
    descrip = data_dict["Description"]
    descripSalud = data_dict["Health"]
    descripData = data_dict["Data"]
    descrip = str(descrip)
    descripSalud = str(descripSalud)
    descripData = int(descripData)

    descrip = str(descrip)
    
    # Translate the description to Spanish
    translator = Translator()
    translated_descrip = translator.translate(descrip, dest='es').text
    translated_descrip2 = translator.translate(descripSalud, dest='es').text

    colores = data_dict["Color"]
    colores = str(colores)

    combined_info = ''
    value_to_annotate = 0

    # Definicio de caracteristicas por código de color

    if colores == '00E400':
        combined_info = f"Fecha: {d0} - Buena. {translated_descrip} {translated_descrip2}"
        value_to_annotate = descripData
    elif colores == "#00E400":
        combined_info = f"Fecha: {d0} - Moderada. {translated_descrip} {translated_descrip2}"
        value_to_annotate = descripData
    elif colores == "#FF7E00":
        combined_info = f"Fecha: {d0} -  Insalubre para grupos sensibles. {translated_descrip} {translated_descrip2}"
        value_to_annotate = descripData
    elif colores == "#FF0000":
        combined_info = f"Fecha: {d0} -  Insalubre. {translated_descrip} {translated_descrip2}"
        value_to_annotate = descripData
    elif colores == "#8F3F97":
        combined_info = f"Fecha: {d0} -  Muy insalubre. {translated_descrip} {translated_descrip2}"
        value_to_annotate = descripData
    elif colores == "#7E0023":
        combined_info = f"Fecha: {d0} -  Peligroso. {translated_descrip} {translated_descrip2}"
        value_to_annotate = descripData

    contaminante1 = data_dict["lastPM25"]
    contaminante2 = data_dict["lastPM10"]
    contaminante3 = data_dict["lastO3"]
    contaminante4 = data_dict["lastCO"]

    contaminante1 = str(contaminante1)
    contaminante2 = str(contaminante2)
    contaminante3 = str(contaminante3)
    contaminante4 = str(contaminante4)

    # Definicion del texto

    tweet_text = f"Reporte de contaminantes({d0}):\n{contaminante1}\n{contaminante2}\n{contaminante3}\n{contaminante4}"

    mpl.rcParams['text.color'] = 'white'

    translated_descrip_jump = insert_line_breaks(combined_info)

    fig = plt.figure(figsize=(8, 2.5), facecolor='black')
    ax2 = fig.add_axes([0.05, 0.8, 0.9, 0.15])

    # Creación de la gráfica, variación de colores y ranfo

    cmap = mpl.colors.ListedColormap(['#00E400', '#FFFF00', '#FF7E00', '#FF0000', '#8F3F97', '#7E0023'])
    bounds = [0, 50, 100, 150, 200, 300, 500]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
                                    norm=norm,
                                    spacing='proportional',
                                    orientation='horizontal')

    texto = f"\nAQI del {d0}"
    r = texto.rjust(20)

    #plt.title('AQI', fontsize=25, fontweight='bold', fontfamily='sans-serif')

    ax2.spines['bottom'].set_color('white')
    ax2.spines['left'].set_color('white')
    ax2.tick_params(axis='both', colors='white')

    cb2.set_label(f'{translated_descrip_jump}', fontsize=15, fontfamily='sans-serif', color='white')

    ax2.annotate(f'AQI: {value_to_annotate}', xy=(value_to_annotate, 0), xytext=(value_to_annotate, 2), color='black',
                 arrowprops=dict(facecolor='black', arrowstyle='->'))

    plt.savefig('images/graph.png')

    return tweet_text


def insert_line_breaks(text, line_length=60):
    lines = []
    for i in range(0, len(text), line_length):
        lines.append(text[i:i + line_length])
    return '\n'.join(lines)

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
        avg = np.mean(y)

        img_name = f"reporte-{device}-{sensor}-{d0.strftime(date_fmt)}-{df.strftime(date_fmt)}-{max_value}.png"

        # Matplotlib setup
        plt.style.use('cyberpunk')
        fig, ax = plt.subplots(figsize=(10, 6))

        match sensor:
            case 9:
                # P.M. 2.5
                long_var = "P.M. 2.5"
                short_var = "PM25"
                units = "ug/m3"
            case 8:
                # P.M. 10
                long_var = "P.M. 10"
                short_var = "PM10"
                units = "ug/m3"
            case 7:
                # Ozono
                long_var = "Ozono"
                short_var = "O2"
                units = "ppb"
            case 2:
                # CO
                long_var = "Monóxido de Carbono"
                short_var = "CO"
                units = "ppb"
            case 12:
                # Temperatura
                long_var = "Temperatura"
                short_var = "temp"
                units = "ªC"
            case 3:
                # Humedad
                long_var = "Humedad Relativa"
                short_var = "hum"
                units = "%"

        main_lbl = f"REPORTE: {long_var} \nDEL {d0.strftime('%Y-%m-%d')} AL {df.strftime('%Y-%m-%d')}"
        line_lbl = f"{short_var} {units}"
        avg_lbl = f"Promedio {short_var} {units}"

        ax.plot(x, y, "C0", label=line_lbl)
        ax.axhline(y=avg, color='#FE53BB', linestyle='--', label=avg_lbl)
        ax.set(xlim=(np.min(x), np.max(x)), xlabel="Fecha", ylabel=f"{long_var} {units}")
        ax.yaxis.label.set_color("C0")

        handles, labels = ax.get_legend_handles_labels()
        plt.legend(handles, labels)
        mplcyberpunk.make_lines_glow()
        mplcyberpunk.add_underglow()

        plt.title(main_lbl, fontsize=25, fontweight='bold', fontfamily='sans-serif')
        fig.savefig("images/" + img_name)
        
        fig.clear()
        img_path = "images/" + img_name
    else:
        img_path = "images/" + matches[0]
        max_value = float(re.findall(rf"([\d+\.\d]+)\.png", matches[0])[0])
        
    
    return (img_path, max_value)

def create_windrose_plot(device: str, d_time: timedelta):
    df = datetime.today()
    d0 = df - d_time

    alist = smability.get_data(device, (18, ), d0, df)[0]
    blist = smability.get_data(device, (19, ), d0, df)[0]

    alist_values = [item['Data'] for item in alist]
    blist_values = [item['Data'] for item in blist]

    # Se extraen los datos de las listas
    df = pd.DataFrame({
        "axis": alist_values,  # Se obtienen los valores
        "velocidad": blist_values
    })

    # Se transfiere los valores flotantes
    df['axis'] = df['axis'].astype(float)

    # Se definen las 16 direcciones
    def map_angle_to_direction(angle):
        directions = ["ENE", "NNE", "N", "NE", "E", "S", "SSE", "SSO", "SO", "NO", "ONO", "SE", "OSO", "NNO", "O", "ESE"]
        angle_step = 360 / len(directions)
        normalized_angle = (angle + 360) % 360
        index = int(normalized_angle // angle_step)
        return directions[index]

    # Se aplica una funcion de direccion
    df['direction'] = df['axis'].apply(map_angle_to_direction)

    # Fuerza a flotantes
    df['velocidad'] = df['velocidad'].astype(float)

    # Rename the 'velocidad' column to 'Velocidad[m/s]'
    df.rename(columns={'velocidad': 'Velocidad[m/s]'}, inplace=True)

    # Definicion de colores
    def map_strength_to_color(velocidad):
        color_groups = ["purple", "blue", "green", "yellow", "orange", "red"]
        group_index = min(int(velocidad) // 1, len(color_groups) - 1)
        return color_groups[group_index]

    df['color'] = df['Velocidad[m/s]'].apply(map_strength_to_color)

    #df.to_csv('Descargables/windrose_data.csv', index=False)

    # Creacion de la rosa de los vientos basdo sen la magnitud y direccion obtenidos de la lectura
    fig = px.bar_polar(df, r="Velocidad[m/s]", theta="direction",
                       color="Velocidad[m/s]",  
                       color_continuous_scale=px.colors.sequential.Plasma,  
                       template="plotly_dark",
                       title="REPORTE: TEMPERATURA \nDEL " + one_day_ago.strftime('%Y/%m/%d') + " AL " + today.strftime("%Y/%m/%d"))

    fig.update_traces(marker=dict(opacity=0.7)) 
    fig.update_layout(
        polar=dict(
            radialaxis=dict(showticklabels=False, ticks=''),
            angularaxis=dict(direction='clockwise')
        ),
        images=[dict(
            source='https://3.bp.blogspot.com/-J2y8YWcMdXM/XCL4aq9WDyI/AAAAAAAAL3M/cayVTD-qScMt49_jBA93R6e_LjgPr9WcgCLcBGAs/s1600/ibero01.jpg',  # Path to your image file
            xref="paper", yref="paper",
            x=0.5, y=0.5,  # Posición del fondo
            sizex=1, sizey=1,  # Tamaño de la imagen
            xanchor="center", yanchor="middle",
            layer="below"  
        )]
    )

    fig.write_image(file='images/graph.png', format='png')

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
