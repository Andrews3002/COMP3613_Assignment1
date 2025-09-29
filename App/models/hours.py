from App.database import db

class Hours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    hours = db.Column(db.Float, default=0.0)
    tenHourMilestone = db.Column(db.Boolean, default=False)
    twentyFiveHourMilestone = db.Column(db.Boolean, default=False)
    fiftyHourMilestone = db.Column(db.Boolean, default=False)
    
    def __init__(self, studentID, hours):
        self.setStudentID(studentID)
        self.setHours(hours)
    
    def getID(self):
        return self.id

    def getStudentID(self):
        return self.studentID
    
    def getHours(self):   
        return self.hours
    
    def getTenHourMS(self):
        return self.tenHourMilestone
    
    def getTwentyFiveHourMS(self):
        return self.twentyFiveHourMilestone
    
    def getFiftyHourMS(self):
        return self.fiftyHourMilestone
    
    def setStudentID(self, studentID):
        self.studentID = studentID
        
    def setHours(self, hours):
        self.hours = hours
        
    def setMilestones(self):
        if self.getHours() >= 10:
            self.tenHourMilestone = True
        if self.getHours() >= 25:
            self.twentyFiveHourMilestone = True
        if self.getHours() >= 50:
            self.fiftyHourMilestone = True
            
        db.session.commit()
    
    def get_json(self):
        return {
            'id': self.getID(),
            'studentID': self.getStudentID(),
            'hours': self.getHours(),
            'tenHourMilestone': self.getTenHourMS(),
            'twentyFiveHourMilestone': self.getTwentyFiveHourMS(),
            'fiftyHourMilestone': self.getFiftyHourMS()
        }