# Smart Calendar
## Project Overview
I was inspired to make this project because I am someone that values productivity and efficiency very much. I am an avid user of Google Calendar in conjunction with Google Tasks to help me plan my weeks and stay ahead of my tasks and goals. However, I spend an awful amount of time deciding *when* I should tackle a specific task, through constant reordering of my calendar. 

Then I considered the work we have been tackling in Algorithms and AI, which are basically creating heuristics and processes with or without the use of data, to tackle problems. It is simply a process of proceduralizing intuition. This is my goal with the smart calendar. 

Given my deadlines, to-do list, recurrent tasks, events, socials, etc. it should automatically sort my calendar and **intelligently** form to-do lists for every day of the week. 

## Feature List
* **Inputs**:
  * Task, deadline, social, exam, etc.
  * Given it's priority (e.g. high priority will make sure the event comes earlier in the calendar)
  * Given any deadline
  * Given the (estimated) duration taken to finish the event (if it's a task) or duration of the event (if it's a social or recurrent event)
   * Given the individual's preferences e.g. time allocated for revision
* **Processing**:
  * Must utilize some form of CSPs (aka Constraint Satisfaction Problems) therefore may require an algorithm for arc and node consistency
  * May utilize a priority system based on arbitrary integers.
  * Perhaps some form of machine learning algorithm that can learn the habits of the user and adjust accordingly
  * Everytime a new event is added, there must be some form of reprocessing to adjust the calendar for any new priorities or if a more efficient option has opened up
* **Output**:
	* Spits out a fully fledged calendar with all your events fully sorted.
	* Examples:
		* Today is the 10th of April, and there is an exam on the 20th. Based on the rest of my schedule and my preference, it will schedule x amount of revision days with revision times prior to the 20th.
		* Imagine a fully sorted calendar. Someone would like to book an appointment with you -- the calendar will automatically pick the ideal time for this meeting.
		* If there is a clash in events, the calendar should automatically sort in terms of priority, and inform the user of any potential clashes, and provide ideal options.

## Technical Specifications
(Will be updated throughout project)
* Written in Python 3
* No front-end focus for this project
* etc.