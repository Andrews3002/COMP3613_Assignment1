from App.database import db

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    
    def __init__(self, studentID, hours):
        self.setStudentID(studentID)
        self.setHours(hours)
    
    def getID(self):
        return self.id

    def getStudentID(self):
        return self.studentID
    
    def getHours(self):   
        return self.hours
    
    def setStudentID(self, studentID):
        self.studentID = studentID
        
    def setHours(self, hours):
        self.hours = hours
        
    def get_json(self):
        return {
            'id': self.getID(),
            'studentID': self.getStudentID(),
            'hours': self.getHours()
        }