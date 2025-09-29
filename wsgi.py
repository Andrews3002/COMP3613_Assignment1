import click
from App.database import get_migrate
from App.main import create_app
from App.controllers import initialize

app = create_app()
migrate = get_migrate(app)

@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')
    
@app.cli.command("add_student", help="Add a new student")
@click.argument("name", nargs=-1)
def add_student(name):
    name = " ".join(name)
    from App.models import User
    user = User.query.first()
    if user:
        user.addStudent(name)
        print(f'Student {name} added!')
    else:
        print("No users found.")

@app.cli.command("list_students", help="Lists all students in the database")
def list_students():
    from App.models import User
    user = User.query.first()
    if user:
        user.listStudents()
    else:
        print("No users found.")

@app.cli.command("switch_to_student", help="Switch to a student role")
@click.argument("student_id", type=int)
def switch_to_student(student_id):
    from App.models import User
    user = User.query.first()
    if user:
        user.switchToStudent(student_id)
        print(f'Switched to student with ID {student_id}')
    else:
        print("No users found.")     

@app.cli.command("switch_to_staff", help="Switch to staff role")
def switch_to_staff():
    from App.models import User
    user = User.query.first()
    if user:
        user.switchToStaff()
        print('Switched to staff role')
    else:
        print("No users found.")     

        
