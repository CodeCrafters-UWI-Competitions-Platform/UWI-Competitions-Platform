from App.database import db
from .competition import *

class CompetitionTeam(db.Model):
    __tablename__ = 'competition_team'
    
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    team_id =  db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    points_earned = db.Column(db.Float, default=0)
    rating_score = db.Column(db.Float, default=0)

    def __init__(self, comp_id, team_id):
      self.comp_id = comp_id
      self.team_id = team_id
      self.points_earned = 0
      self.rating_score = 0

    def update_points(self, points_earned):
      self.points_earned = points_earned

      competition = Competition.query.get(self.comp_id)
      if competition:
         competition.notify()

    def update_rating(self, rating_score):
      self.rating_score = rating_score

    def get_json(self):
      return {
          "id" : self.id,
          "team_id" : self.team_id,
          "competition_id" : self.comp_id,
          "points_earned" : self.points_earned,
          "rating_score" : self.rating_score
      }

    def toDict(self):
      return {
        "ID" : self.id,
        "Student ID" : self.student_id,
        "Competition ID" : self.comp_id,
        "Points Earned" : self.points_earned,
        "Rating Score" : self.rating_score
      } 