import tkinter as tk
from tkinter import ttk, messagebox
import random
import os


# ================= QUESTIONS =================

questions = {
    "General Knowledge": [
        ("What is the capital of India?",
         ["Mumbai", "New Delhi", "Kolkata", "Chennai"], "New Delhi"),

        ("How many days are there in a week?",
         ["5", "6", "7", "8"], "7"),

        ("Which is the largest ocean?",
         ["Indian Ocean", "Atlantic Ocean", "Pacific Ocean", "Arctic Ocean"],
         "Pacific Ocean"),

        ("How many continents are there?",
         ["5", "6", "7", "8"], "7"),

        ("Which planet is known as the Red Planet?",
         ["Earth", "Mars", "Jupiter", "Venus"], "Mars")
    ],

    "Python": [
        ("Which keyword is used to define a function?",
         ["function", "def", "fun", "define"], "def"),

        ("Which symbol is used for comments in Python?",
         ["//", "<!-- -->", "#", "**"], "#"),

        ("Which data type stores True or False?",
         ["String", "Integer", "Boolean", "List"], "Boolean"),

        ("Which function displays output?",
         ["input()", "print()", "output()", "display()"], "print()"),

        ("Which extension is used for Python files?",
         [".java", ".html", ".py", ".cpp"], ".py")
    ],

    "Science": [
        ("What is the chemical formula of water?",
         ["CO2", "H2O", "O2", "NaCl"], "H2O"),

        ("Which organ pumps blood?",
         ["Brain", "Lungs", "Heart", "Kidney"], "Heart"),

        ("Which gas do humans need to breathe?",
         ["Oxygen", "Carbon dioxide", "Hydrogen", "Nitrogen"],
         "Oxygen"),

        ("What is the center of an atom called?",
         ["Electron", "Proton", "Nucleus", "Neutron"], "Nucleus"),

        ("Which force pulls objects toward Earth?",
         ["Friction", "Gravity", "Magnetism", "Pressure"], "Gravity")
    ]
}


# ================= VARIABLES =================

current_question = 0
score = 0
selected_category = ""
quiz_questions = []

time_left = 10
timer_id = None
answer_locked = False


# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("Quiz Master")
root.geometry("700x600")
root.resizable(False, False)


# ================= START QUIZ =================

def start_quiz():

    global selected_category
    global quiz_questions
    global current_question
    global score
    global answer_locked

    name = name_entry.get().strip()

    if name == "":
        messagebox.showwarning(
            "Name Required",
            "Please enter your name!"
        )
        return

    selected_category = category_var.get()

    if selected_category == "":
        messagebox.showwarning(
            "Category Required",
            "Please select a category!"
        )
        return

    quiz_questions = questions[selected_category].copy()
    random.shuffle(quiz_questions)

    current_question = 0
    score = 0
    answer_locked = False

    start_frame.pack_forget()
    result_frame.pack_forget()
    quiz_frame.pack(fill="both", expand=True)

    show_question()


# ================= SHOW QUESTION =================

def show_question():

    global time_left
    global timer_id
    global answer_locked

    answer_locked = False

    # Cancel previous timer
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    question, options, correct_answer = quiz_questions[current_question]

    question_label.config(
        text=f"Question {current_question + 1} / 5\n\n{question}"
    )

    # Update progress bar
    progress["value"] = current_question + 1

    # Connect every button to check_answer()
    for i in range(4):
        option_buttons[i].config(
            text=options[i],
            state="normal",
            command=lambda answer=options[i]: check_answer(answer)
        )

    # Reset timer
    time_left = 10
    timer_label.config(
        text=f"Time: {time_left} seconds"
    )

    countdown()


# ================= TIMER =================

def countdown():

    global time_left
    global timer_id

    timer_label.config(
        text=f"Time: {time_left} seconds"
    )

    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1000, countdown)

    else:
        timer_id = None
        time_up()


# ================= TIME UP =================

def time_up():

    global current_question
    global answer_locked

    if answer_locked:
        return

    answer_locked = True

    for button in option_buttons:
        button.config(state="disabled")

    correct_answer = quiz_questions[current_question][2]

    messagebox.showinfo(
        "Time's Up!",
        f"⏰ Time's up!\n\nCorrect answer: {correct_answer}"
    )

    current_question += 1

    if current_question < len(quiz_questions):
        show_question()
    else:
        finish_quiz()


# ================= CHECK ANSWER =================

def check_answer(answer):

    global current_question
    global score
    global timer_id
    global answer_locked

    if answer_locked:
        return

    answer_locked = True

    # Stop timer immediately
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    # Disable buttons
    for button in option_buttons:
        button.config(state="disabled")

    correct_answer = quiz_questions[current_question][2]

    if answer == correct_answer:

        score += 1

        messagebox.showinfo(
            "Answer",
            "Correct! ✅"
        )

    else:

        messagebox.showinfo(
            "Answer",
            f"Wrong! ❌\n\nCorrect answer: {correct_answer}"
        )

    # Move to next question
    current_question += 1

    if current_question < len(quiz_questions):
        show_question()
    else:
        finish_quiz()


# ================= FINISH QUIZ =================

