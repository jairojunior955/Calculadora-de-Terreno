from flask import Flask, redirect, render_template, request, url_for, flash, session
# from views import views
from packages.Database.database import Query as query, Query
from packages.calculate_area.calculo_de_terreno import Rectangle, Elipse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pppppp'


class Login:
    def __init__(self, login):
        self.login = login


@app.route('/')
@app.route('/cadastro')
def cadastro():
    return render_template('Cadastro.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('Login.html')


@app.route('/validate', methods=["POST"])
def validate():
    if request.method == 'POST':
        login_user = request.form['login']
        password = request.form['password']
        if query().auth_user(f'{login_user}', f'{password}'):
            if login_user is not None:
                session['login'] = login_user
                return render_template('Index.html', login_user=login_user)
            else:
                redirect(url_for("login"))
        else:
            return redirect(url_for("login"))


@app.route('/register', methods=['POST', 'GET'])
def register():
    login = request.form['login']
    password = request.form['password']
    check = query().check_exists('login')
    if not check:
        query().register_user(f'{login}', f'{password}')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('cadastro'))


@app.route('/erro')
def erro():
    return render_template('CadastroErro.html')


@app.route('/index', methods=['POST', 'GET'])
def index():
    if 'login' in session:
        login_user = session['login']
        return render_template('Index.html', login_user=login_user)
    else:
        return redirect(url_for('login'))


@app.route('/gerar', methods=['POST', 'GET'])
def gerar():
    if request.method == 'POST':
        formato = request.form['option']
        arealote = float(request.form['area-lote'])
        xE = float(request.form['x-extra'])
        yE = float(request.form['y-extra'])
        custo = float(request.form['custo'])
        user = session['login']
        if formato == 'RECTANGLE':
            area = Rectangle().calculate_area_rectangle(xE, yE, arealote)
            custoTotal = round(Rectangle().calculate_cost(area[2], custo), 2)
            area = [round(i, 2) for i in area]
            Query().log_generator(user, xE, yE, arealote, area[2], area[1], area[0], custo)
            return render_template('Resultado.html', resposta=area, custo=custoTotal)
        if formato == 'ELIPSE':
            area = Elipse().calculate_area_elipse(xE, yE, arealote)
            custoTotal = round(Elipse().calculate_cost(area[2], custo), 2)
            area = [round(i, 2) for i in area]
            Query().log_generator(user, xE, yE, arealote, area[2], area[1], area[0], custo)
            return render_template('Resultado.html', resposta=area, custo=custoTotal)
    return render_template('Index.html')


@app.route('/historico', methods=['POST'])
def historico():
    print(session)
    if 'login' in session:
        user = session['login']
        historico = Query().get_log(user)
        print(historico)
        return render_template('Historico.html', historico=historico)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
