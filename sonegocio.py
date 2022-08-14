from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://ecommerce:123456@localhost:3306/sonegocio"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column("idusuario", db.Integer, primary_key=True)
    nome = db.Column("user_nome", db.String(256))
    email = db.Column("user_email", db.String(256))
    senha = db.Column("user_senha", db.String(256))
    end = db.Column("user_end", db.String(256))
    telefone = db.Column("user_telefone", db.String(256))

    def __init__(self, nome, email, senha, end, telefone):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.end = end
        self.telefone = telefone

class Favorito(db.Model):
    __tablename__ = "favorito"
    id = db.Column("idfavorito", db.Integer, primary_key=True)
    idanuncio = db.Column("anunc_idanuncio", db.Integer, db.ForeignKey("anuncio.idanuncio"))
    idusuario = db.Column("user_idusuario", db.Integer, db.ForeignKey("usuario.idusuario"))

    def __init__(self, idanuncio, idusuario):
        self.idanuncio = idanuncio
        self.idusuario = idusuario

class Compra(db.Model):
    __tablename__ = "compra"
    id = db.Column("idcompra", db.Integer, primary_key=True)
    preco = db.Column("com_preco", db.Float)
    qtd = db.Column("com_qtd", db.Integer)
    total = db.Column("com_total", db.Float)
    idanuncio = db.Column("anunc_idanuncio", db.Integer, db.ForeignKey("anuncio.idanuncio"))
    idusuario = db.Column("user_idusuario", db.Integer, db.ForeignKey("usuario.idusuario"))

    def __init__(self, preco, qtd, total, idanuncio, idusuario):
        self.preco = preco
        self.qtd = qtd
        self.total = total
        self.idanuncio = idanuncio
        self.idusuario = idusuario

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column("idcategoria", db.Integer, primary_key=True)
    nome = db.Column("cat_nome", db.String(256))
    desc = db.Column("cat_desc", db.String(256))

    def __init__(self, nome, desc):
        self.nome = nome
        self.desc = desc

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column("idanuncio", db.Integer, primary_key=True)
    nome = db.Column("anunc_nome", db.String(256))
    desc = db.Column("anunc_desc", db.String(256))
    qtd = db.Column("anunc_qtd", db.Integer)
    preco = db.Column("anunc_preco", db.Float)
    idusuario = db.Column("user_idusuario", db.Integer, db.ForeignKey("usuario.idusuario"))
    idcategoria = db.Column("cat_idcategoria", db.Integer, db.ForeignKey("categoria.idcategoria"))

    def __init__(self, nome, desc, qtd, preco, idusuario, idcategoria):
        self.nome = nome
        self.desc = desc
        self.qtd = qtd
        self.preco = preco
        self.idusuario = idusuario
        self.idcategoria = idcategoria

class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column("idPergunta", db.Integer, primary_key=True)
    pergunta = db.Column("per_pergunta", db.String(256))
    resposta = db.Column("per_resposta", db.String(256))
    idusuario = db.Column("user_idusuario", db.Integer, db.ForeignKey("usuario.idusuario"))
    idanuncio = db.Column("anunc_idanuncio", db.Integer, db.ForeignKey("anuncio.idanuncio"))

    def __init__(self, pergunta, resposta, idusuario, idanuncio):
        self.pergunta = pergunta
        self.resposta = resposta
        self.idusuario = idusuario
        self.idanuncio = idanuncio

@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template("error404.html")

@app.errorhandler(500)
def paginanaoencontrada(error):
    return render_template("error500.html")

@app.route("/")
def index():
    return render_template("index.html", usuarios= Usuario.query.all(), anuncios = Anuncio.query.all(), categorias = Categoria.query.all())

@app.route("/cad/categoria/")
def categoria():
    return render_template("categoria.html", categorias = Categoria.query.all(), titulo="Cadastro de Categoria")

@app.route("/categoria/criar", methods=['POST'])
def criarcategoria():
    categoria = Categoria(request.form.get("nome"), request.form.get("desc"))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for("categoria"))

@app.route("/categoria/detalhar/<int:id>")
def buscarcategoria(id):
    return render_template("cat_detalhes.html", categorias = Categoria.query.get(id), anuncio = Anuncio.query.all())

@app.route("/categoria/editar/<int:id>", methods=['GET','POST'])
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == "POST":
        categoria.nome = request.form.get("nome")
        categoria.desc = request.form.get("desc")
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for("categoria"))
    return render_template("cat_editar.html", categoria = categoria, titulo="Editar Categoria")

@app.route("/categoria/deletar/<int:id>")
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for("categoria"))

@app.route("/cad/usuario/")
def usuario():
    return render_template("usuario.html", usuarios = Usuario.query.all(), titulo="Cadastro de Usuário")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    usuario = Usuario(request.form.get("user"), request.form.get("email"),request.form.get("passwd"),request.form.get("end"), request.form.get("telefone"))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for("usuario"))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    return render_template("user_detalhes.html", usuarios = Usuario.query.get(id))

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == "POST":
        usuario.nome = request.form.get("user")
        usuario.email = request.form.get("email")
        usuario.senha = request.form.get("passwd")
        usuario.end = request.form.get("end")
        usuario.telefone = request.form.get("telefone")
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for("usuario"))
    return render_template("user_editar.html", usuario = usuario, titulo="Editar Usuário")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("usuario")) 

