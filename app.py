from flask import Flask, render_template, request, redirect, url_for  # type: ignore  
from flask_sqlalchemy import SQLAlchemy  # type: ignore  

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pacientes.db'  # Banco de dados SQLite  
app.config['SECRET_KEY'] = 'sua_chave_secreta'  # Adicione uma chave secreta  
db = SQLAlchemy(app)  


class Paciente(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    nome = db.Column(db.String(100), nullable=False)  
    idade = db.Column(db.Integer)  
    cpf = db.Column(db.String(14))  
    peso = db.Column(db.Float)  
    altura = db.Column(db.Float)  
    sexo = db.Column(db.String(10))  # Adicionado campo sexo  
    objetivo = db.Column(db.String(120))  
    descricao = db.Column(db.String(200))  

    def __repr__(self):  
        return f"Paciente('{self.nome}', '{self.idade}')"  


# Recria o banco de dados (APENAS PARA DESENVOLVIMENTO - REMOVA PARA PRODUÇÃO!)  
with app.app_context():  
    db.drop_all()  # Apaga todas as tabelas  
    db.create_all()  # Recria as tabelas com as novas definições  


@app.route('/', methods=['GET', 'POST'])  
def index():  
    if request.method == 'POST':  
        nome = request.form['nome']  
        idade = request.form['idade']  
        cpf = request.form['cpf']  
        peso = request.form['peso']  
        altura = request.form['altura']  
        sexo = request.form['sexo']  # Obtém o sexo do formulário  
        descricao = request.form['descricao']  
        objetivo = request.form['objetivo']  

        novo_paciente = Paciente(nome=nome, idade=idade, cpf=cpf, peso=peso, altura=altura, sexo=sexo, descricao=descricao, objetivo=objetivo)  
        db.session.add(novo_paciente)  
        db.session.commit()  
        return redirect(url_for('index'))  # Redireciona para a página inicial após adicionar  
    return render_template('index.html')  


@app.route('/pesquisar', methods=['GET', 'POST'])  
def pesquisar():  
    resultados = []  
    if request.method == 'POST':  
        nome = request.form.get('nome')  
        cpf = request.form.get('cpf')  
        # Construa a consulta com base nos parâmetros de pesquisa  
        query = Paciente.query  
        if nome:  
            query = query.filter(Paciente.nome.contains(nome))  
        if cpf:  
            query = query.filter(Paciente.cpf == cpf)  
        resultados = query.all()  
        return render_template('resultados_pesquisa.html', resultados=resultados)  
    else:  
        return render_template('pesquisar.html')  # Exibe o formulário de pesquisa  


@app.route('/editar/<int:id>', methods=['GET', 'POST'])  
def editar(id):  
    paciente = Paciente.query.get_or_404(id)  # Busca o paciente ou retorna um erro 404  
    if request.method == 'POST':  
        paciente.nome = request.form['nome']  
        paciente.idade = request.form['idade']  
        paciente.cpf = request.form['cpf']  
        paciente.peso = request.form['peso']  
        paciente.altura = request.form['altura']  
        paciente.sexo = request.form['sexo']  # Atualiza o sexo  
        paciente.descricao = request.form['descricao']  
        paciente.objetivo = request.form['objetivo']  
        db.session.commit()  
        return redirect(url_for('pesquisar'))  # Redireciona de volta para a página de pesquisa  
    return render_template('editar.html', paciente=paciente)  


@app.route('/relatorio/<int:id>')  
def relatorio(id):  
    paciente = Paciente.query.get_or_404(id)  
    return render_template('relatorio.html', paciente=paciente)  


@app.route('/peso_ideal', methods=['GET', 'POST'])  
def calcular_peso_ideal():  
    peso_ideal = None  
    if request.method == 'POST':  
        sexo = request.form['sexo']  
        altura = float(request.form['altura'])  
        peso_atual = float(request.form['peso'])  

        if sexo == 'Masculino':  
            peso_ideal = 72.7 * altura - 58  
        else:  
            peso_ideal = 62.1 * altura - 44.7  

    return render_template('peso_ideal.html', peso_ideal=peso_ideal)  


if __name__ == '__main__':  
    app.run(debug=True)  