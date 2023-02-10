import sqlite3
from reg_criptomoneda.conexion import Conexion
import requests
from config import *

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

# Añadar registros
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
        raise APIError(resultado.status_code)

        
#Errores Consulta Api
class APIError(Exception):
    def __init__(self, code):
        if code == 204:
            error = "Error 204__No content, se ha aceptado la solicitud, pero no hay datos para devolver."
        if code == 400:
            error = "Error 400__Bad Request,La solicitud no fue válida. El servidor ha intentado procesar la solicitud, pero algún aspecto de la solicitud no es válido."
        elif code == 401:
            error = "Error 401__Unauthorized, Está habilitada la seguridad y falta la información de autorización en la solicitud."
        elif code == 403:
            error = "Error 403__Forbidden, Ha intentado acceder a un recurso al que no tiene acceso."
        elif code == 404:
            error = "Error 404__Not found, Indica que el recurso de destino no existe."    
        elif code == 429:
            error = "Error 429__Demasiadas solicitudes, superó el límite de solicitudes en una cantidad de tiempo especificada"
        elif code == 500:
            error = "Error 500__Error interno del servidor."    
        else:
            error = "Ha ocurrido un error. Por favor revise su conexión a Internet e inténtelo de nuevo mas tarde."
        super().__init__(error)    



# Calcular el valor total de las monedas en EUR
def consulta_total_cripto():
    monedas = ['EUR','BTC','ETH','BNB','XRP','ADA','USDT','SOL','DOT','MATIC']
    resultado = 0
    con = sqlite3.connect(ORIGIN_DATA)
    cur = con.cursor()

    dict_cripto = {}
    for moneda in monedas:
        consulta = f"SELECT ((SELECT COALESCE(SUM(cantidad_to), 0) as tot FROM movimientos WHERE moneda_to = '{moneda}') - (SELECT COALESCE(SUM(cantidad_from), 0) as ee FROM movimientos WHERE moneda_from = '{moneda}')) AS {moneda}"
        cur.execute(consulta)
        dict_cripto[moneda] = cur.fetchone()[0]
    con.close()

    url = requests.get(f"https://rest.coinapi.io/v1/exchangerate/EUR?&apikey={API_KEY}")
    if url.status_code != 200:
        raise APIError(url.status_code)

    valores = url.json()

    for moneda in dict_cripto.keys():
        for tasa in valores['rates']:
            if tasa['asset_id_quote'] == moneda:
                resultado += dict_cripto[moneda] * 1/tasa['rate']

    return resultado


#Suma de cantidad de Euros desde la moneda_from (Invertido)
def select_from():
            consulta = Conexion("SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from='EUR'")
            select = consulta.cur.fetchone()
            consulta.con.commit()
            consulta.con.close()
            return select    

#Suma de cantidad de Euros desde la moneda_to (Recuperado)
def select_to():
            consulta = Conexion("SELECT sum(cantidad_to) FROM movimientos WHERE moneda_to='EUR'")
            select = consulta.cur.fetchone()
            consulta.con.commit()
            consulta.con.close()
            return select      



#Suma total de moneda_to en cantidad_to
def consultar_saldo_compras(monedas):
        saldo = Conexion("SELECT sum(cantidad_to) FROM movimientos WHERE moneda_to = '" + \
            monedas + "'")
        resultado = saldo.cur.fetchone()
        saldo.con.commit()
        saldo.con.close()
        return resultado
#Suma total de moneda_from en cantidad_from
def consultar_saldo_ventas(monedas):
        saldo = Conexion("SELECT sum(cantidad_from) FROM movimientos WHERE moneda_from = '" + \
            monedas + "'")
        resultado = saldo.cur.fetchone()
        saldo.con.commit()
        saldo.con.close()
        return resultado        

#Calcular si se dispone de saldo para la compra de criptomonedas
def calcular_saldo(monedas):
        datos_compras = consultar_saldo_compras(monedas)
        datos_ventas = consultar_saldo_ventas(monedas)
        if datos_ventas[0] == None and datos_compras[0] == None:
            return 0
        elif datos_ventas[0] == None:
            return datos_compras[0]
        elif datos_compras[0] == None:
            return 0
        else:
            return datos_compras[0] - datos_ventas[0]

                


           



           