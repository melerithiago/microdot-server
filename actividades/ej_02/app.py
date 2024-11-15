from boot import do_connect
from microdot import Microdot, send_file
import machine
import neopixel
import time

do_connect()
app = Microdot()

leda = machine.Pin(32, machine.Pin.OUT)
ledb = machine.Pin(33, machine.Pin.OUT)
ledc = machine.Pin(25, machine.Pin.OUT)

np = neopixel.NeoPixel(machine.Pin(27), 8)

@app.route('/')
async def index(request):
    return send_file('index.html')

@app.route('/<dir>/<file>')
async def static_file(request, dir, file):
    return send_file(f"/{dir}/{file}")

@app.route('/led')
async def led_control(request):
    led_num = int(request.args.get('led'))
    state = request.args.get('state') == 'true'
    print(f"Controlando LED {led_num}, su condición es: {state}")
    led = [leda, ledb, ledc][led_num - 1]
    if state:
        led.on()
    else:
        led.off()
    return f'LED {led_num} {"Andando" if state else "Apagado"}'

@app.route('/color')
async def color_control(request):
    # Obtener los valores RGB desde los parámetros de la URL
    r = int(request.args.get('r'))
    g = int(request.args.get('g'))
    b = int(request.args.get('b'))

    # Mostrar los valores de color en la consola
    print(f"Estableciendo color de tira LED: Rojo:{r}, Verde:{g}, Azul:{b}")
    
    # Configurar todos los LEDs de la tira al color especificado
    np.fill((r, g, b))
    np.write()

    # Retornar una respuesta indicando el color establecido
    return f'Color establecido a Rojo:{r}, Verde:{g}, Azul:{b}'

app.run(port=80)# Aplicacion del servidor
