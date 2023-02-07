from reg_criptomoneda import app
from flask import render_template,request,redirect,url_for,flash
from datetime import date,datetime
from reg_criptomoneda.models import *
from reg_criptomoneda.forms import MovementsForm      
from config import *       
from wtforms.validators import DataRequired,ValidationError 




#Inicio
@app.route("/")
def index():
    try:
        movimientos = consultaSql()
        return render_template("index.html",movements = movimientos)
    except:
        flash("Error en la base de datos")
        return render_template("index.html")





   
#Compra
@app.route("/purchase", methods=["GET", "POST"])
def compra():
    
    if request.method == "GET":
        form = MovementsForm()
        return render_template("purchase.html", form=form)
    else:
        try:
            form = MovementsForm(data=request.form)

            moneda_from = form.coin_from.data
            moneda_to = form.coin_to.data
            cantidad_from = form.quantity_from.data
            cantidad_from = float(round(cantidad_from, 8))

            
            calc = consulta_api(moneda_from,moneda_to)
            calc = float(round(calc, 8))
            cantidad_to = cantidad_from * calc
            cantidad_to = float(round(cantidad_to, 8))

            saldo = calcular_saldo(moneda_from)
            if moneda_from != "EUR" and saldo < float(cantidad_from):
                flash("No tienes suficientes monedas {} ".format(moneda_from))
                return render_template("purchase.html", form=form)
            
            
                
            if form.calcular.data:
                if moneda_from == moneda_to:
                   flash("·Debes seleccionar dos monedas diferentes")
                if cantidad_from <= 0.00001 or cantidad_from >= 99999999:
                       flash("·Por favor, introduzca un numero positivo")
                else:    
                    return render_template("purchase.html", form=form, quantity_to=cantidad_to,quantity_from=cantidad_from)
        except APIError as err:
            flash(err)
            return render_template("purchase.html", form=form)

        if form.aceptar.data:  
            form = MovementsForm(data=request.form)
            moneda_from = str(form.coin_from.data)
            moneda_to = str(form.coin_to.data)
            cantidad_from = float(cantidad_from)
            form.date.data = date.today()
            fecha = form.date.data
            form.hora.data = datetime.today().strftime("%H:%M:%S")
            hora = form.hora.data
            params = (fecha, hora, moneda_from,cantidad_from, moneda_to, cantidad_to)
            resultado = insert(params)

            if resultado:
                flash("Movimiento actualizado correctamente")
                return redirect(url_for("index"))

            else:
                return render_template("purchase.html", form=form, cantidad_to=cantidad_to, errores=["Error conexión SQL"])

        else:
            return redirect(url_for("compra"))
       
        
        
        
#Estado        
@app.route("/status", methods=["GET"])
def estado():
    try:
        euros_to = select_to() #recuperado
        euros_to = euros_to[0]
        if euros_to == None:
            euros_to = 0
        euros_from = select_from() #Invertido
        euros_from = euros_from[0]
        if euros_from == None:
            euros_from = 0
        saldo_euros_invertidos = euros_from - euros_to # Valor de compra

        saldo_euros_invertidos = round(saldo_euros_invertidos, 2) #Valor de compra(redondeado)
        total_euros_invertidos = round(euros_from, 2) #Invertido (redondeado)
        recuperado = round(euros_to, 2) #Recuperado (redondeado)
       
        try:
            
            valor_actual = consulta_total_cripto()#Valor actual 
            valor_actual = round(valor_actual, 2)#Valor actual redondeado
          

            return render_template("status.html",total_euros_invertidos=total_euros_invertidos,saldo_euros_invertidos=saldo_euros_invertidos,recuperado=recuperado,valor_actual=valor_actual)
        except APIError:
            flash("Error en la consulta de STATUS con el servidor (API)",
            category="fallo")
            return render_template("status.html")
    except:
        flash("No hay movimientos en tu base de datos SQLITE, ahora mismo no podemos calcular",
            category="fallo")
        return render_template("status.html")


       