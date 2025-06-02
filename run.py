# run.py
from frontend_web import create_app
import threading
import webbrowser
import time

app = create_app()

def abrir_navegador():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000/tabla-paquete")  # sin "s"

if __name__ == '__main__':
    threading.Thread(target=abrir_navegador).start()
    app.run(debug=True, use_reloader=False)
