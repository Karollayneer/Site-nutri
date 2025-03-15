from flask import Flask, render_template, request, redirect, url_for   # type: ignore  
from flask_sqlalchemy import SQLAlchemy   # type: ignore  

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pacientes.db'  
app.config['SECRET_KEY'] = 'sua_chave_secreta'  
db = SQLAlchemy(app)  


class Paciente(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    nome = db.Column(db.String(100), nullable=False)  
    idade = db.Column(db.Integer)  
    cpf = db.Column(db.String(14))  
    peso = db.Column(db.Float)  
    altura = db.Column(db.Float)  
    sexo = db.Column(db.String(10))  
    objetivo = db.Column(db.String(120))  
    descricao = db.Column(db.String(200))  

    def __repr__(self):  
        return f"Paciente('{self.nome}', '{self.idade}')"  


# Criar o banco de dados apenas se ele não existir  
with app.app_context():  
    db.create_all()  

    # Adicionar um paciente de teste caso o banco esteja vazio  
    if Paciente.query.first() is None:  
        paciente_teste = Paciente(  
            nome="Paciente Teste",  
            idade=30,  
            cpf="000.000.000-00",  
            peso=70.0,  
            altura=1.75,  
            sexo="Masculino",  
            objetivo="Saúde",  
            descricao="Paciente de teste"  
        )  
        db.session.add(paciente_teste)  
        db.session.commit()  


@app.route('/', methods=['GET', 'POST'])  
def index():  
    if request.method == 'POST':  
        nome = request.form['nome']  
        idade = request.form['idade']  
        cpf = request.form['cpf']  
        peso = request.form['peso']  
        altura = request.form['altura']  
        sexo = request.form['sexo']  
        descricao = request.form['descricao']  
        objetivo = request.form['objetivo']  

        novo_paciente = Paciente(  
            nome=nome, idade=idade, cpf=cpf, peso=peso, altura=altura,   
            sexo=sexo, descricao=descricao, objetivo=objetivo  
        )  
        db.session.add(novo_paciente)  
        db.session.commit()  
        return redirect(url_for('index'))  
    return render_template('index.html')  


@app.route('/pesquisar', methods=['GET', 'POST'])  
def pesquisar():  
    resultados = []  
    if request.method == 'POST':  
        nome = request.form.get('nome')  
        cpf = request.form.get('cpf')  
        query = Paciente.query  
        if nome:  
            query = query.filter(Paciente.nome.contains(nome))  
        if cpf:  
            query = query.filter(Paciente.cpf == cpf)  
        resultados = query.all()  
        return render_template('resultados_pesquisa.html', resultados=resultados)  
    return render_template('pesquisar.html')  


@app.route('/editar/<int:id>', methods=['GET', 'POST'])  
def editar(id):  
    paciente = Paciente.query.get_or_404(id)  
    if request.method == 'POST':  
        paciente.nome = request.form['nome']  
        paciente.idade = request.form['idade']  
        paciente.cpf = request.form['cpf']  
        paciente.peso = request.form['peso']  
        paciente.altura = request.form['altura']  
        paciente.sexo = request.form['sexo']  
        paciente.descricao = request.form['descricao']  
        paciente.objetivo = request.form['objetivo']  
        db.session.commit()  
        return redirect(url_for('pesquisar'))  
    return render_template('editar.html', paciente=paciente)  


@app.route('/relatorio/<int:id>')  
def relatorio(id):  
    paciente = Paciente.query.get_or_404(id)  
    return render_template('relatorio.html', paciente=paciente)  


@app.route('/excluir/<int:id>', methods=['POST'])  
def excluir(id):  
    paciente = Paciente.query.get_or_404(id)  
    db.session.delete(paciente)  
    db.session.commit()  
    return redirect(url_for('pesquisar'))  


if __name__ == '__main__':  
    app.run(debug=True)  