import warnings
warnings.filterwarnings("ignore", category=UserWarning)

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
    if name == "":
        print("Please provide a name for the student.")
        return
    
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

@app.cli.command("view_leaderboard", help="View the leaderboard of students by hours")
def view_leaderboard():
    from App.models import User
    user = User.query.first()
    if user:
        user.viewLeaderboard()
    else:
        print("No users found.") 
        
@app.cli.command("make_request", help="Make a request to staff to log your hours")
@click.argument("hours", type=float)
def make_request(hours):
    from App.models import User
    user = User.query.first()
    if user:
        if user.getIsStaff():
            print("This function is for Student access only")
            return
        from App.models import Student
        student = Student.query.filter_by(studentID = user.getSelectedStudentID()).first()
        if student:
            if student.getRequestPending():
                print("You already have a pending request.")
                return
            else:
                student.makeRequest(hours)
                print("Request made successfully.")
    else:
        print("No users found.")
        
@app.cli.command("withdraw_request", help="Withdraw a pending request to staff to log your hours ")
def withdraw_request():
    from App.models import User
    user = User.query.first()
    if user:
        from App.models import Student
        student = Student.query.filter_by(studentID = user.getSelectedStudentID()).first()
        if student:
            if not student.getRequestPending():
                print("This student does not have a pending request to withdraw")
                return
            else:
                student.withdrawRequest()
                print("Request withdrawn successfully.")
    else:
        print("No users found.")


@app.cli.command("view_accolades", help="View your accolades")
def view_accolades():
    from App.models import User
    user = User.query.first()
    if user:
        if user.getIsStaff():
            print("This function is for Student access only")
            return
        from App.models import Student
        student = Student.query.filter_by(studentID = user.getSelectedStudentID()).first()
        if student:
            student.viewAccolades()
    else:
        print("No users found.")
        
@app.cli.command("view_requests", help="View all pending requests from students")
def view_requests():
    from App.models import User
    user = User.query.first()
    if user:
        if not user.getIsStaff():
            print("This function is for Staff access only")
            return
        
        isStudent = user.getIsStudent()
        isStaff = user.getIsStaff()
        selectedStudentID = user.getSelectedStudentID()
            
        from App.models import Staff
        staff = Staff.query.filter_by().first()
        if staff:
            staff.setIsStudent(isStudent)
            staff.setIsStaff(isStaff)
            staff.setSelectedStudentID(selectedStudentID)
            staff.viewRequests()
        else:
            newstaff = Staff()
            newstaff.setIsStudent(isStudent)
            newstaff.setIsStaff(isStaff)
            newstaff.setSelectedStudentID(selectedStudentID)
            from App.database import db
            db.session.add(newstaff)
            db.session.commit()
            newstaff.viewRequests()
    else:
        print("No users found.")
        
@app.cli.command("reject_request", help="Reject a student's request")
@click.argument("request_id", type=int)
def reject_request(request_id):
    from App.models import User
    user = User.query.first()
    if user:
        if not user.getIsStaff():
            print("This function is for Staff access only")
            return
        
        from App.models import Staff, Request
        staff = Staff.query.filter_by().first()
        request = Request.query.filter_by(id = request_id).first()
        if staff and request:
            staff.rejectRequest(request_id)
            print(f"Request {request_id} rejected.")
        else:
            print("No request with ID:", request_id, "was found.")
    else:
        print("No users found.")