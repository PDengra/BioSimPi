# bio_sim_pi.py

import random
import time
import streamlit as st
import numpy as np
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from telegram import Bot
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="BioSimPi - Simulador Biomédico", layout="wide")

# --- VARIABLES GLOBALES ---
DATA_FILE = "biosimpi_log.csv"
placeholder = st.empty()
history = {"HR": [], "SpO2": [], "Temp": []}

# --- PANEL DE CONFIGURACIÓN ---
st.sidebar.header("⚙️ Configuración del sistema")

# Rangos fisiológicos
st.sidebar.subheader("🧬 Rangos normales")
hr_min = st.sidebar.slider("Frecuencia cardíaca mínima (bpm)", 40, 80, 60)
hr_max = st.sidebar.slider("Frecuencia cardíaca máxima (bpm)", 90, 150, 100)

spo2_min = st.sidebar.slider("SpO₂ mínima (%)", 85, 99, 95)
spo2_max = 100

temp_min = st.sidebar.slider("Temperatura mínima (°C)", 34.0, 37.0, 36.0, step=0.1)
temp_max = st.sidebar.slider("Temperatura máxima (°C)", 37.0, 40.0, 37.5, step=0.1)

# Datos de contacto
st.sidebar.subheader("📧 Notificaciones")
EMAIL_SENDER = st.sidebar.text_input("Correo del remitente", "tucorreo@gmail.com")
EMAIL_PASS = st.sidebar.text_input("Contraseña de aplicación", type="password")
EMAIL_RECV = st.sidebar.text_input("Correo destinatario", "destinatario@gmail.com")

TELEGRAM_TOKEN = st.sidebar.text_input("Token del bot de Telegram")
TELEGRAM_CHAT_ID = st.sidebar.text_input("Chat ID de Telegram")

st.sidebar.markdown("---")
interval = st.sidebar.slider("Intervalo de actualización (segundos)", 1, 10, 3)
st.sidebar.caption("Los datos se actualizan en tiempo real según este intervalo.")

# --- FUNCIONES AUXILIARES ---
def enviar_correo(mensaje):
    if not EMAIL_SENDER or not EMAIL_PASS or not EMAIL_RECV:
        st.warning("Faltan credenciales de correo.")
        return
    try:
        msg = MIMEText(mensaje)
        msg["Subject"] = "⚠️ Alerta Biomédica - BioSimPi"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECV
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        st.warning(f"Error al enviar correo: {e}")

def enviar_telegram(mensaje):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        st.warning("Faltan credenciales de Telegram.")
        return
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=mensaje)
    except Exception as e:
        st.warning(f"Error al enviar mensaje Telegram: {e}")

def generar_parametros():
    return {
        "HR": random.randint(50, 130),
        "SpO2": random.uniform(90, 100),
        "Temp": random.uniform(35, 40)
    }

def verificar_alertas(data):
    alertas = []
    if not (hr_min <= data["HR"] <= hr_max):
        alertas.append(f"❤️ Frecuencia cardíaca fuera de rango: {data['HR']} bpm")
    if not (spo2_min <= data["SpO2"] <= spo2_max):
        alertas.append(f"🩸 Saturación baja: {data['SpO2']:.1f}%")
    if not (temp_min <= data["Temp"] <= temp_max):
        alertas.append(f"🌡️ Temperatura fuera de rango: {data['Temp']:.1f}°C")
    return alertas

def registrar_datos(data):
    registro = {
        "FechaHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "HR": data["HR"],
        "SpO2": round(data["SpO2"], 2),
        "Temp": round(data["Temp"], 2)
    }
    df = pd.DataFrame([registro])
    df.to_csv(DATA_FILE, mode='a', header=not pd.io.common.file_exists(DATA_FILE), index=False)

# --- CABECERA ---
st.title("🧠 BioSimPi – Simulador de parámetros biomédicos")
st.markdown("""
Simulación en tiempo real de frecuencia cardíaca (HR), saturación de oxígeno (SpO₂) y temperatura corporal.
El sistema genera alertas visuales y notificaciones por correo y Telegram si los valores superan los límites definidos.
""")

# --- BUCLE DE SIMULACIÓN ---
while True:
    data = generar_parametros()
    alertas = verificar_alertas(data)
    registrar_datos(data)

    # Actualizar historial para gráficas
    for k in history.keys():
        history[k].append(data[k])
        if len(history[k]) > 40:
            history[k].pop(0)

    # Mostrar dashboard
    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("❤️ Frecuencia cardíaca (bpm)", data["HR"])
        col2.metric("🩸 SpO₂ (%)", f"{data['SpO2']:.1f}")
        col3.metric("🌡️ Temperatura (°C)", f"{data['Temp']:.1f}")

        st.line_chart(np.column_stack([history["HR"], history["SpO2"], history["Temp"]]), 
                      height=300)

        if alertas:
            st.error("⚠️ ALERTAS DETECTADAS ⚠️")
            for a in alertas:
                st.write(f"- {a}")
            mensaje = "\n".join(alertas)
            enviar_correo(mensaje)
            enviar_telegram(mensaje)
        else:
            st.success("✅ Todos los parámetros dentro del rango normal")

        st.caption(f"Última actualización: {datetime.now().strftime('%H:%M:%S')}")

    time.sleep(interval)
