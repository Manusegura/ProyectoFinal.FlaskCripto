import sqlite3
from reg_criptomoneda.conexion import Conexion
import requests
from config import API_KEY,ORIGIN_DATA,SECRET_KEY

#Actualización movimientos Inicio, Actualización estado inversiones
def consultaSql():
    consultaSql = Conexion("SELECT * FROM movimientos ORDER BY date")
    filas = consultaSql.cur.fetchall()
    columnas = consultaSql.res.description

    movimientos = []
    nombres_columnas = []

    for desc_columna in columnas:
        nombres_columnas.append(desc_columna[0])

    for fila in filas:
        movimiento = {}
        indice = 0
        for nombre in nombres_columnas:
            movimiento[nombre] = fila[indice]
            indice += 1
        movimientos.append(movimiento)
    consultaSql.con.close()

    return movimientos


def insert(params):
        registro = Conexion("INSERT INTO movimientos (date, time, moneda_from, cantidad_from, moneda_to, cantidad_to) VALUES (?,?,?,?,?,?)",params)
        try:
            registro
            registro.con.commit()
        except Exception as error:
            print("ERROR SQLITE:", error)
            registro.con.rollback()
        registro.con.close()

        return registro      


#Consulta Api Criptomoneda
def consulta_api(origen,destino):
    moneda_origen = origen
    moneda_destino = destino
    cambio = 0.0
    resultado = requests.get(f'https://rest.coinapi.io/v1/exchangerate/{moneda_origen}/{moneda_destino}?apikey={API_KEY}')

    if resultado.status_code == 200:
        cambio = resultado.json()["rate"]
        return(cambio)

    else:
        raise api_errors(resultado.status_code)

#Errores Consulta Api

def api_errors(code):
    if code == 204:
        error = "No content, se ha aceptado la solicitud, pero no hay datos para devolver."
    if code == 400:
        error = "Bad Request,La solicitud no fue válida. El servidor ha intentado procesar la solicitud, pero algún aspecto de la solicitud no es válido."
    elif code == 401:
        error = "Unauthorized, Está habilitada la seguridad y falta la información de autorización en la solicitud."
    elif code == 403:
        error = "Forbidden, Ha intentado acceder a un recurso al que no tiene acceso."
    elif code == 404:
        error = "Not found, Indica que el recurso de destino no existe."    
    elif code == 429:
        error = "Demasiadas solicitudes, superó el límite de solicitudes en una cantidad de tiempo especificada."
    elif code == 500:
        error = "Error interno del servidor."    
    else:
        error = "Ha ocurrido un error. Por favor revise su conexión a Internet e inténtelo de nuevo mas tarde."
    return error 



    