from flask_wtf import FlaskForm
from wtforms import SelectField,TimeField,DateField,FloatField,HiddenField,SubmitField
from wtforms.validators import DataRequired

class MovementsForm(FlaskForm):
    id = HiddenField()
    date = DateField('Fecha')
    hora = TimeField('Hora')

    coin_from = SelectField('Moneda elegida',choices= [('EUR','EUR'),('BTC','BTC'),('ETH','ETH'),('USDT','USDT'),
    ('BNB','BNB'),('XRP','XRP'),('ADA','ADA'),('SOL','SOL'),('DOT','DOT'),('MATIC','MATIC')
    ],validators = [DataRequired()])

    quantity_from = FloatField('Q',validators=[DataRequired()])

    coin_to = SelectField("Moneda comprada",choices= [('EUR','EUR'),('BTC','BTC'),('ETH','ETH'),('USDT','USDT'),
    ('BNB','BNB'),('XRP','XRP'),('ADA','ADA'),('SOL','SOL'),('DOT','DOT'),('MATIC','MATIC')
    ],validators = [DataRequired()])

    quantity_to = FloatField("Cantidad to",validators=[DataRequired()])


    
    aceptar = SubmitField("Aceptar")
    
    borrar = SubmitField("Borrar")

    calcular= SubmitField("calcular")
   
