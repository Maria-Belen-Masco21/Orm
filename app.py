from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tutorial.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app) 

# definicion del modelo 
class User(db.Model): 
    __tablename__ = "users" 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(100), nullable=False, unique=True) 

    def __repr__(self): 
        return f"<User(name='{self.name}', email='{self.email}')>"

# funcion para crear la base de datos 
def init_db():
    with app.app_context(): 
        db.create_all() 
        print("Tablas creadas exitosamente") 

# INSERT (CREATE)
def insert_users(): 
    with app.app_context():
        user1 = User(name="Bruno Diaz", email="bruno@mail.com") 
        user2 = User(name="Ricardo Tapia", email="ricky@mail.com") 
        user3 = User(name="Maria Masco", email="mar@mail.com") 

        db.session.add(user1) 
        db.session.add(user2) 
        db.session.add(user3) 

        db.session.commit() 
        print("Usuarios insertados") 
        
# READ (CONSULTAS)
def query_users(): 
    with app.app_context(): 
        print("\nListado de usuarios") 
        
        users = User.query.all() 
        for item in users: 
            print(item) 

        print("\nListado de registros filtrados")
        filtrados = User.query.filter(User.id >= 2).all()
        for item in filtrados:
            print(item)
    
        print("\nObtener un solo registro") 
        user = User.query.filter_by(id=100).first() 
        if user: 
            print(user) 
        else: 
            print("Usuario no encontrado")

# UPDATE
def update_user(): 
    with app.app_context(): 
        print("\nActualización de un registro") 
        
        user = User.query.filter_by(id=1).first() 
        
        if user: 
            user.name = "Pepe Trueno" 
            user.email = "pepe@mail.com" 
            
            db.session.commit() 
            print("Usuario actualizado:", user) 
        else: 
            print("Usuario no encontrado") 

# DELETE (opcional agregado para CRUD completo)
def delete_user():
    with app.app_context():
        print("\nEliminando usuario")
        
        user = User.query.filter_by(id=2).first()
        
        if user:
            db.session.delete(user)
            db.session.commit()
            print("Usuario eliminado")
        else:
            print("Usuario no encontrado")


if __name__ == "__main__": 
    init_db() 
    insert_users() 
    query_users() 
    update_user() 
    delete_user()
    query_users()