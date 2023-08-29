## Review Assignment 
A system for assigning reviews to a reviewer who is most likely to complete a take within the turn around time based on their prior review history.

## How it works
Based on the day of the week and time that a review is submitted, the system will look for the mentor who is most likely to complete the review within SLA. 

For example, if a task is submitted at 4pm on a Tuesday and has a deadline of 4pm the next day, the system will get the average number of reviews completed by each reviewer in the past `n` `Tuesday 4pm` to `Wednesday 4pm` periods. 

To get the probability of the review being competed, the current back log plus the new review will be compared to the historical average.

#### Benefits 
- Reviews are assigned to reviewers who are most productive between submission and deadline.
	- *A reviewer who completes less reviews between 2pm - 6pm is less likely to get a review in that time period than a review who is more productive at those times*
- Takes off days into consideration 
	- *if a task is assigned at 4pm on a Friday, a reviewer who doesn't work on weekends is less likely to get the review than a reviewer who works on a Saturday*
- Balances the review load based on how many reviews each reviewer can do 

#### Short Comings 
- Without some sort of random assignment, there is not chance of increasing a reviewers review average once it goes down without manually assigning reviews 

## Other Notes 
#### How I Got The Past Review Data 
I created a program that generate random reviews based the following factors for each reviewer.
- Expected reviews per hour 
- Hours with not reviews done (during the working day)
- Off days

The program runs for every day from the 1st of August to the 4th of September (This returns 4 results for each day of the week). 

The following pseudocode was used to generate the past reviews:
1. For each day in date range 
	1. Get each mentor working on the day 
	2. for each mentor working 
		1. Create `n` reviews for each hour of the working day, where `n` is a random number between `expected reviews - 2` and `expected reviews + 3`

## Running the Code

Will simulate 7 days of receiving 1 review per hour
``` cmd
python simulate_assignment.py
```





