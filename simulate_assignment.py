import review_assignment
from models import *
import random
import load_data
from tabulate import tabulate
import sys

def run_simulation(total_days: int, reviews_per_hour: int):
    '''
        Simulate students making review submissions 

        @Params 
            total_days (int) : The total number of days the simulation should run for
            reviews_per_hour : The number of reviews that should be created per hour         
    '''
    load_data.reset_backlog()
    reviews = _generate_reviews(total_days, reviews_per_hour)

    for review in reviews:
        reviewers_prob = review_assignment.get_suggested_reviewer(review)
        
        load_data.increment_backlog(reviewers_prob[1])

        draw_table()    
    
def _generate_reviews(total_days: int, reviews_per_hour: int):
    '''
        Generates a list of reviews submitted at a given time 

        @Params 
            total_days (int) : The total number of days the simulation should run for
            reviews_per_hour : The number of reviews that should be created per hour 

        @Returns 
            new_reviews (List[NewReview]) : List of reviews submitted
    '''
    start_date = get_start_datetime()
    end_date = start_date + datetime.timedelta(days=total_days)

    new_reviews = []

    while (start_date <= end_date):
        new_reviews.extend([NewReview("ds", start_date.date(), start_date.time()) 
                            for i in range(reviews_per_hour)])
        
        start_date += datetime.timedelta(hours=1)

    return new_reviews

def get_start_datetime():
    '''
        Generate a random day to start creating reviews from
    '''
    day = random.randrange(1,32)
    hour = random.randrange(9, 18)
    return datetime.datetime(year=2023, month=8, day=day, hour=hour, minute=0)

def draw_table():
    '''
        Display the table with the current backlog
    '''
    reviewer_backlog = load_data.get_backlog()

    print("\n\n", tabulate(reviewer_backlog, headers=reviewer_backlog.columns))


if __name__ == '__main__':
    run_simulation(7, 1)