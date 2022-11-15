from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# RESPONSES_KEY will be the dictionary key inside of session. You will use this to access session data
# saving response key string out here ensures no typos later
RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    title = survey.title
    instructions = survey.instructions
    return render_template("home.html", title=title, instructions=instructions)

# @app.route('/questions/<num>')
# def list_questions(num):
#     num = 

# @app.route('/questions/0')
# def list_questions():
#     q0 = satisfaction_survey.questions[0]
#     return render_template("0.html", q0= q0)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice from question.html form 
    choice = request.form['answer']

    ## add this response to the session object

    # set responses to session[RESPONSES_KEY] which is a list of responses
    responses = session[RESPONSES_KEY]

    # add choice to responses
    responses.append(choice)

    # save responses to session object 
    session[RESPONSES_KEY] = responses

    # if survey.questions list is the same length as responses list
    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        # redirect to next question. if answered first question, len of responses is 1, will redirect to
        # questions/1 (which is the next question). first q was questions/0
        return redirect(f"/questions/{len(responses)}")


# unanswered questions redirects here

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    # if no responses in list send back to home
    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        # send back to proper page
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""
    question = survey.questions
    return render_template("completion.html", responses=session.get(RESPONSES_KEY), question = question )