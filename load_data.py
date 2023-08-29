from models import *
import pandas as pd
import datetime

REVIEWER_FILE = "data/reviewer_backlog.csv"
PAST_REVIEWS_FILE = "data/data.csv"

def get_past_reviews():
    '''
        Get all of the past reviews

        @Returns 
            output (List[PastReview]) : completed reviews
    '''

    reviews = pd.read_csv(PAST_REVIEWS_FILE)
    
    output = []
    for i in range(len(reviews)):
        completed_time = _convert_time(reviews.loc[i, 'completed_time'])
        completed_date = _convert_date(reviews.loc[i, 'completed_date'])

        review = PastReview(completed_by=reviews.loc[i, 'completed_by'],
                            course=reviews.loc[i, 'course'],
                            completed_date=completed_date,
                            completed_time=completed_time,
                            day_of_week=completed_date.weekday())
        output.append(review)

    return output

def _convert_date(date_string: str):
    '''
        Converts the date string from the CSV to a date objec 

        @Params 
            date_string (str) : Date string of M/D/YYYY format 

        @Return 
            (datetime.date) : date object
    '''
    month, day, year = date_string.split('/')

    return datetime.date(int(year), int(month), int(day))

def _convert_time(time_string: str):
    '''
        Converts the time string to a time object 

        @Params 
            time_string (str) : Time string of MM:HH <AM/PM>

        @Return 
            (datetime.time)  : time object
    '''
    time, tod = time_string.split()
    hour, min = time.split(':')

    hour = int(hour)
    min = int(min)

    if (tod == 'PM'):
        hour += 12 % 12

    return datetime.time(hour, min, 0)

def get_reviewers() -> Reviewer:
    '''
        Gets all reviews from file 

        @Returns
            output (List[Reviewer]) : List of reviewers 
    '''
    reviewers = pd.read_csv(REVIEWER_FILE)

    output = []

    for i in range(len(reviewers)):
        reviewer = Reviewer(name=reviewers.loc[i, 'name'], 
                            courses=reviewers.loc[i, 'courses'].split(':'),
                            backlog=int(reviewers.loc[i, 'backlog']))

        output.append(reviewer)

    return output

def increment_backlog(reviewer_name: str):
    '''
        Adds a review to a reviewers backlog 

        @Params 
            reviewer_name (str) : Reviewer whose backlog should be updated        
    '''
    reviewers = pd.read_csv(REVIEWER_FILE)

    index = reviewers.loc[reviewers.name == reviewer_name.lower()].index[0]
    reviewers.at[index, "backlog"] += 1

    reviewers.to_csv(REVIEWER_FILE, index=False)

def reset_backlog():
    '''
        Sets the backlog to 0 for all reviewers
    '''
    reviewers = pd.read_csv(REVIEWER_FILE)
    
    reviewers.backlog = 0

    reviewers.to_csv(REVIEWER_FILE, index=False)

def get_backlog():
    reviewers = pd.read_csv(REVIEWER_FILE)
    return reviewers