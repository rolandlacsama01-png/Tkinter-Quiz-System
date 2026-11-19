# Tkinter-Quiz-System
 
*Name: Lacsama Roland Jr
*Section: SE-3A
*Topic: Computer Hardware
 
## Features Completed
10 multiple-choice questions
Random question order
20-second countdown timer
Answer checking and time-out handling
Score and percentage
Answer review
High score saved in a text file
Restart button
 
## How the Questions Are Stored and Shuffled
 question can be stored in a list or dictionaries, and python used the random.shuffle().
 
## How the Timer Works
python use import time start_time = time.time() it counts time in seconds, and when quiz starts it record, when answer is submitted the recording ending time.
 
## How the Program Identifies the Correct Answer
each question has an answer key that contains the correct answer, the program use the user_answer = input("Your answer: ")
 
## How the Score and High Score Work
 it calculate based on the number of correct answers and dividing the total number of question the code use score = 0, (correct answer / total questions) x 100
 
## Function Explanations
| Function | Purpose | Called when |
|----------|---------|-------------|
|   
High_score() records or save highest score  | reopening the game or after all answering 10 questions
Score() to calculate user performance  | when finishing answering all question
Automatic answer checking() when determine and identify if correct or incorrect  | when after answering the question
Countdown_timer()   to limit the user answering the question   | when answering another question or didn't answer
Question shuffle() reset and suffle the question    |   reloading or starting the game   
 
## Screenshots
![Start screen](screenshots/start.png)
![Question screen](screenshots/question.png)
![Answer feedback](screenshots/feedback.png)
![Results screen](screenshots/results.png)
![High score after reopening](screenshots/high_score.png)
 
## Challenges I Faced
The difficult thing i face when creating this mini game is what to put inside in question, and making a clear UI design and clean line of codes, and by solving it by just doing some adjustment in spacings, cama, i manage to make the code look presentable.
