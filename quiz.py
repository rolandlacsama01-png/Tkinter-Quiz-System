import tkinter as tk
from tkinter import messagebox
import random
import os


QUESTIONS = [
    {
        "question": "Which component is often called the brain of the computer?",
        "choices": ["A. RAM", "B. CPU", "C. Monitor", "D. Keyboard"],
        "answer": "B"
    },
    {
        "question": "Which component temporarily stores data while programs are running?",
        "choices": ["A. RAM", "B. SSD", "C. Power supply", "D. Printer"],
        "answer": "A"
    },
    {
        "question": "Which device is mainly used to display visual output?",
        "choices": ["A. Mouse", "B. Microphone", "C. Monitor", "D. Scanner"],
        "answer": "C"
    },
    {
        "question": "What does SSD stand for?",
        "choices": [
            "A. System Storage Disk",
            "B. Solid State Drive",
            "C. Secure System Data",
            "D. Serial Storage Device"
        ],
        "answer": "B"
    },
    {
        "question": "Which component supplies electrical power to the computer?",
        "choices": [
            "A. CPU cooler",
            "B. Motherboard",
            "C. Power supply unit",
            "D. Graphics card"
        ],
        "answer": "C"
    },
    {
        "question": "Which device is commonly used to move the pointer on the screen?",
        "choices": ["A. Mouse", "B. Speaker", "C. Webcam", "D. Projector"],
        "answer": "A"
    },
    {
        "question": "Which part connects the major components of a computer?",
        "choices": ["A. Monitor", "B. Motherboard", "C. Case fan", "D. Headphones"],
        "answer": "B"
    },
    {
        "question": "Which component helps render graphics and videos?",
        "choices": [
            "A. Network card",
            "B. Sound card",
            "C. Graphics processing unit",
            "D. Power button"
        ],
        "answer": "C"
    },
    {
        "question": "Which of these is an input device?",
        "choices": ["A. Printer", "B. Speaker", "C. Monitor", "D. Keyboard"],
        "answer": "D"
    },
    {
        "question": "What is the main purpose of a computer cooling fan?",
        "choices": [
            "A. To increase storage",
            "B. To prevent components from overheating",
            "C. To improve internet speed",
            "D. To display images"
        ],
        "answer": "B"
    }
]



TIME_LIMIT = 20
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)

BG = "#FBFCFE"
CARD = "#234DD5"
DARK = "#000000"
ACCENT = "#A51420"
ACCENT_HOVER = "#CAFF2C"
GREEN = "#16834A"
RED = "#C43D4B"
MUTED = "#65728A"

root = tk.Tk()
root.title("TechQuest | Computer Hardware Quiz")
root.geometry("760x680")
root.configure(bg=BG)
root.resizable(False, False)


quiz_questions = []
current_question = 0
score = 0
time_left = TIME_LIMIT
wrong_answers = []
timer_job = None
answered = False
selected_answer = tk.StringVar()


main_frame = tk.Frame(root, bg=BG)
main_frame.pack(fill="both", expand=True, padx=34, pady=24)

timer_label = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []



