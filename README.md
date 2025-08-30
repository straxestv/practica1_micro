# Practica 1 Microprocesadores Control de barra de leds con menú mediante una página y PICO

Este proyecto implementa un sistema de control de LEDs utilizando una Raspberry Pi Pico W como servidor web.
A traves de una interfaz grafica accesible desde cualquier navegador, el usuario puede seleccionar distintas secuencias de encendido de LEDs utilizando un teclado virtual de 9 botones.

Cada boton ejecuta una animacion diferente en la barra de LEDs, lo que permite comprender la integracion entre hardware (GPIO, LEDs) y software (servidor web, HTML, JavaScript, Python/MicroPython).

#Objetivos.

Comprender como la Raspberry Pi Pico W se conecta a una red WiFi y actua como un servidor web.
Implementar comunicacion entre frontend y el backend.
Programar secuencias logicas de encendido de LEDs usando controladores GPIO.
Favorecer el aprendizaje practico de redes, electronica digital y programacion web embedida.

#Ejecucion del proyecto

1.- Clona o copia los archivos del proyecto en tu computadora.

2.- Abre el codigo en Thonny y selecciona el interprete MicroPython.

3.- Configura tu red cambiando los datos entre comillas de las siguientes variables:

SSID = "Tu-SSID"
PASSWORD = "La contraseña de tu red"

4.- Ejecuta el programa y observa en la consola la direccion IP asignada al Pico W.

5.- Desde cualquier navegador, ingresa a:

http://<IP-DE-TU-PICO>

6.- Controla la secuencia de leds desde la pagina.
