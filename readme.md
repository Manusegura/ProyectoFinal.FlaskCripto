# Aplicación Web de registro, cambio y tradeo de criptomonedas

- Programa hecho en python con el framework Flask, con motor de base de datos SQLite.


## Creamos el entorno virtual
```
Si es windows```python -m venv <nombre del entorno virtual>``` y si es mac ```python3 -m venv <nombre del entorno virtual>```
```
## Activamos el entorno virtual
```
Si es windows```.<nombre del entorno virtual>\Scripts\activate``` y si es mac ```source/<nombre del entorno virtual>/bin/activate```
```

## En su entorno de python ejecutar el comando
```
pip install -r requirements.txt
```
## Renombrar el archivo .env_template a .env y agregar las siguientes lineas
```
FLASK_APP=main.py
FLASK_DEBUG=true
```
## Renombrar el archivo .config_template a .config.
```
Dentro de config_template encontrará las instrucciones:
- Introducir ruta de la base de datos.
- Introducir una clave secreta propia
- Introducir la Api Key propia, puede descargarla en: https://www.coinapi.io
```
## Obtener la api Key
```
Dentro de config_template encontrará las instrucciones, 
```
## Creación de base de datos.
```
Descargar gestor de BBDD sqlite en el siguiente enlace: https://www.sqlite.org/download.html
Abrir el archivo ```data/movimientos.sqlite```.
```
## Ejecucion del programa con el .env
```
flask run
```

## funcionamiento:
Página de Inicio:
- Encontrará los movimientos de sus registros de compra y venta de criptomonedas/euros.
- Si no existen movimientos, aparecerá el mensaje 'No hay movimientos'.
- Tendrá un botón para pasar a la página de compra y otro para la página de estado.

Página de Compra:
- Deberá elegir dos monedas diferentes y una cantidad mayor a '0' para realizar el cálculo, a continuación pulse calcular.
- Si está de acuerdo, pulse aceptar, la compra será realizada y el movimiento quedará registrado en Inicio.

Página de Estado:
    Encontrará los siguientes datos:
- Invertido: Es el total de euros con el que se han comprado Criptomonedas.
- Recuperado: Es el total de euros obtenidos con la venta de cualquier Criptomoneda.
- Valor de compra: Es el resultado de Invertido menos Recuperado.
- Valor actual: Es el valor actual de Criptomonedas que tenemos en nuestra cartera expresado en Euros:
    - Si el Valor actual es mayor que el valor de compra, la cifra aparecerá en verde.
    - Si el Valor actual es igual que el valor de compra, la cifra aparecerá en naranja.
    - Si el Valor actual es menor que el valor de compra, la cifra aparecerá en rojo.
- Ganancia : Es el valor si vendieramos toda nuestra cartera en ese momento ( Valor actual - Valor de compra):
    - Si la ganancia es positiva, la cifra aparecerá en verde.
    - Si la ganancia es cero, la cifra aparecerá en naranja.
    - Si la ganancia es negativa, la cifra aparecerá en rojo.





