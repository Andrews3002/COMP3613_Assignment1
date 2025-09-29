from App.models.request import Request
from App.models.hours import Hours

from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isStudent = db.Column(db.Boolean, default=True)
    isStaff = db.Column(db.Boolean, default=False)
    selectedStudentID = db.Column(db.Integer, nullable=True)

    def __init__(self):
        self.isStudent = False
        self.isStaff = False
        self.selectedStudentID = None
        
    def getID(self):
        return self.id
        
    def getIsStudent(self):
        return self.isStudent
    
    def getIsStaff(self):
        return self.isStaff
    
    def getSelectedStudentID(self):
        return self.selectedStudentID
    
    def setIsStudent(self, isStudent):
        self.isStudent = isStudent
        
    def setIsStaff(self, isStaff):
        self.isStaff = isStaff
    
    def setSelectedStudentID(self, selectedStudentID):
        self.selectedStudentID = selectedStudentID
   
    def listStudents(self):
        list = Student.query.all()
        for i in list:
            print("ID: ", i.getID(), "Name: ", i.getName())
    
    def viewLeaderboard(self):
        list = Hours.query.order_by(Hours.hours.desc()).all()
        count = 1
        for i in list:
            student = Student.query.filter_by(studentID = i.getStudentID()).first()
            print("| Rank: ", count, "| Name: ", student.getName(), "| Hours: ", i.getHours(), "|")
            count += 1
            
    def addStudent(self, name):
        student = Student(name)
        db.session.add(student)
        db.session.commit()
        
        HoursEntry = Hours(student.getID(), 0)
        db.session.add(HoursEntry)
        db.session.commit()
        
    def switchToStudent(self, studentID):
        self.setSelectedStudentID(studentID)
        self.setIsStudent(True)
        self.setIsStaff(False)
        db.session.commit()
        
    def switchToStaff(self):
        self.setSelectedStudentID(None)
        self.setIsStudent(False)
        self.setIsStaff(True)
        db.session.commit()
        
    def get_json(self):
        return {
            "isStudent": self.getIsStudent(),
            "isStaff": self.getIsStaff(),
            "selectedStudentID": self.getSelectedStudentID()
        }
        
class Student(User):
    studentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    requestPending = db.Column(db.Boolean, default=False)
    
    def __init__(self, name):
        self.name = name
    
    def getID(self):
        return self.studentID
    
    def getName(self):
        return self.name
    
    def getRequestPending(self):
        return self.requestPending
    
    def setName(self, name):
        self.name = name
        
    def setRequestPending(self, requestMade):
        self.requestPending = requestMade
        
    def makeRequest(self, hours):
        if not self.getIsStudent():
            print ("This function is for Student access only")
            return
        
        if self.getRequestPending():
            print("This student already has a pending request, Each student can only make one request at a time")
            return
        
        request = Request(self.getID(), hours)
        self.setRequestPending(True)
        
        db.session.add(request)
        db.session.commit()
        
    def withdrawRequest(self):
        if not self.getIsStudent():
            print ("This function is for Student access only")
            return
        
        if not self.getRequestPending():
            print("This student does not have a pending request to withdraw")
            return
        
        request = Request.query.filter_by(studentID = self.getID()).first()
        if request:
            db.session.delete(request)
            self.setRequestPending(False)
            db.session.commit()
            
    def viewAccolades(self):
        if not self.getIsStudent():
            print ("This function is for Student access only")
            return
        
        hours = Hours.query.filter_by(studentID = self.getID()).first()
        
        if hours:
            if hours.getTenHourMS():
                print("10 Hour Milestone Achieved")
            else:
                print("No Milestones Achieved")
                
                
            if hours.getTwentyFiveHourMS():
                print("25 Hour Milestone Achieved")
            if hours.getFiftyHourMS():
                print("50 Hour Milestone Achieved")
        
    def get_json(self):
        return {
            "id": self.getID(),
            "name": self.getName(),
            "requestPending": self.getRequestPending()
        }
        
class Staff(User):
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    def __init__(self):
        pass
    
    def viewRequests(self):
        if self.getIsStaff() == False:
            print("This function is for Staff access only")
            return
        
        list = Request.query.filter_by().all()
        for i in list:
            print("ID: ", i.getID(), "Student ID: ", i.getStudentID(), "Hours: ", i.getHours())
            
    def rejectRequest(self, requestID):
        if self.getIsStaff() == False:
            print("This function is for Staff access only")
            return
        
        request = Request.query.filter_by(id = requestID).first()
        
        student = Student.query.filter_by(studentID = request.getStudentID()).first()
        if student:
            student.setRequestPending(False)
            db.session.delete(request)
            db.session.commit()
            
    def confirmRequest(self, requestID):
        if self.getIsStaff() == False:
            print("This function is for Staff access only")
            return
        
        request = Request.query.filter_by(id = requestID).first()
        
        student = Student.query.filter_by(studentID = request.getStudentID()).first()
        if student:
            student.setRequestPending(False)
            self.logHours(request.getHours(), student.getID())
            db.session.delete(request)
            db.session.commit()
       
            
    def logHours(self, hours, studentID): 
        hoursEntry = Hours.query.filter_by(studentID = studentID).first()
        if hoursEntry:
            hoursEntry.setHours(hoursEntry.getHours() + hours)
            hoursEntry.setMilestones()
            db.session.commit()
        else:
            hoursEntry = Hours(studentID, hours)
            hoursEntry.setMilestones()
            db.session.add(hoursEntry)
            db.session.commit()
    