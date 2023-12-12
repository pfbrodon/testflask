from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
app = Flask(__name__)


# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/proyecto'# MAC OS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemyb ,cvgb                                    


class Producto(db.Model):
    # Define tu modelo SQLAlchemy aquí
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    cantidad=db.Column(db.Integer)
    categoria=db.Column(db.String(50))
    codigo=db.Column(db.Integer)
    descripcion=db.Column(db.String(50))
    precioUnit=db.Column(db.Numeric(precision=10, scale=2))
    precioVPublico=db.Column(db.Numeric(precision=10, scale=2))
    
    def __init__(self,cantidad,categoria,codigo,descripcion,precioUnit,precioVPublico):   #crea el  constructor de la clase
        self.cantidad=cantidad  # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.categoria=categoria
        self.codigo=codigo
        self.descripcion=descripcion
        self.precioUnit=precioUnit
        self.precioVPublico=precioVPublico
        
@app.route('/')
def index():
    # Obtén los datos de la tabla
    data = Producto.query.all()
    return render_template('index.html', data=data)

###################################################################

@app.route('/editar/<int:id>')
def editar(id):
    # Obtén los datos del elemento con el ID proporcionado
    item = Producto.query.get(id)
    return render_template('editar.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)