def finish_quiz():

    global timer_id

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    quiz_frame.pack_forget()
    result_frame.pack(fill="both", expand=True)

    name = name_entry.get().strip()

    result_label.config(
        text=(
            "🎉 QUIZ COMPLETED 🎉\n\n"
            f"Name: {name}\n"
            f"Category: {selected_category}\n"
            f"Score: {score} / 5"
        )
    )

    if score == 5:

        message_label.config(
            text="🏆 Excellent!"
        )

    elif score >= 3:

        message_label.config(
            text="🎉 Good Job!"
        )

    else:

        message_label.config(
            text="💪 Keep Practicing!"
        )

    save_score()
    show_leaderboard()


# ================= SAVE SCORE =================

def save_score():

    name = name_entry.get().strip()

    with open("leaderboard.txt", "a") as file:

        file.write(
            f"{name} | {selected_category} | {score}/5\n"
        )


# ================= LEADERBOARD =================

def show_leaderboard():

    leaderboard_text.delete(
        "1.0",
        tk.END
    )

    if not os.path.exists("leaderboard.txt"):

        leaderboard_text.insert(
            tk.END,
            "No scores yet."
        )

        return

    with open(
        "leaderboard.txt",
        "r"
    ) as file:

        scores = file.readlines()

    if len(scores) == 0:

        leaderboard_text.insert(
            tk.END,
            "No scores yet."
        )

        return

    for position, player in enumerate(
        scores,
        start=1
    ):

        leaderboard_text.insert(
            tk.END,
            f"{position}. {player.strip()}\n"
        )


# ================= PLAY AGAIN =================

def play_again():

    global timer_id

    if timer_id is not None:

        root.after_cancel(timer_id)
        timer_id = None

    result_frame.pack_forget()
    quiz_frame.pack_forget()

    start_frame.pack(
        fill="both",
        expand=True
    )


# ================= EXIT =================

def exit_app():

    global timer_id

    if timer_id is not None:

        root.after_cancel(timer_id)

    root.destroy()


# ================= START FRAME =================

start_frame = tk.Frame(root)

title_label = tk.Label(
    start_frame,
    text="🎯 QUIZ MASTER",
    font=("Arial", 30, "bold")
)

title_label.pack(pady=30)


subtitle_label = tk.Label(
    start_frame,
    text="Test Your Knowledge!",
    font=("Arial", 16)
)

subtitle_label.pack(pady=5)


name_label = tk.Label(
    start_frame,
    text="Enter your name:",
    font=("Arial", 14, "bold")
)

name_label.pack(pady=15)


name_entry = tk.Entry(
    start_frame,
    font=("Arial", 14),
    width=25
)

name_entry.pack()


category_title = tk.Label(
    start_frame,
    text="Choose a Category:",
    font=("Arial", 16, "bold")
)

category_title.pack(pady=20)


category_var = tk.StringVar()


for category in questions.keys():

    tk.Radiobutton(
        start_frame,
        text=category,
        variable=category_var,
        value=category,
        font=("Arial", 13)
    ).pack(pady=4)


start_button = tk.Button(
    start_frame,
    text="START QUIZ 🚀",
    font=("Arial", 14, "bold"),
    command=start_quiz,
    width=18,
    height=2
)

start_button.pack(pady=25)


# ================= QUIZ FRAME =================

quiz_frame = tk.Frame(root)


timer_label = tk.Label(
    quiz_frame,
    text="Time: 10 seconds",
    font=("Arial", 16, "bold")
)

timer_label.pack(pady=15)


progress = ttk.Progressbar(
    quiz_frame,
    length=500,
    maximum=5,
    mode="determinate"
)

progress.pack(pady=10)


question_label = tk.Label(
    quiz_frame,
    text="",
    font=("Arial", 18, "bold"),
    wraplength=600,
    justify="center"
)

question_label.pack(pady=30)


option_buttons = []


for i in range(4):

    button = tk.Button(
        quiz_frame,
        text="",
        font=("Arial", 13),
        width=40,
        height=2
    )

    button.pack(pady=6)

    option_buttons.append(button)


# ================= RESULT FRAME =================

result_frame = tk.Frame(root)


result_label = tk.Label(
    result_frame,
    text="",
    font=("Arial", 20, "bold"),
    justify="center"
)

result_label.pack(pady=20)


message_label = tk.Label(
    result_frame,
    text="",
    font=("Arial", 17)
)

message_label.pack(pady=5)


leaderboard_title = tk.Label(
    result_frame,
    text="🏆 LEADERBOARD",
    font=("Arial", 18, "bold")
)

leaderboard_title.pack(pady=10)


leaderboard_text = tk.Text(
    result_frame,
    width=50,
    height=8,
    font=("Arial", 11)
)

leaderboard_text.pack()


play_button = tk.Button(
    result_frame,
    text="PLAY AGAIN 🔄",
    font=("Arial", 13, "bold"),
    command=play_again,
    width=15
)

play_button.pack(
    side="left",
    padx=40,
    pady=20
)


exit_button = tk.Button(
    result_frame,
    text="EXIT ❌",
    font=("Arial", 13, "bold"),
    command=exit_app,
    width=15
)

exit_button.pack(
    side="right",
    padx=40,
    pady=20
)


# ================= START APPLICATION =================

start_frame.pack(
    fill="both",
    expand=True
)

root.mainloop()