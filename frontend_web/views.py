# frontend_web/views.py
from flask import Blueprint, render_template, request
from database import *


views = Blueprint('views', __name__)

@views.route('/tabla-paquete')
def tabla_paquete():
    estado = request.args.get('estado', type=int)
    if estado in [1, 2, 3]:
        paquetes = obtener_paquetes_por_estado(estado)
    else:
        paquetes = obtener_todos_los_paquetes()
    return render_template('tabla_paquete.html', paquetes=paquetes, estado_actual=estado)
