from flask import Flask, request
import mysql.connector
import json

# Configuración de la base de datos
db = mysql.connector.connect(user='root', password='123',
                              host='192.168.0.7',
                              database='nombre')

app = Flask(__name__)

# Definición de ruta para enviar datos
@app.route('/enviar_datos', methods=['POST'])
def enviar_datos():
    nombre = request.form['nombre']
    carnet = request.form['carnet']

    cursor = db.cursor()
    cursor.execute("INSERT INTO nombres (nombres, carnet) VALUES (%s, %s)", (nombre, carnet))
    db.commit()
    cursor.close()

    return 'Datos enviados correctamente'

# Obtener todos los datos
@app.route('/obtener_datos', methods=['GET'])
def obtener_datos():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM nombres")
    datos = cursor.fetchall()
    cursor.close()

    resultados = []
    for dato in datos:
        resultado = {
            'carnet': dato[0],
            'nombre': dato[1]
        }
        resultados.append(resultado)

    return json.dumps(resultados, ensure_ascii=False)

# Actualizar un registro existente
@app.route('/actualizar_datos/<carnet>', methods=['PUT'])
def actualizar_datos(carnet):
    nuevo_nombre = request.json['nombre']

    cursor = db.cursor()
    cursor.execute("UPDATE nombres SET nombres=%s WHERE carnet=%s", (nuevo_nombre, carnet))
    db.commit()
    cursor.close()

    return 'Datos actualizados correctamente'


# Eliminar un registro existente
@app.route('/eliminar_datos/<carnet>', methods=['DELETE'])
def eliminar_datos(carnet):
    cursor = db.cursor()
  
    cursor.execute("DELETE FROM nombres WHERE carnet=%s", (carnet,))
    db.commit()
    cursor.close()
    return 'Datos eliminados correctamente'

if __name__ == '__main__':
    app.run(debug=True)

