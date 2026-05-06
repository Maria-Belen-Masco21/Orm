# relaciones 1-N con ORM

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# configuracion de SQLAlchemy
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# declaracion para usar el SQLAlchemy
db = SQLAlchemy(app) 

# definicion del modelo
class User(db.Model):
    __tablename__ = "users" 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=False) 
    email = db.Column(db.String(100), nullable=False) 
    
    posts = db.relationship('Post', back_populates='user')
    
    def __repr__(self): 
        return f"<usuario(name={self.name}, email={self.email})>" 


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', back_populates='posts')
    
    def __repr__(self): 
        return f"POST: title:{self.title} user: {self.user.name} - {self.user.email}"


# funcion para inicializar la base de datos 
def init_db():
    with app.app_context(): 
        db.create_all() 
        print("Base de datos creada satisfactoriamente")


# operaciones crud
def insert_data():
    with app.app_context():
        user1 = User(name="Bruno Diaz", email="bruno@mail.com") 
        user2 = User(name="Ricardo Tapia", email="ricky@mail.com")
        user3 = User(name="Zacarias Flores", email="zacarias@mail.com") 
        
        post1 = Post(title="Primer post de Bruno",
                     content="Primera publicación de Bruno",
                     user=user1)
        post2 = Post(title="Segundo post de Bruno",
                     content="Segunda publicación de Bruno",
                     user=user1)
        post3 = Post(title="Primer post de Ricardo",
                     content="Entrada uno de Ricardo",
                     user=user2)
        post4 = Post(title="Primera entrada de Zacarias",
                     content="Entrada uno de Zaca",
                     user=user3)

        db.session.add_all([user1, user2, user3, post1, post2, post3, post4])
        db.session.commit()
        print("Usuarios y entradas insertadas")


# consultas a la base de datos 
def query_data(): 
    with app.app_context(): 
        print("\nListado de usuarios y sus publicaciones")
        
        users = User.query.all() 
        for user in users:
            print(user)
            for post in user.posts:
                print(post)


def update_data():
    with app.app_context():
        print("\nActualizando una publicación")
        
        post = Post.query.filter_by(id=3).first()
        if post:
            post.content = "Entrada actualizada de Ricardo"
            db.session.commit()
            print("Entrada actualizada correctamente")
        else:
            print("Post no encontrado")


# MAIN 
if __name__ == "__main__":
    init_db()        
    insert_data()    
    query_data()    
    update_data()    
    query_data()   