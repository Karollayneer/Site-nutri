# forms.py  
from flask_wtf import FlaskForm   # type: ignore
from wtforms import StringField, FloatField, SubmitField, SelectField   # type: ignore
from wtforms.validators import DataRequired   # type: ignore

class PesoIdealForm(FlaskForm):  
    sexo = SelectField('Sexo', choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], validators=[DataRequired()])  
    altura = FloatField('Altura (em metros)', validators=[DataRequired()])  
    peso_atual = FloatField('Peso Atual (em kg)', validators=[DataRequired()])  
    calcular = SubmitField('Calcular Peso Ideal')  