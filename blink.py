import network
import socket
import time
from machine import Pin

# ---------------------------
# Configuración WiFi
# ---------------------------
SSID = "Nombre de la red"  #aqui se debe ingresar el nombre de nuestra red
PASSWORD = "Contraseña de la red"  # de igual forma que en lo anterior ingresar la contraseña

wlan = network.WLAN(network.STA_IF) #comprueba la conexion si se puede conectar
wlan.active(True) #si si pasa al siguiente metodo
wlan.connect(SSID, PASSWORD) #con este metodo se estable la conexion con nuestra red con los atributos que le proporcionamos anteriormente

print("Conectando a WiFi...")
while not wlan.isconnected():
    time.sleep(1)

print("Conectado a WiFi:", wlan.ifconfig())
ip = wlan.ifconfig()[0]

# ---------------------------
# Configuración de LEDs (10 pines consecutivos del GP2 al GP11)
# ---------------------------
led_pins = [Pin(i, Pin.OUT) for i in range(2, 12)]
for led in led_pins:
    led.off()

# ---------------------------
# Secuencias de LEDs
# ---------------------------
def secuencia_1():  # Izquierda → Derecha
    for led in led_pins:
        led.on()
        time.sleep(0.2)
        led.off()

def secuencia_2():  # Derecha → Izquierda
    for led in reversed(led_pins):
        led.on()
        time.sleep(0.2)
        led.off()

def secuencia_3():  # Centro hacia los lados
    centro = len(led_pins) // 2
    for i in range(centro + 1):
        if centro - i >= 0:
            led_pins[centro - i].on()
        if centro + i < len(led_pins):
            led_pins[centro + i].on()
        time.sleep(0.2)
        for led in led_pins:
            led.off()

def secuencia_4():  # Solo costado derecho
    led_pins[-1].on(); time.sleep(0.5); led_pins[-1].off()

def secuencia_5():  # Solo costado izquierdo
    led_pins[0].on(); time.sleep(0.5); led_pins[0].off()

def secuencia_6():  # Vúmetro (acumulativo de izq. a der.)
    for i in range(len(led_pins)):
        for j in range(i + 1):
            led_pins[j].on()
        time.sleep(0.2)
        for led in led_pins:
            led.off()

def secuencia_7():  # Pares (índices pares)
    for i in range(0, len(led_pins), 2):
        led_pins[i].on()
    time.sleep(0.5)
    for led in led_pins:
        led.off()

def secuencia_8():  # Nones (índices impares)
    for i in range(1, len(led_pins), 2):
        led_pins[i].on()
    time.sleep(0.5)
    for led in led_pins:
        led.off()

def secuencia_9():  # Dos de cada costado (parpadeo 2 izq + 2 der)
    for _ in range(3):
        led_pins[0].on(); led_pins[1].on()
        led_pins[-1].on(); led_pins[-2].on()
        time.sleep(0.4)
        for led in led_pins:
            led.off()
        time.sleep(0.2)

# Mapeo de secuencias
secuencias = {
    "1": secuencia_1,
    "2": secuencia_2,
    "3": secuencia_3,
    "4": secuencia_4,
    "5": secuencia_5,
    "6": secuencia_6,
    "7": secuencia_7,
    "8": secuencia_8,
    "9": secuencia_9,
}

# ---------------------------
# Página HTML integrada
# ---------------------------
html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Teclado para controlar barra de leds</title>
  <style>
    body { background-image: url("https://cdn.myanimelist.net/s/common/uploaded_files/1450334498-7c9a08087503f7f42209f491d5768ffa.jpeg"); background-repeat: no-repeat; background-size: cover; background-position: center; background-attachment: fixed; font-family: Arial, sans-serif; text-align: center; }
    .grid { display: grid; grid-template-columns: repeat(3, 80px); gap: 10px; justify-content: center; margin-top: 50px; }
    button { font-size: 20px; color: azure; background-color: #10A8B5; transition-duration: 0.4s; padding: 20px; border-radius: 10px; cursor: pointer; }    
    #msg { margin-top: 20px; font-weight: bold; }
  </style>
</head>
<body>
  <h1>Teclado para control de barra de leds.</h1>
  
  <div class="grid">
    <button onclick="sendOption(1)">1</button>
    <button onclick="sendOption(2)">2</button>
    <button onclick="sendOption(3)">3</button>
    <button onclick="sendOption(4)">4</button>
    <button onclick="sendOption(5)">5</button>
    <button onclick="sendOption(6)">6</button>
    <button onclick="sendOption(7)">7</button>
    <button onclick="sendOption(8)">8</button>
    <button onclick="sendOption(9)">9</button>
  </div>
  
  <div id="msg"></div>

  <div>
    <img src="https://i0.wp.com/walfiegif.wordpress.com/wp-content/uploads/2023/07/out-transparent-116.gif?resize=560%2C753&ssl=1">
  </div>

  <script>
    function sendOption(num) {
      fetch('/seleccion?num=' + num)
        .then(res => res.text())
        .then(data => {
          document.getElementById("msg").innerText = "Secuencia " + num + " ejecutada";
        })
        .catch(err => {
          document.getElementById("msg").innerText = "Error de conexión";
        });
    }
  </script>
</body>
</html>
"""

# ---------------------------
# Servidor Web
# ---------------------------
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Servidor corriendo en -> http://{}".format(ip))

while True:
    cl, addr = s.accept()
    request = cl.recv(1024).decode()
    
    if "GET /seleccion?num=" in request:
        num = request.split("num=")[1].split(" ")[0]
        if num in secuencias:
            secuencias[num]()  # Ejecuta la secuencia
            response = "Secuencia {} ejecutada".format(num)
        else:
            response = "Opción inválida"
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + response)
    else:
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html)
    
    cl.close()
