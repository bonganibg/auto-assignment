import sqlite3
from models import *
from typing import List

DATABASE_PATH = 'data/review.db'

def get_reviewer_for_course(course_id: int) -> List[Reviewer]:
    conn = _get_connection()
    cur = conn.cursor()

    reviewers = cur.execute("""
                    SELECT R.*, (SELECT COUNT(*)
                                 FROM Review
                                 WHERE CompletedAt IS NULL
                                 AND ReviewerID = R.id
                            ) as backlog
                    FROM Reviewer R
                    LEFT JOIN Course_Reviewer CR ON CR.ReviewerID = R.id
                    WHERE CR.CourseID = ?
                """, (course_id,)).fetchall()
    
    conn.commit()
    conn.close()

    return [eval(f"Reviewer{reviewer}") for reviewer in reviewers]

def get_reviews_in_range(reviewer_id: int, start_date: date, end_date: date, days_of_week: List[str]):
    conn = _get_connection()
    cur = conn.cursor()

    days = tuple([f'{day}' for day in days_of_week])    

    reviews = cur.execute(f"""
    SELECT * 
    FROM Review
    WHERE CompletedAt BETWEEN ? and ?
    AND strftime(\"%w\", CompletedAt) IN {days}
    AND ReviewerID = ?    
    """, (start_date, end_date, reviewer_id)).fetchall()

    return _filter_time_before_submission_after_deadline(reviews, days_of_week, datetime.time(9, 0))
                
def _filter_time_before_submission_after_deadline(reviews, days: List[int], review_time: time):
    output = []
    start_day = (days[0] + 1) % 7
    end_day = (days[-1] + 1) % 7

    for review in reviews:
        review: Review = eval(f"Review{review}")

        if ((review.completed_at.date().weekday() == start_day and review.completed_at.time() < review_time)  or 
            (review.completed_at.date().weekday() == end_day and review.completed_at.time() > review_time)):
            continue

        output.append(review)
    
    return output

def create_submission(course_id: int, submission_datetime: datetime = datetime.datetime.today()):
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO Submission (CourseID, SubmissionDate) VALUES(?, ?)
    """, (course_id, submission_datetime))

    conn.commit()
    conn.close()

def get_unassgined_reviews():
    conn = _get_connection()
    cur = conn.cursor()

    submissions = cur.execute("""
    SELECT S.* 
    FROM Submission S
    LEFT JOIN Review R ON R.SubmissionID = S.id
    WHERE R.SubmissionID IS NULL
    """).fetchall()

    conn.commit()
    conn.close()

    return [eval(f"Submission{sub}") for sub in submissions]

def assign_review(submission: Submission, reviewer_id: int, completed_at: datetime = datetime.datetime.today()):
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO Review (ReviewerID, CourseID, SubmissionID, CompletedAt) 
                VALUES (?, ?, ?, ?)
                
    """, (reviewer_id, submission.course_id, submission.id, completed_at))

    conn.commit()
    conn.close()
                    

def _get_connection():
    conn = None

    try:
        conn = sqlite3.connect(DATABASE_PATH)        
    except:
        print("Unable to connect to database")
        exit()

    return conn