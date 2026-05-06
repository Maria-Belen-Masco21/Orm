# relaciones N-N con ORM
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Tabla intermedia (muchos a muchos)
student_course = db.Table(
    "student_course",  # nombre corregido (antes "studen_course")
    db.Column("student_id", db.Integer, db.ForeignKey("students.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id"), primary_key=True)
)

class Student(db.Model):
    __tablename__ = "students"  # doble guion bajo
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    courses = db.relationship("Course", secondary=student_course, back_populates="students")

    def __repr__(self):
        return f"<Student: nombre={self.name}>"

class Course(db.Model):  # db.Model con mayúscula
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    students = db.relationship("Student", secondary=student_course, back_populates="courses")

    def __repr__(self):
        return f"<Course: titulo={self.title}>"

# Inicializar la base de datos
def init_db():
    with app.app_context():
        db.create_all()
        print("Base de datos creada satisfactoriamente")

# Insertar registros de ejemplo
def insert_data():
    with app.app_context():
        # Crear estudiantes
        s1 = Student(name="Bruno Díaz")
        s2 = Student(name="Zacarias Flores")
        s3 = Student(name="Elsa Capunta")  # nombre consistente

        # Crear cursos
        c1 = Course(title="Python")
        c2 = Course(title="Javascript")
        c3 = Course(title="React")

        # Asignar cursos a estudiantes
        s1.courses.extend([c1, c2])  # Bruno -> Python y Javascript
        s2.courses.append(c2)        # Zacarias -> Javascript
        s3.courses.extend([c1, c3])  # Elsa -> Python y React

        # Agregar todas las instancias a la sesión y guardar
        db.session.add_all([s1, s2, s3, c1, c2, c3])
        db.session.commit()
        print("Estudiantes y cursos insertados correctamente")

# Consultar y mostrar datos
def query_data():
    with app.app_context():
        print("\n=== Listado de estudiantes y sus cursos ===")
        students = Student.query.all()
        for s in students:
            print(f"\n{s.name} está inscrito en:")
            for c in s.courses:
                print(f"  - {c.title}")

        print("\n=== Listado de cursos y sus estudiantes ===")
        courses = Course.query.all()
        for c in courses:
            print(f"\n{c.title} tiene inscritos a:")
            for s in c.students:
                print(f"  - {s.name}")

# Actualizar relación: agregar un curso existente a un estudiante existente
def update_relations():
    with app.app_context():
        print("\n--- Agregando un curso a un estudiante ---")
        # Ejemplo: estudiante con id=1 (Bruno) se inscribe en curso id=3 (React)
        estu = Student.query.get(1)
        curso = Course.query.get(3)
        if estu and curso:
            if curso not in estu.courses:
                estu.courses.append(curso)
                db.session.commit()
                print(f"Inscripción actualizada: {estu.name} ahora está en {curso.title}")
            else:
                print(f"{estu.name} ya estaba inscrito en {curso.title}")
        else:
            print("Estudiante o curso no encontrado")

# Eliminar relación: quitar un curso a un estudiante
def delete_relation():
    with app.app_context():
        print("\n--- Eliminando una inscripción ---")
        # Ejemplo: estudiante id=1 (Bruno) se desinscribe de curso id=3 (React)
        estu = Student.query.get(1)
        curso = Course.query.get(3)
        if estu and curso:
            if curso in estu.courses:
                estu.courses.remove(curso)
                db.session.commit()
                print(f"Se eliminó la inscripción: {estu.name} ya no está en {curso.title}")
            else:
                print(f"{estu.name} no estaba inscrito en {curso.title}")
        else:
            print("Estudiante o curso no encontrado")

if __name__ == "__main__":
    init_db()
    insert_data()
    query_data()
    update_relations()
    query_data()      # ver el cambio
    delete_relation()
    query_data()      # ver el cambio final