@app.route("/cad/anuncio/")
def anuncio():
    return render_template("anuncio.html",usuarios= Usuario.query.all(), anuncios = Anuncio.query.all(), categorias = Categoria.query.all(), titulo="Cadastro de Anúncio")

@app.route("/anuncio/criar", methods=['POST'])
def criaranuncio():
    anuncio = Anuncio(request.form.get("nome"), request.form.get("desc"),request.form.get("qtd"),request.form.get("preco"), request.form.get("user"), request.form.get("cat"))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for("anuncio"))

@app.route("/anuncio/detalhar/<int:id>")
def buscaranuncio(id):
    return render_template("anunc_detalhes.html", anuncios = Anuncio.query.get(id), usuarios= Usuario.query.all(), categorias = Categoria.query.all())

@app.route("/anuncio/editar/<int:id>", methods=['GET','POST'])
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == "POST":
        anuncio.nome = request.form.get("nome")
        anuncio.desc = request.form.get("desc")
        anuncio.qtd = request.form.get("qtd")
        anuncio.preco = request.form.get("preco")
        anuncio.idusuario = request.form.get("user")
        anuncio.idcategoria = request.form.get("cat")
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for("anuncio"))
    return render_template("anunc_editar.html", anuncio = anuncio, titulo="Editar Anúncio", usuarios= Usuario.query.all(), categorias = Categoria.query.all())

@app.route("/anuncio/deletar/<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for("anuncio")) 

@app.route("/anunc/pergunta/")
def pergunta():
    return render_template("pergunta.html", perguntas = Pergunta.query.all())

@app.route("/anunc/fazerpergunta/<int:id>")
def fazerpergunta(id):
    anuncio = Anuncio.query.get(id)
    return render_template("fazerpergunta.html", anuncio = anuncio, usuarios= Usuario.query.all())

@app.route("/anunc/pergunta/criar/<int:id>", methods=['POST'])
def criarpergunta(id):
    anuncio = Anuncio.query.get(id)
    pergunta = Pergunta(request.form.get("pergunta"), "", request.form.get("user"), anuncio.id)
    db.session.add(pergunta)
    db.session.commit()
    return redirect(url_for("pergunta"))


@app.route("/anunc/pergunta/resposta/<int:id>", methods=['GET','POST'])
def editarperguntar(id):
    pergunta = Pergunta.query.get(id) 
    if request.method == "POST":
        pergunta.pergunta = pergunta.pergunta
        pergunta.resposta = request.form.get("resposta")
        pergunta.idusuario = pergunta.idusuario
        pergunta.idanuncio = pergunta.idanuncio
        db.session.add(pergunta)
        db.session.commit()
        return redirect(url_for("pergunta"))
    return render_template("responderpergunta.html", pergunta = pergunta)

@app.route("/anunc/compra/")
def compra():
    return redirect(url_for("index"))

@app.route("/anunc/comprar/<int:id>")
def comprar(id):
    anuncio = Anuncio.query.get(id)
    aux = anuncio.qtd
    return render_template("comprar.html",aux = aux, anuncio = anuncio, usuarios= Usuario.query.all())

@app.route("/anunc/compra/confirmarcompra/<int:id>", methods=['GET','POST'])
def confirmarcompra(id):
    anuncio = Anuncio.query.get(id)
    if int(request.form.get("qtd")) > anuncio.qtd:
        return render_template("errocompra.html")
    else:
        compra = Compra(anuncio.preco, request.form.get("qtd"), anuncio.preco * float(request.form.get("qtd")), anuncio.id, request.form.get("user"))
        anuncio.nome = anuncio.nome
        anuncio.desc = anuncio.desc
        anuncio.qtd = anuncio.qtd - int(request.form.get("qtd"))
        anuncio.preco = anuncio.preco
        anuncio.idusuario = anuncio.idusuario
        anuncio.idcategoria = anuncio.idcategoria
        db.session.add(compra)
        db.session.commit()
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/anunc/favoritos/")
def favoritos():
    return render_template("favoritos.html", favoritos = Favorito.query.all(), anuncio = Anuncio.query.all(), usuarios = Usuario.query.all())

@app.route("/anunc/favoritos/detalhes/<int:id>", methods=['GET', 'POST'])
def detalhesfavoritos(id):
    anuncio = Anuncio.query.get(id)
    return render_template("detalhesfavoritos.html", anuncio = anuncio, usuarios= Usuario.query.all())

@app.route("/anunc/favoritos/criar", methods=['POST'])
def criarfavoritos():
    favorito = Favorito(request.form.get("anunc"), request.form.get("user"))
    db.session.add(favorito)
    db.session.commit()
    return redirect(url_for("favoritos"))

@app.route("/rel/vendas")
def relVendas():
    return render_template("relVendas.html", compras = Compra.query.all(), anuncios = Anuncio.query.all(), usuarios = Usuario.query.all())

@app.route("/rel/compras")
def relCompras():
    return render_template("relCompras.html", compras = Compra.query.all(), anuncio = Anuncio.query.all(), usuarios = Usuario.query.all())

if __name__ == "sonegocio":
	db.create_all()


