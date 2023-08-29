import load_data
from models import *
import datetime
from typing import List, Dict, Set, Tuple

TURN_AROUND_TIME = 1 # How soon reviews should be done
TRAINING_PERIOD = 4 #How many weeks back we go to view past review averages

def get_suggested_reviewer(new_review: NewReview):
    '''
        Get the reviewer with the highest probability of finishing review in SLA

        @Params 
            new_review (NewReview) : Unassigned review

        @Returns 
            reviewer_probability (Dict[string, float]) : reviewer name as key and the probability as the value
            best_reviewer (string) : name of the reviewer with the best probability
    '''
    course_reviewers = _get_reviewers_for_course(new_review.course)

    reviewer_probability = {reviewer.name: - 1 for reviewer in course_reviewers}
    best_reviewer = None


    for reviewer in course_reviewers:
        potential_backlog = reviewer.backlog + 1                                                                    # Total backlog if new review is added

        average_in_period = _get_historical_review_total(new_review.get_datetime(), reviewer.name)
        average_in_period /= TRAINING_PERIOD

        if average_in_period == 0:
            continue

        reviewer_probability[reviewer.name] = 1 - (potential_backlog/average_in_period)

        if (best_reviewer == None or reviewer_probability[reviewer.name] > reviewer_probability[best_reviewer]):
            best_reviewer = reviewer.name

    return reviewer_probability, best_reviewer
    

def _get_reviewers_for_course(review_course: str) -> Set[Reviewer]:
    '''
        Get reviewers for a given course

        @Params
            review_course (str) : Course to be reviewed

        @Returns 
            output (Set[Reviewer]) : Set of reviewers for a given course
    '''
    reviewers = load_data.get_reviewers()

    output = set()

    for reviewer in reviewers:
        if (review_course.upper() in reviewer.courses):
            output.add(reviewer)

    return output

def _get_historical_review_total(submission_time: datetime, reviewer: str):
    '''
        Get the total reviews done in the past on a given day of the week at the currently required time range

        @Params
            submission_time (datetime) : The time the new review was submitted
            reviewer (str) : The name of the reviewer being considered

        @Returns
            int : total reviews done in the period
    '''
    past_reviews = load_data.get_past_reviews()

    reviews_by_reviewer = _get_reviews_by_reviewer(reviewer, past_reviews)
    
    return _get_past_total_in_turn_around_time(reviews_by_reviewer, submission_time)

def _get_reviews_by_reviewer(reviewer_name: str, reviews: List[PastReview]):
    '''
        Filters reviews done by a single reviewer

        @Params
            reviewer_name (str) : Reviewer whose reviews are being checked
            reviews (List[PastReview]) : Reviews to be filtered
        
        @Returns 
            output (List[PastReviews]) : List of filtered reviews
    '''
    output = []

    for review in reviews:
        if review.completed_by.lower() == reviewer_name.lower():
            output.append(review)

    return output

def _get_past_total_in_turn_around_time(reviews_by_reviewer: List[PastReview], start_datetime: datetime):
    '''
        Gets the total reviews done in the past where the day of the week and time match the range for the next submission

        @Params 
            reviews_by_reviewer (List[PastReview]) : List of reviews done by a single reviewer 
            start_datetime (datetime) : When the new review was submitted
        
        @Returns
            total (int) : total number of reviews completed in period
    '''
    end_datetime = start_datetime + datetime.timedelta(days=TURN_AROUND_TIME)

    # Get days of week in review range 
    current_date = start_datetime
    days_of_week = []

    while (current_date <= end_datetime):
        days_of_week.append(current_date.date().weekday())
        current_date += datetime.timedelta(days=1)

    reviews = _get_reviews_in_days(reviews_by_reviewer, days_of_week)

    # Remove review done before submission time
    reviews[days_of_week[0]] = [review for review in reviews[days_of_week[0]] 
                                if review.completed_time > start_datetime.time()]

    # Remove reviews done after deadline time
    reviews[days_of_week[-1]] = [reviews for review in reviews[days_of_week[-1]] 
                                 if review.completed_time < start_datetime.time()]
    
    total = 0

    for day in days_of_week:
        total += len(reviews[day])

    return total
    

def _get_reviews_in_days(reviews: List[PastReview], days: List[int]) -> Dict[int, List[PastReview]]:
    '''
        Gets the reviews completed on certain days of the week 

        @Params
            reviews (List[PastReview]) : Reviews to be filtered
            days (List[int]) : The days that should be extracted 

        @Returns 
            output (Dict[int, List[PastReviews]]) : 
    '''
    output = {day: [] for day in days}

    for review in reviews:        
        if (review.day_of_week not in output):
            continue        

        output[review.day_of_week].append(review)
    
    return output