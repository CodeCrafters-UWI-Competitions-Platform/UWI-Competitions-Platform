from datetime import datetime
from App.database import db

class RankingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    total_rating = db.Column(db.Float, nullable=False)
    average_rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, rank, total_rating, average_rating, timestamp):
        self.rank = rank
        self.total_rating = total_rating
        self.average_rating = average_rating
        self.timestamp = timestamp

    def __repr__(self):
        return f'Student {self.student_id} : {self.rank}, {self.rating}, {self.timestamp}'
    
    def get_json(self):
        return {
            "id" : self.id,
            "student_id" : self.student_id,
            "rank" : self.rank,
            "total_rating" : self.rating,
            "average_rating" : self.average_rating,
            "timestamp" : self.timestamp
        }