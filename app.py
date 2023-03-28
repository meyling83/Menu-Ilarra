from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import * 
import os

app=Flask(__name__)

basedir=os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'databaseMenu.db')
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Platos(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50),nullable=False)
    descripcion=db.Column(db.String(250),nullable=False)
    categoria=db.Column(db.String(250),nullable=False)
    precio=db.Column(db.Numeric,nullable=False)
    um=db.Column(db.String(50),nullable=True)
    activo=db.Column(db.Boolean,default=True)
    
    def __init__(self,nombre,descripcion,categoria,precio,um):
        self.nombre=nombre
        self.descripcion=descripcion
        self.categoria=categoria
        self.precio=precio
        self.um=um
        self.activo=True

    def add_plato(self, plato):
        db.session.add(plato)
        db.session.commit()
  
        
        
def Rellenar_PrimeraVez():
    p1=Platos("Rodaballo","a la parrila","Pescados",98," €/Kg")
    p2=Platos("Entrecot","de vacuno madurado a la parrilla","Carnes",28,"€")

    db.session.add_all([p1,p2])
    db.session.commit()

""" with app.app_context():
    db.create_all() """

@app.route("/")
def index():
    render_template("index.html")
    
@app.route("/rellenar")
def rellenar():
    Rellenar_PrimeraVez()

@app.route("/sql_todos")
def sql_todos():
    platos=Platos.query.filter_by(activo=True)
    pescados=[p for p in platos if p.categoria=="Pescados"]
    carnes=[c for c in platos if c.categoria=="Carnes"]
    guarniciones=[a for a in platos if a.categoria=="Guarniciones"]
    guarnicionaux=""
    for g in guarniciones:
        guarnicionaux=guarnicionaux + g.nombre+" " + g.descripcion + " " +str("%.2f" % g.precio) + " " +g.um + ", "

    return render_template("menu.html",pescados=pescados,carnes=carnes,guarniciones=guarnicionaux)

@app.route("/lista_platos")
def lista_platos():
     platos=Platos.query.filter_by(activo=True)
     return render_template("lista_platos.html",platos=platos)

@app.route("/insertar_plato",methods=["GET","POST"])
def insertar_plato():
    if request.method=="POST":
        nombre=request.form.get("txtNombre")
        descripcion=request.form.get("txtDescripcion")
        categoria=request.form.get("txtCategoria")
        precio=request.form.get("txtPrecio")
        um=request.form.get("txtUM")

        plato=Platos(nombre,descripcion,categoria,precio,um)
        plato.add_plato(plato) 
       
        return redirect(url_for("sql_todos"))
    else:
        return render_template("insertar_plato.html")
    
@app.route("/eliminar/<int:id>",methods=["GET","POST"])
def eliminar(id):
    if request.method=="POST":
        plato=Platos.query.get(id)
        db.session.delete(plato)
        db.session.commit()
        return redirect(url_for("sql_todos"))
    else:
         plato=Platos.query.get(id)
         return render_template("eliminar.html",plato=plato)
    
@app.route("/actualizar/<int:id>",methods=["GET","POST"])
def actualizar(id):
     if request.method=="POST":
        plato=Platos.query.get(id)
        plato.nombre=request.form.get("txtNombre")
        plato.descripcion=request.form.get("txtDescripcion")
        plato.categoria=request.form.get("txtCategoria")
        plato.precio=request.form.get("txtPrecio")
        plato.um=request.form.get("txtUM")

        plato.add_plato(plato) 
       
        return redirect(url_for("sql_todos"))
     else:
         plato=Platos.query.get(id)
         return render_template("actualizar.html",plato=plato)
            
            # break
        #if encontrado==False:
           # return redirect(url_for("noencontrado")) 


if __name__=="__main__":
    app.run(debug=True)
    