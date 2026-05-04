from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tutorial.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#definicion del modelo
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False,unique=True)
    
    def __repr__(self):
        return f"<users(name='{self.name}', email='{self.email}')"
    #funcion para listar la base de datos
    
def init_db():
    with app.app_context():
        db.create_all()
        print(" Tablas creadas exitosamente")
#operadores crud
def insert_users():
   with app.app_context():
# Creamos objetos Python
        user1 = User(name="Bruno Diaz", email="bruno@mail.com")
        user2 = User(name="Ricardo Tapia", email="ricky@mail.com")
        user3 = User(name="Maria Masco", email="mar@mail.com")

# Los añadimos de objetos de tipo user
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)

# consolida los cambios de la base de datos
        db.session.commit()
        print(" Usuarios insertados")
#consultas a la base de datos       
def query_users():
    with app.app_context():
        #consulta para los registros de la tabla
        print("listado de usuarios")
        users = User.query.all()
        for item in users:
            print(item)
        #consulta de un solo usuario
        print("obtener un solo registro ")
        user = User.query.filter_by(id=100).first()
        if user:
            print(user)
        else:
            print("usuario no encontrado")

def update_user():
    with app.app_context():
        print("\nActualización de un registro")
        
        user = User.query.filter_by(id=1).first()
        
        if user:
            user.name = "Pepe Trueno"
            user.email = "pepe@mail.com"
            
            # Consolida los cambios en la base de datos
            db.session.commit()
            
            print("Usuario actualizado: ", user)
        else:
            print("Usuario no encontrado")
             
if __name__=="__main__":
    init_db()
    insert_users()
    query_users()
    update_user()
