from flask import Flask, render_template, request, redirect, url_for, session
import random
import time
app = Flask(__name__)
app.secret_key = "secretkey"

# HangmanGame class
class HangmanGame:
    def __init__(self, course):
        self.course = course
        self.questions = self.get_questions(course)
        self.current_question_index = 0
        self.correct_answers = 0
        self.incorrect_attempts = 0
        self.max_attempts = 6

    def get_questions(self, course):
        data = {
            "Python": [
                {"question": "print(5 + _)", "answer": "5"},
                {"question": "def func(_):", "answer": "self"},
                {"question": "print('Hello, _!')", "answer": "World"},
                {"question": "for _ in range(5):", "answer": "i"},
                {"question": "if _ == '__main__':", "answer": "name"},
                {"question": "list = [1, 2, 3, _]", "answer": "4"},
                {"question": "return _ + y", "answer": "x"},
                {"question": "try:\n    x = 1/0\nexcept _:", "answer": "ZeroDivisionError"},
                {"question": "with open('file.txt', 'r') as _:", "answer": "file"},
                {"question": "class MyClass(_):", "answer": "object"}
            ],
            "HTML": [
                {"question": "<_ href='link'>Click</a>", "answer": "a"},
                {"question": "<div _='background-color:red;'>", "answer": "style"},
                {"question": "<img src='image.png' _='An image'>", "answer": "alt"},
                {"question": "<_ charset='UTF-8'>", "answer": "meta"},
                {"question": "<p _='text-align:center;'>Hello</p>", "answer": "style"},
                {"question": "<_ name='viewport' content='width=device-width, initial-scale=1.0'>", "answer": "meta"},
                {"question": "<button _='submit'>Submit</button>", "answer": "type"},
                {"question": "<ul>\n  <li>_</li>\n</ul>", "answer": "Item"},
                {"question": "<_ lang='en'>", "answer": "html"},
                {"question": "<table>\n  <_>Header</th>\n</table>", "answer": "th"}
            ],
            "CSS": [
                {"question": "background-_: url('image.png');", "answer": "image"},
                {"question": "font-_: Arial, sans-serif;", "answer": "family"},
                {"question": "margin-_: 10px;", "answer": "top"},
                {"question": "padding: 10px _ 20px;", "answer": "15px"},
                {"question": "border: 1px _ black;", "answer": "solid"},
                {"question": "display: _;", "answer": "flex"},
                {"question": "position: _;", "answer": "absolute"},
                {"question": "box-shadow: 0px 4px _px gray;", "answer": "10"},
                {"question": "transition: all 0.3s _;", "answer": "ease"},
                {"question": "overflow: _;", "answer": "hidden"}
            ],
        }
        return random.sample(data[course], 10)

