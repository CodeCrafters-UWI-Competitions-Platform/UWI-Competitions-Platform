from datetime import datetime
from App.database import db

class RankingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, rank, rating, timestamp):
        self.rank = rank
        self.rating = rating
        self.timestamp = timestamp

    def __repr__(self):
        return f'Student {self.student_id} : {self.rank}, {self.rating}, {self.timestamp}'
    
    def get_json(self):
        return {
            "id" : self.id,
            "student_id" : self.student_id,
            "rank" : self.rank,
            "rating" : self.rating,
            "timestamp" : self.timestamp
        }