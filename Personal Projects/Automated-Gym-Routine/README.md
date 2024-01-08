# Automated Gym Routine

## Project Overview
I personally find it cumbersome to do trivial tasks that have deterministic outcomes myself because of how much time I waste doing it everyday. I believe that automating these tasks with code is an investment into saving time in the future. One such time waster is constructing an exercise routine for the gym.

I am a huge advocate for Renaissance Periodization, which is a group that focuses efforts towards sharing scientific research in digestible ways to the general public to optimize workouts. As such, I wanted to utilize algorithmic paradigms I know to build a project that automates creating a gym routine for you based on your soreness levels and RP's ideals.

As a brief overview, the program should be able to take the individual's soreness levels per muscle group, and intelligently decide which exercises you should do based on what muscles are not sore. However, it should also be able to aggregate your recent soreness levels for your individual muscles to decide whether to change your volume (set count) for the exercise.

## Day 0 1/7/24
Thus far, I've only thought about the project abstractly and realized that the amount of time I take to decide these things and create spreadsheets for my routines can be done automatically.

I also want to note that I use ChatGPT as my assistant when I work on projects. I understand that it can't get code right every single time, but it is useful when I want something trivial to be done that I do not want to waste my time with. I used it in this project to create a CSV file to hold exercises that pertain to a particular muscle group so that my program will be able to fetch one when needed.

## Day 1 1/8/24
I've built out a rough outline of my project:
![Automated Gym Routine Flowchart](![Alt text](<Flowchart for Automated Gym Project.jpg>))
    ### Motivations
    