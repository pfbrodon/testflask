from flask import Flask, render_template,request, url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
app = Flask(__name__)


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:12345678@localhost/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
app.config['SECRET_KEY'] = '12345678'
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemyb ,cvgb                                    


class Producto(db.Model):
    # Define tu modelo SQLAlchemy aquí
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    cantidad=db.Column(db.Integer)
    categoria_id=db.Column(db.String(50))
    codigo=db.Column(db.Integer)
    descripcion=db.Column(db.String(50))
    precioUnit=db.Column(db.Numeric(precision=10, scale=2))
    precioVPublico=db.Column(db.Numeric(precision=10, scale=2))
    
    def __init__(self,cantidad,categoria_id,codigo,descripcion,precioUnit,precioVPublico):   #crea el  constructor de la clase
        self.cantidad=cantidad  # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.categoria_id=categoria_id
        self.codigo=codigo
        self.descripcion=descripcion
        self.precioUnit=precioUnit
        self.precioVPublico=precioVPublico
        
###################################################################
        
@app.route('/')
def index():
    # Obtén los datos de la tabla
    data = Producto.query.all()
    return render_template('index.html', data=data)

###################################################################

@app.route('/editar/<int:id>', methods=['POST','GET'])
def editar(id):
    item = Producto.query.get(id)
    if request.method=='POST':
        item.cantidad=request.form.get('cantidad')
        item.categoria_id=request.form.get('categoria_id')
        item.codigo=request.form.get('codigo')
        item.descripcion=request.form.get('descripcion')
        item.precioUnit=request.form.get('precioUnit')
        item.precioVPublico=request.form.get('precioVPublico')
        db.session.commit() # confirma el alta
        return redirect(url_for('index'))
    # Obtén los datos del elemento con el ID proporcionado
    return render_template('editar.html', item=item)

###################################################################

@app.route('/nuevo', methods=['POST','GET']) # crea ruta o endpoint
def nuevo():
    if request.method=='POST':        #print(request.json)  # request.json contiene el json que envio el cliente
        cantidad=request.form.get('cantidad')
        categoria_id=request.form.get('categoria_id')
        codigo=request.form.get('codigo')
        descripcion=request.form.get('descripcion')
        precioUnit=request.form.get('precioUnit')
        precioVPublico=request.form.get('precioVPublico')
        productoNuevo=Producto(cantidad,categoria_id,codigo,descripcion,precioUnit,precioVPublico)
        db.session.add(productoNuevo)
        db.session.commit() # confirma el alta
        return redirect(url_for('index'))
    return render_template('nuevo.html')

###################################################################

@app.route('/eliminar/<int:id>',methods=['POST','GET'])
def eliminar(id):
    item=db.session.query(Producto).get(id)
    if request.method=='POST':
        db.session.delete(item)
        db.session.commit()
        flash('Elemento eliminado correctamente', 'success')
        return redirect(url_for('index'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
