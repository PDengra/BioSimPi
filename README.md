💻 Proyecto: BioSimPi – Simulador de Parámetros Biomédicos en Raspberry Pi
Descripción

BioSimPi es un simulador biomédico en tiempo real desarrollado en Python y Streamlit, que genera parámetros vitales como frecuencia cardíaca (HR), saturación de oxígeno (SpO₂) y temperatura corporal.

El sistema alerta automáticamente mediante correo electrónico y Telegram si algún parámetro se encuentra fuera del rango definido, y mantiene un registro histórico en CSV para análisis posterior.

Características principales

- Generación simulada de parámetros biomédicos en tiempo real.
- Configuración de rangos fisiológicos normales mediante sliders en la barra lateral.
- Alertas visuales en la interfaz cuando los valores exceden los límites.

Notificaciones automáticas por:

- Correo electrónico usando SMTP y contraseña de aplicación de Gmail.
- Telegram mediante bot y chat ID.
- Historial de datos guardado en biosimpi_log.csv y visualizado con gráficas dinámicas.
- Interfaz interactiva creada con Streamlit.

Tecnologías utilizadas:

- Python 3
- Streamlit
- NumPy / Pandas
- smtplib (correo electrónico)
- python-telegram-bot (Telegram)
- Raspberry Pi OS
  
--------------------------------------------------------------------------------------------------------------------------------------------------------------------

Instalación y uso:

1. Preparar Raspberry Pi
sudo apt update
sudo apt install python3-venv python3-full -y

2. Crear entorno virtual
python3 -m venv ~/biosimpi
source ~/biosimpi/bin/activate

3. Instalar dependencias
pip install streamlit numpy pandas python-telegram-bot

4. Descargar el proyecto

Copia tu script bio_sim_pi_pro.py a la Raspberry, por ejemplo en /home/pi/.

5. Ejecutar el simulador
cd ~
source ~/biosimpi/bin/activate
streamlit run ~/bio_sim_pi_pro.py

Aparecerá la interfaz en:

Local: http://localhost:8501

Red local: http://<IP_DE_TU_PI>:8501

6. Configurar alertas

Correo electrónico:

Usar tu Gmail con contraseña de aplicación (Verificación en dos pasos activada).

Telegram:

- Crear un bot con @BotFather y obtener token.
- Obtener tu chat ID enviando un mensaje al bot y usando:

https://api.telegram.org/bot<TOKEN>/getUpdates

En la barra lateral de Streamlit, rellena:

- Correo remitente (Gmail)
- Contraseña de aplicación
- Correo destinatario
- Token de Telegram y Chat ID
