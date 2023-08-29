from typing import List
from datetime import date, time
import datetime

class Reviewer():
    def __init__(self, name: str, courses: List[str], backlog: int):
        self.name = name
        self.courses = courses
        self.backlog = backlog

    def __str__(self):
        return f"""
            {self.name},
            {self.courses},
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


