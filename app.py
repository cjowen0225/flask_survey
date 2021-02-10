from flask import Flask, request, session, render_template, flash, redirect
"from flask_debugtoolbar import DebugToolbarExtension"
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
responses_key = "responses"
"debug = DebugToolbarExtension(app)"

@app.route("/")
def start_page():
    """Show the home page with survey selections"""

    return render_template("start_page.html", survey=survey)

@app.route("/start_page", methods=["POST"])
def start_survey():
    """Create an empty responses array for the survey"""

    session[responses_key] = []

    return redirect("/questions/0")

@app.route("/questions/<int:qnum>")
def question_display(qnum):
    """Display the Question"""

    responses = session.get(responses_key)

    if (responses is None):
        return redirect("/")
    elif(len(responses) == len(survey.questions)):
        return redirect("/gratitude")
    
    if (len(responses) != qnum):
        if (qnum >= len(survey.questions)):
            flash(f"There is no question {qnum + 1}.")
            return redirect(f"/questions/{len(responses)}")
        else:
            flash(f"You cannot access question {qnum + 1}.")
            return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qnum]
    return render_template('question.html', q_num=qnum, question=question)

@app.route("/answer", methods=["POST"])
def save_response():
    """Save the question response and move on"""

    responses = session[responses_key]
    selection = request.form['answer']
    responses.append(selection)
    session[responses_key] = responses

    if(len(responses) == len(survey.questions)):
        return redirect("/gratitude")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/gratitude")
def gratitude():
    """Thank the user for completing the survey"""

    return render_template("gratitude.html")