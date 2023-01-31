from reg_criptomoneda import app
from flask import render_template,request,redirect,url_for,flash
from datetime import date,datetime
from reg_criptomoneda.models import *
from reg_criptomoneda.forms import MovementsForm      
from config import *       
from wtforms.validators import DataRequired,ValidationError 


@app.route("/")
def index():
    movimientos = consultaSql()
    return render_template("index.html",movements = movimientos)
    '''try:
        movimientos = consultaSql()
        return render_template("index.html",movements = movimientos)
    except:
        flash("Error en la base de datos")
        return render_template("index.html")'''
   

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

            
                
            if form.calcular.data:
                if moneda_from == moneda_to:
                   flash("·Debes seleccionar dos monedas diferentes")
                if cantidad_from <= 0.00001 or cantidad_from >= 99999999:
                       flash("·Por favor, introduzca un numero positivo")
                else:    
                    return render_template("purchase.html", form=form, quantity_to=cantidad_to,quantity_from=cantidad_from)

        except api_errors as error:
            flash(error)
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
                return render_template("purchase.html", form=form, cantidad_to=cantidad_to, errores=["Ha fallado la conexión con las Base de datos"])

        else:
            return redirect(url_for("mercado"))
       
        
        
        
        
@app.route("/status", methods=["GET"])
def estado():
   pass