# Questions data for Pop Quiz
quiz_questions = {
        "Python": [
    {
        "question": "What is the output of print(2**3)?",
        "choices": ["6", "8", "9", "12"],
        "answer": "8"
    },
    {
        "question": "Which of the following is a Python data type?",
        "choices": ["Integer", "Float", "String", "All of the above"],
        "answer": "All of the above"
    },
    {
        "question": "What is the correct file extension for Python files?",
        "choices": [".py", ".python", ".pt", ".p"],
        "answer": ".py"
    },
    {
        "question": "Which keyword is used to create a function in Python?",
        "choices": ["function", "def", "create", "func"],
        "answer": "def"
    },
    {
        "question": "Which operator is used for floor division?",
        "choices": ["/", "//", "%", "**"],
        "answer": "//"
    },
    {
        "question": "What does len() function do in Python?",
        "choices": ["Returns the length of a string", "Returns the number of elements in a list", "Both of the above", "None of the above"],
        "answer": "Both of the above"
    },
    {
        "question": "Which module in Python is used for generating random numbers?",
        "choices": ["math", "random", "os", "sys"],
        "answer": "random"
    },
    {
        "question": "Which method is used to add an element to a set in Python?",
        "choices": ["add()", "append()", "insert()", "push()"],
        "answer": "add()"
    },
    {
        "question": "What is the index of the first element in a Python list?",
        "choices": ["0", "1", "-1", "None of the above"],
        "answer": "0"
    },
    {
        "question": "How do you start a Python comment?",
        "choices": ["//", "/*", "#", "<!--"],
        "answer": "#"
    },
],

    "HTML": [
        {
            "question": "Which tag is used to define a hyperlink?",
            "choices": ["<a>", "<link>", "<href>", "<url>"],
            "answer": "<a>"
        },{
        "question": "Which tag is used to create an ordered list?",
        "choices": ["<ol>", "<ul>", "<li>", "<list>"],
        "answer": "<ol>"
    },
    {
        "question": "What does the <img> tag require to display an image?",
        "choices": ["src", "alt", "href", "both src and alt"],
        "answer": "both src and alt"
    },
    {
        "question": "Which tag is used to insert a line break?",
        "choices": ["<br>", "<lb>", "<break>", "<newline>"],
        "answer": "<br>"
    },
    {
        "question": "Which tag is used for the largest heading in HTML?",
        "choices": ["<h1>", "<heading>", "<h6>", "<header>"],
        "answer": "<h1>"
    },
    {
        "question": "What attribute is used to provide a unique identifier for an element?",
        "choices": ["id", "class", "name", "unique"],
        "answer": "id"
    },
    {
        "question": "Which tag is used to define a table row?",
        "choices": ["<row>", "<tr>", "<td>", "<table-row>"],
        "answer": "<tr>"
    },
    {
        "question": "What is the purpose of the <meta> tag?",
        "choices": [
            "To provide metadata about the HTML document",
            "To create a hyperlink",
            "To add a comment",
            "To style the document"
        ],
        "answer": "To provide metadata about the HTML document"
    },
    {
        "question": "Which tag is used to define a form in HTML?",
        "choices": ["<form>", "<input>", "<action>", "<fieldset>"],
        "answer": "<form>"
    },
    {
        "question": "Which attribute specifies where to open the linked document in an <a> tag?",
        "choices": ["target", "href", "link", "open"],
        "answer": "target"
    },
],
    "CSS": [
        {
            "question": "Which property is used to change the background color?",
            "choices": ["background", "color", "background-color", "bg-color"],
            "answer": "background-color"
        },
        {
        "question": "Which property is used to set the text color of an element?",
        "choices": ["color", "font-color", "text-color", "background-color"],
        "answer": "color"
    },
    {
        "question": "What is the default position value in CSS?",
        "choices": ["static", "relative", "absolute", "fixed"],
        "answer": "static"
    },
    {
        "question": "Which property is used to change the font of an element?",
        "choices": ["font-family", "font-style", "font", "text-font"],
        "answer": "font-family"
    },
    {
        "question": "Which property controls the size of text?",
        "choices": ["font-size", "text-size", "size", "text-style"],
        "answer": "font-size"
    },
    {
        "question": "Which property is used to add space inside the element border?",
        "choices": ["padding", "margin", "border", "spacing"],
        "answer": "padding"
    },
    {
        "question": "Which property specifies the stack order of elements?",
        "choices": ["z-index", "stack", "index", "order"],
        "answer": "z-index"
    },
    {
        "question": "Which unit is relative to the size of the parent element?",
        "choices": ["em", "px", "rem", "%"],
        "answer": "em"
    },
    {
        "question": "What is the purpose of the float property?",
        "choices": [
            "To position an element to the left or right",
            "To center an element",
            "To hide an element",
            "To make an element responsive"
        ],
        "answer": "To position an element to the left or right"
    },
    {
        "question": "Which property is used to create space between elements?",
        "choices": ["margin", "padding", "spacing", "border"],
        "answer": "margin"
    },
],
}

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/score")
def score():
    incorrect_answers = session.get('incorrect_answers', [])
    return render_template(
        "score.html", 
        score=session['score'], 
        total=len(session['questions']),
        incorrect_answers=incorrect_answers
    )

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        selected_choice = request.form.get("choice")
        current_question = session['current_question']
        question_data = session['questions'][current_question]

        if selected_choice == question_data['answer']:
            session['score'] += 1
        else:
            session['incorrect_answers'].append({
                "question": question_data['question'],
                "correct_answer": question_data['answer'],
                "your_answer": selected_choice
            })

        session['current_question'] += 1

        if session['current_question'] >= len(session['questions']):
            return redirect(url_for("score"))

    current_question = session['current_question']
    question_data = session['questions'][current_question]
    return render_template("quiz.html", question=question_data, question_number=current_question + 1)

@app.route("/select", methods=["GET", "POST"])
def select():
    if request.method == "POST":
        session['course'] = request.form.get("course")
        session['game'] = request.form.get("game")
        if session['game'] == "pop_quiz":
            session['questions'] = random.sample(quiz_questions[session['course']], 10)
            session['current_question'] = 0
            session['score'] = 0
            session['incorrect_answers'] = []
            return redirect(url_for("quiz"))
        elif session['game'] == "hangman":
            session['hangman'] = HangmanGame(session['course']).__dict__
            return redirect(url_for("hangman"))
    return render_template("select.html")

@app.route("/hangman", methods=["GET", "POST"])
def hangman():
    hangman_data = session.get('hangman', None)
    if not hangman_data:
        return redirect(url_for("select"))

    game = HangmanGame(hangman_data['course'])
    game.__dict__ = hangman_data

    if request.method == "POST":
        guess = request.form.get("guess")
        start_time = session.pop('start_time', time.time())
        elapsed_time = time.time() - start_time

        current_question = game.questions[game.current_question_index]

        if elapsed_time > 10:  # Time limit exceeded
            game.incorrect_attempts += 1
        elif guess and guess.lower() == current_question['answer'].lower():
            game.correct_answers += 1
        else:
            game.incorrect_attempts += 1

        game.current_question_index += 1

        # End game conditions
        if game.current_question_index >= len(game.questions) or game.incorrect_attempts >= 5:
            session['hangman_score'] = {
                "correct_answers": game.correct_answers,
                "incorrect_attempts": game.incorrect_attempts,
                "total_questions": len(game.questions),
                "incorrect_answers": [
                    {
                        "question": q['question'],
                        "correct_answer": q['answer']
                    }
                    for i, q in enumerate(game.questions) if i < game.current_question_index and i >= game.current_question_index - game.incorrect_attempts
                ]
            }
            return redirect(url_for("hangman_score"))

        session['hangman'] = game.__dict__
        session['start_time'] = time.time()

    current_question = game.questions[game.current_question_index]
    return render_template("hangman.html", question=current_question, game=game)


@app.route('/hangman_score')
def hangman_score():
    hangman_score = session.get('hangman_score', None)
    if not hangman_score:
        return redirect(url_for("select"))

    return render_template(
        'hangman_score.html',
        correct_answers=hangman_score["correct_answers"],
        incorrect_attempts=hangman_score["incorrect_attempts"],
        total_questions=hangman_score["total_questions"],
        incorrect_answers=hangman_score["incorrect_answers"]
    )


if __name__ == "__main__":
    app.run(debug=True)