def get_high_score():
    """Read the saved high score from the text file."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as file:
                return int(file.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def save_high_score(new_score):
    """Save the new score only when it is higher than the old record."""
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as file:
            file.write(str(new_score))
        return True
    return False



def clear_screen():
    """Remove all widgets from the main frame before showing another screen."""
    for widget in main_frame.winfo_children():
        widget.destroy()


def get_choice_text(question, letter):
    """Find and return the full choice text that matches a letter."""
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"


def make_button(parent, text, command, width=16):
    """Create a consistently styled application button."""
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        font=("Arial", 11, "bold"),
        bg=ACCENT,
        fg="white",
        activebackground=ACCENT_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=10,
        pady=9
    )



def show_start_screen():
    """Display the welcome screen and the saved high score."""
    clear_screen()

    tk.Label(
        main_frame, text="TECHQUEST", font=("Arial", 30, "bold"),
        bg=BG, fg=ACCENT
    ).pack(pady=(55, 5))

    tk.Label(
        main_frame, text="COMPUTER HARDWARE CHALLENGE",
        font=("Arial", 14, "bold"), bg=BG, fg=DARK
    ).pack(pady=5)

    tk.Label(
        main_frame,
        text="Test what you know about the parts inside and around a computer.",
        font=("Arial", 11), bg=BG, fg=MUTED, wraplength=580
    ).pack(pady=(8, 25))

    info_card = tk.Frame(main_frame, bg=CARD, padx=30, pady=22,
                         highlightbackground="#DCE3EF", highlightthickness=1)
    info_card.pack(pady=8)

    tk.Label(
        info_card, text=f"{len(QUESTIONS)} QUESTIONS",
        font=("Arial", 14, "bold"), bg=CARD, fg=DARK
    ).pack(pady=4)
    tk.Label(
        info_card, text=f"{TIME_LIMIT} seconds for every question",
        font=("Arial", 11), bg=CARD, fg=MUTED
    ).pack(pady=4)
    tk.Label(
        info_card,
        text=f"PERSONAL BEST: {get_high_score()} / {len(QUESTIONS)}",
        font=("Arial", 13, "bold"), bg=CARD, fg=GREEN
    ).pack(pady=(12, 4))

    make_button(main_frame, "START QUIZ", start_quiz, 20).pack(pady=25)

    tk.Label(
        main_frame, text="Choose one answer for each question. Good luck!",
        font=("Arial", 10, "italic"), bg=BG, fg=MUTED
    ).pack(pady=5)



def start_quiz():
    """Reset the quiz and create a randomly ordered question list."""
    global quiz_questions, current_question, score, wrong_answers
    stop_timer()
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()


def show_question():
    """Build the question screen, reset the timer, and display four choices."""
    global time_left, answered, timer_label, feedback_label
    global submit_button, next_button, choice_buttons

    clear_screen()
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]

    header = tk.Frame(main_frame, bg=BG)
    header.pack(fill="x", pady=(5, 15))

    tk.Label(
        header,
        text=f"QUESTION {current_question + 1} OF {len(quiz_questions)}",
        font=("Arial", 12, "bold"), bg=BG, fg=DARK
    ).pack(side="left")

    timer_label = tk.Label(
        header, text="", font=("Arial", 12, "bold"), bg=BG, fg=RED
    )
    timer_label.pack(side="right")

    tk.Label(
        main_frame, text=f"Current score: {score}",
        font=("Arial", 10), bg=BG, fg=MUTED
    ).pack(anchor="w", pady=(0, 10))

    card = tk.Frame(
        main_frame, bg=CARD, padx=26, pady=24,
        highlightbackground="#DCE3EF", highlightthickness=1
    )
    card.pack(fill="x", pady=5)

    tk.Label(
        card, text=question["question"], font=("Arial", 16, "bold"),
        bg=CARD, fg=DARK, wraplength=620, justify="left"
    ).pack(anchor="w", pady=(0, 20))

    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        radio = tk.Radiobutton(
            card, text=choice, variable=selected_answer, value=letter,
            font=("Arial", 12), bg=CARD, fg=DARK,
            activebackground=CARD, selectcolor="#DCE7FA",
            anchor="w", padx=8, pady=8, wraplength=590,
            justify="left"
        )
        radio.pack(fill="x", anchor="w", pady=3)
        choice_buttons.append(radio)

    feedback_label = tk.Label(
        main_frame, text="", font=("Arial", 11, "bold"),
        bg=BG, fg=DARK, wraplength=620
    )
    feedback_label.pack(pady=16)

    button_row = tk.Frame(main_frame, bg=BG)
    button_row.pack(pady=8)

    submit_button = make_button(button_row, "SUBMIT ANSWER", submit_answer)
    submit_button.pack(side="left", padx=8)

    button_text = "VIEW RESULTS" if current_question == len(quiz_questions) - 1 else "NEXT QUESTION"
    next_button = make_button(button_row, button_text, next_question)
    next_button.config(state="disabled")
    next_button.pack(side="left", padx=8)

    update_timer()


def update_timer():
    """Update the countdown once per second without freezing the window."""
    global time_left, timer_job

    if answered:
        return

    timer_label.config(
        text=f"TIME LEFT: {time_left}s",
        fg=RED if time_left <= 5 else ACCENT
    )

    if time_left <= 0:
        time_up()
        return

    time_left -= 1
    timer_job = root.after(1000, update_timer)


def stop_timer():
    """Cancel the scheduled countdown callback, if one exists."""
    global timer_job
    if timer_job is not None:
        try:
            root.after_cancel(timer_job)
        except tk.TclError:
            pass
        timer_job = None



def lock_choices():
    """Disable every radio button after the question has been answered."""
    for button in choice_buttons:
        button.config(state="disabled")


def submit_answer():
    """Check the selected answer and prevent a second submission."""
    global score, answered

    if answered:
        return

    choice = selected_answer.get()
    if not choice:
        messagebox.showwarning("No answer selected", "Please choose an answer first.")
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    if choice == question["answer"]:
        score += 1
        feedback_label.config(text="Correct! Great job.", fg=GREEN)
    else:
        correct_text = get_choice_text(question, question["answer"])
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": correct_text
        })
        feedback_label.config(
            text=f"Not quite. Correct answer: {correct_text}", fg=RED
        )

    next_button.config(state="normal")


def time_up():
    """Mark the question wrong when the countdown reaches zero."""
    global answered

    if answered:
        return

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    correct_text = get_choice_text(question, question["answer"])
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time ran out)",
        "correct_answer": correct_text
    })

    feedback_label.config(
        text=f"Time is up! Correct answer: {correct_text}", fg=RED
    )
    next_button.config(state="normal")


def next_question():
    """Move to the next question or display the final results."""
    global current_question

    if not answered:
        return

    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()



def show_results():
    """Display the final score, performance message, and incorrect answers."""
    stop_timer()
    clear_screen()

    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)

    if percentage >= 90:
        performance = "Outstanding! You really know your hardware."
    elif percentage >= 70:
        performance = "Great work! You have a good understanding."
    elif percentage >= 50:
        performance = "Good effort. Keep learning and practicing."
    else:
        performance = "Keep studying. You can do better next time."

    tk.Label(
        main_frame, text="QUIZ COMPLETED",
        font=("Arial", 25, "bold"), bg=BG, fg=ACCENT
    ).pack(pady=(5, 8))

    tk.Label(
        main_frame, text=f"{score} / {total}",
        font=("Arial", 32, "bold"), bg=BG, fg=DARK
    ).pack(pady=2)

    tk.Label(
        main_frame, text=f"Final percentage: {percentage:.0f}%",
        font=("Arial", 14, "bold"), bg=BG, fg=ACCENT
    ).pack(pady=4)

    tk.Label(
        main_frame, text=performance,
        font=("Arial", 11), bg=BG, fg=MUTED, wraplength=620
    ).pack(pady=5)

    record_message = (
        "NEW PERSONAL BEST!" if new_record
        else f"Personal best: {get_high_score()} / {total}"
    )
    tk.Label(
        main_frame, text=record_message,
        font=("Arial", 12, "bold"), bg=BG, fg=GREEN
    ).pack(pady=5)

    tk.Label(
        main_frame, text="ANSWER REVIEW",
        font=("Arial", 12, "bold"), bg=BG, fg=DARK
    ).pack(anchor="w", pady=(12, 5))

    review_frame = tk.Frame(main_frame, bg=CARD)
    review_frame.pack(fill="both", expand=True, pady=3)

    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")

    review_box = tk.Text(
        review_frame, height=9, wrap="word", font=("Arial", 10),
        yscrollcommand=scrollbar.set, bg=CARD, fg=DARK,
        padx=10, pady=8, relief="flat"
    )
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)

    if not wrong_answers:
        review_box.insert("end", "Perfect score! You answered all questions correctly.")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n")

    review_box.config(state="disabled")

    button_row = tk.Frame(main_frame, bg=BG)
    button_row.pack(pady=12)
    make_button(button_row, "PLAY AGAIN", start_quiz).pack(side="left", padx=8)
    make_button(button_row, "EXIT", on_close).pack(side="left", padx=8)



def on_close():
    """Stop the timer before closing the application."""
    stop_timer()
    root.destroy()



root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()