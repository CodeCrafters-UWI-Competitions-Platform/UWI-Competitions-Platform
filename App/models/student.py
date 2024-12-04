from App.database import db
from App.models import User

class Student(User):
    __tablename__ = 'student'

    rating_score = db.Column(db.Float, nullable=False, default=0)
    comp_count = db.Column(db.Integer, nullable=False, default=0)
    curr_rank = db.Column(db.Integer, nullable=False, default=0)
    teams = db.relationship('Team', secondary='student_team', overlaps='students', lazy=True)
    notifications = db.relationship('Notification', backref='student', lazy=True)
    ranking_history = db.relationship('RankingHistory', backref='student', lazy=True)

    def __init__(self, username, password):
        super().__init__(username, password)
        self.rating_score = 0
        self.comp_count = 0
        self.curr_rank = 0
        self.teams = []
        self.notifications = []

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "rating_score": self.rating_score,
            "comp_count" : self.comp_count,
            "curr_rank" : self.curr_rank,
            "ranking_history" : [entry.get_json() for entry in self.ranking_history]
        }

    def to_Dict(self):
        return {
            "ID": self.id,
            "Username": self.username,
            "Rating Score": self.rating_score,
            "Number of Competitions" : self.comp_count,
            "Rank" : self.curr_rank,
            "Ranking History" : [entry.get_json() for entry in self.ranking_history]

        }

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'