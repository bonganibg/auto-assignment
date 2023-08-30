from typing import List
from datetime import date, time
import datetime

class Reviewer():
    def __init__(self, id: int, name: str, backlog: int):
        self.name = name
        self.id = id
        self.backlog = backlog

    def __str__(self):
        return f"""
            {self.id},
            {self.name},            
            {self.backlog}
        """

    
class PastReview():

    def __init__(self, completed_by: str,course: str, completed_date: date, 
                completed_time: time, day_of_week: str):
        self.completed_by = completed_by
        self.course = course
        self.completed_date = completed_date
        self.completed_time = completed_time
        self.day_of_week = day_of_week

    def __str__(self):
        return f"""
            {self.course},
            {self.completed_by},
            {self.completed_date},
            {self.completed_time},
            {self.day_of_week}
        """
class Review():

    def __init__(self, id: int, reviewer_id: int, course_id: int, sub_id: int, completed_at: str) -> None:
        self.id = id
        self.reviewer_id = reviewer_id
        self.course_id = course_id
        self.sub_id = sub_id
        self.completed_at = self._convert_string_to_date(completed_at)

    def _convert_string_to_date(self, date_string: str) -> datetime:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        
class Submission():

    def __init__(self, id: int, course_id: int, submission_date: datetime) -> None:
        self.id = id
        self.course_id = course_id
        self.submission_date = submission_date                

class NewReview():

    def __init__(self, course, submitted_date: date, submitted_time: time):
        self.course = course
        self.submitted_date = submitted_date
        self.submitted_time = submitted_time

    def get_datetime(self):
        new_datetime = datetime.datetime(year=self.submitted_date.year, 
                                         month=self.submitted_date.month, 
                                         day=self.submitted_date.day, 
                                         hour=self.submitted_time.hour, 
                                         minute=self.submitted_time.minute)
        return new_datetime
    
    def __str__(self):
        return f"""
            {self.course},
            {self.submitted_date},
            {self.submitted_time}
        """


