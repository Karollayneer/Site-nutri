from flask_sqlalchemy import SQLAlchemy   # type: ignore

db = SQLAlchemy()  # Certifique-se de ter instanciado o SQLAlchemy  

class Paciente(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    nome = db.Column(db.String(200), nullable=False)  
    idade = db.Column(db.Integer)  
    cpf = db.Column(db.String(20))  
    peso = db.Column(db.Float)  
    altura = db.Column(db.Float)  
    sexo = db.Column(db.String(20))  # Adicione esta linha  
    objetivo = db.Column(db.Text)  
    descricao = db.Column(db.Text)  

    def __repr__(self):  
        return f'<Paciente {self.nome}>'  