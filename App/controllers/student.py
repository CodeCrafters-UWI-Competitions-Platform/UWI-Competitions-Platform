from datetime import datetime
from App.database import db
from App.models import Student, Competition, Notification, CompetitionTeam, RankingHistory

def create_student(username, password):
    student = get_student_by_username(username)
    if student:
        print(f'{username} already exists!')
        return None

    newStudent = Student(username=username, password=password)
    try:
        db.session.add(newStudent)
        db.session.commit()
        print(f'New Student: {username} created!')
        return newStudent
    except Exception as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json

def update_student(id, username):
    student = get_student(id)
    if student:
        student.username = username
        try:
            db.session.add(student)
            db.session.commit()
            print("Username was updated!")
            return student
        except Exception as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

def display_student_info(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        competitions = []
        
        for team in student.teams:
            team_comps = CompetitionTeam.query.filter_by(team_id=team.id).all()
            for comp_team in team_comps:
                comp = Competition.query.filter_by(id=comp_team.comp_id).first()
                competitions.append(comp.name)

        profile_info = {
            "profile" : student.get_json(),
            "competitions" : competitions
        }

        return profile_info

def display_notifications(username):
    student = get_student_by_username(username)

    if not student:
        print(f'{username} does not exist!')
        return None
    else:
        return {"notifications":[notification.to_Dict() for notification in student.notifications]}

# def update_rankings():
#     students = get_all_students()
    
#     students.sort(key=lambda x: (x.rating_score, x.comp_count), reverse=True)

#     leaderboard = []
#     count = 1
    
#     curr_high = students[0].rating_score
#     curr_rank = 1
        
#     for student in students:
#         if curr_high != student.rating_score:
#             curr_rank = count
#             curr_high = student.rating_score

#         if student.comp_count != 0:
#             leaderboard.append({"placement": curr_rank, "student": student.username, "rating score":student.rating_score})
#             count += 1
        
#             student.curr_rank = curr_rank
#             if student.prev_rank == 0:
#                 message = f'RANK : {student.curr_rank}. Congratulations on your first rank!'
#             elif student.curr_rank == student.prev_rank:
#                 message = f'RANK : {student.curr_rank}. Well done! You retained your rank.'
#             elif student.curr_rank < student.prev_rank:
#                 message = f'RANK : {student.curr_rank}. Congratulations! Your rank has went up.'
#             else:
#                 message = f'RANK : {student.curr_rank}. Oh no! Your rank has went down.'
#             student.prev_rank = student.curr_rank
#             notification = Notification(student.id, message)
#             student.notifications.append(notification)

#             try:
#                 db.session.add(student)
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()

#     return leaderboard

'''Returns Leaderboard data in the order of Highest to Lowest Rank'''
def get_student_leaderboard_data():
    students = get_all_students()

    students.sort(key=lambda x: (x.curr_rank), reverse=False)
    leaderboard = []

    for student in students:
        if student.comp_count != 0:
            leaderboard.append({"placement": student.curr_rank, "student": student.username, "Total Score": student.total_rating, "Average Score": student.average_rating})
    return leaderboard

'''Calculates the Total and Average ratings for each student'''
def calculate_ratings():
    save_ranking_history()
    students = get_all_students()
    for student in students:
        total_rating = 0
        count = 0
        for team in student.teams:
            competition_teams = CompetitionTeam.query.filter_by(team_id=team.id).all()
            for competition_team in competition_teams:
                count += 1
                total_rating += competition_team.rating_score

        if total_rating > 0 and count > 0:
            average_rating = total_rating / count
            update_ratings_db(student.id, total_rating, average_rating)
        
'''Updates the database for total and average for a single student'''
def update_ratings_db(id, total_rating, average_rating):
    student = get_student(id)
    student.total_rating = total_rating
    student.average_rating = average_rating
    student.comp_count += 1

    try:
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

'''Updates the rank of all students based on total rating for all competitions'''
def update_all_rankings_total():
    if calculate_ratings():
        print("Success Updating Rankings")

    students = get_all_students()
    students.sort(key=lambda x: (x.total_rating, x.average_rating, x.comp_count), reverse=True)
    rank = 1
    prev_student = None

    for student in students:
        student.curr_rank = rank
        rank += 1
        db.session.add(student)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    send_notification()
    
'''Updates the rank of all students based on the average rating per competition'''
def update_all_rankings_average():
    if calculate_ratings():
        print("Success Updating Rankings...")

    students = get_all_students()
    students.sort(key=lambda x: (x.average_rating, x.total_rating, x.comp_count), reverse=True)
    count = 1

    for student in students:
        student.curr_rank = count
        count += 1
        db.session.add(student)
        
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()

'''Updates the rank of all students based on the number of competitions they are involved in'''
def update_all_rankings_competition_count():
    if calculate_ratings():
        print("Success Updating Rankings...")

    students = get_all_students()
    students.sort(key=lambda x: (x.comp_count, x.total_rating, x.average_rating), reverse=True)
    count = 1

    for student in students:
        student.curr_rank = count
        count += 1
        db.session.add(student)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()

'''Saves the ranking history for each student before recalculating rank'''
def save_ranking_history():
    students = get_all_students()

    for student in students:
        if student.curr_rank != 0:
            rank = db.session.query(RankingHistory).order_by(RankingHistory.timestamp.desc()).first()
            record = RankingHistory(student.curr_rank, student.total_rating, student.average_rating, datetime.now())
            student.ranking_history.append(record)
            db.session.add(student)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()

'''Checks if rank changed and issues a notification'''
def send_notification():
    students = get_all_students()

    for student in students:
        if(student.curr_rank != 0):
            rank = RankingHistory.query.filter_by(student_id = student.id).order_by(RankingHistory.timestamp.desc()).first()
            if rank != None:
                print(rank.get_json())

            if rank == None:
                notification = Notification(student.id, f"RANK : {student.curr_rank}. Congratulations on your first rank!")
                db.session.add(notification)
            elif rank.rank < student.curr_rank:
                notification = Notification(student.id, f"RANK : {student.curr_rank}. Oh no! Your rank went down!")
                db.session.add(notification)
            elif rank.rank > student.curr_rank:
                notification = Notification(student.id, f"RANK : {student.curr_rank}. Congratulations! your rank went up!")
                db.session.add(notification)
            elif rank.rank == student.curr_rank:
                notification = Notification(student.id, f"RANK : {student.curr_rank}. Well done! You retained your rank.")
                db.session.add(notification)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()