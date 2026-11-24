from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    """!
    Endpoint para saludar al usuario.

    @param name (str): Nombre del usuario recibido por query string.
    @return str: Mensaje de saludo personalizado.
    """
    name = request.args.get('name', 'Mundo')
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
