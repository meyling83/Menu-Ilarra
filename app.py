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

        
#funcion para llenar la BD la primera vez      
def Rellenar_PrimeraVez():
    p1=Platos("Rodaballo","a la parrila","Pescados",98," €/Kg")
    p2=Platos("Entrecot","de vacuno madurado a la parrilla","Carnes",28,"€")

    db.session.add_all([p1,p2])
    db.session.commit()
#creacion de la BD. Descomentar 
""" with app.app_context():
    db.create_all() """

#ruta para rellenar la BD por primera vez
@app.route("/rellenar")
def rellenar():
    Rellenar_PrimeraVez()

#ruta principal. Se muestra el menú del día
@app.route("/")
def sql_todos():
    #se filtran solo los paltos activos, pues los falsos som los eliminados
    platos=Platos.query.filter_by(activo=True)
    #obtengo las listas de pescados, carnes, guarniciones y sugerencias del chef para enviarlas al html
    pescados=[p for p in platos if p.categoria=="Pescados"]
    carnes=[c for c in platos if c.categoria=="Carnes"]
    guarniciones=[a for a in platos if a.categoria=="Guarniciones"]
    sugerencias=[s for s in platos if s.categoria=="Sugerencia"]
    #obtener un cadena de texto con todas las guarniciones
    guarnicionaux=""
    for g in guarniciones:
        guarnicionaux=guarnicionaux + g.nombre+" " + g.descripcion + " " +str("%.2f" % g.precio) + " " +g.um + ", "
    
    return render_template("menu.html",pescados=pescados,carnes=carnes,guarniciones=guarnicionaux,sugerencias=sugerencias)

#ruta para el formulario que muestra un listado de todos los platos activos para añadir, actualizar o eliminar platos 
@app.route("/lista_platos")
def lista_platos():
    platos=Platos.query.filter_by(activo=True)
    return render_template("lista_platos.html",platos=platos)

#ruta del formulario en el que se añaden platos
@app.route("/insertar_plato",methods=["GET","POST"])
def insertar_plato():
    if request.method=="POST":
        nombre=request.form.get("txtNombre")
        descripcion=request.form.get("txtDescripcion")
        categoria=request.form.get("slcCategoria")
        precio=request.form.get("txtPrecio")
        um=request.form.get("txtUM")

        plato=Platos(nombre,descripcion,categoria,precio,um)
        plato.add_plato(plato) 
    
        return redirect(url_for("lista_platos"))
    else:
        return render_template("insertar_plato.html")

#ruta del formulario de eliminar platos   
@app.route("/eliminar/<int:id>",methods=["GET","POST"])
def eliminar(id):
    plato=Platos.query.get(id)
    if plato is None:
        return redirect(url_for("no_encontrado"))
    else:
        if request.method=="POST":
            #los platos no se eliminan fisicamente, se marcan como falso
            plato.activo=False
            plato.add_plato(plato)     
            return redirect(url_for("lista_platos"))
        else:
            return render_template("eliminar.html",plato=plato)

#ruta del formulario para actualizar los platos   
@app.route("/actualizar/<int:id>",methods=["GET","POST"])
def actualizar(id):
    plato=Platos.query.get(id)
    if plato is None:
        return redirect(url_for("no_encontrado"))
    else:
        if request.method=="POST":
            plato.nombre=request.form.get("txtNombre")
            plato.descripcion=request.form.get("txtDescripcion")
            plato.categoria=request.form.get("slcCategoria")
            plato.precio=request.form.get("txtPrecio")
            plato.um=request.form.get("txtUM")

            plato.add_plato(plato) 
    
            return redirect(url_for("lista_platos"))
        else:
            return render_template("actualizar.html",plato=plato)
            

@app.route("/no_encongtrado")
def no_encontrado():
    return render_template("noencontrado.html")

if __name__=="__main__":
    app.run(debug=True)   
