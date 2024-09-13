from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app import db
from models import UserData, questions, municipalities
from utils import generate_plot, get_quadrant_explanation
import logging

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
  return render_template('home.html')


@bp.route('/demographics')
def demographics():
  return render_template('demographics.html', municipalities=municipalities)


@bp.route('/submit_demographics', methods=['POST'])
def submit_demographics():
  age = request.form.get('age')
  sex = request.form.get('sex')
  education = request.form.get('education')
  city = request.form.get('city')
  session['demographics'] = {
      'age': age,
      'sex': sex,
      'education': education,
      'city': city
  }
  return redirect(url_for('main.quiz'))


@bp.route('/quiz')
def quiz():
  return render_template('quiz.html', questions=questions)


@bp.route('/submit_quiz', methods=['POST'])
def submit_quiz():
  try:
    answers = request.json
    logging.debug(f"Received answers: {answers}")
    if not answers or len(answers) != 20:
      return jsonify({"error": "Invalid input: 20 answers required"}), 400
    # Calculate political compass coordinates
    economic_score = 0
    libertarian_authoritarian_score = 0
    # Questions lists as given before
    economic_questions = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    libertarian_authoritarian_questions = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    for i, answer in enumerate(answers):
      if not isinstance(answer, (int, float)) or answer < 1 or answer > 5:
        return jsonify({
            "error":
            f"Invalid answer for question {i+1}: must be between 1 and 5"
        }), 400
      if i in economic_questions:
        economic_score += (answer - 3) * 0.5
      elif i in libertarian_authoritarian_questions:
        libertarian_authoritarian_score += (answer - 3) * 0.5
    # Normalize scores to be between -10 and 10
    economic_score = max(min(economic_score, 10), -10)
    libertarian_authoritarian_score = max(
        min(libertarian_authoritarian_score, 10), -10)
    logging.debug(
        f"Calculated scores: economic={economic_score}, libertarian_authoritarian={libertarian_authoritarian_score}"
    )
    # Generate the plot using the calculated scores
    plot_json = generate_plot(economic_score, libertarian_authoritarian_score)
    # Get quadrant explanation
    quadrant, explanation = get_quadrant_explanation(
        economic_score, libertarian_authoritarian_score)
    # Create mockup comparisons for demonstration purposes
    comparisons = {
        'average_scores': {
            'overall': {
                'economic': 2.5,
                'social': -1.5
            },
            'age_group': {
                'economic': 3.0,
                'social': -2.0
            },
            'sex': {
                'economic': 1.5,
                'social': -1.0
            },
            'country': {
                'economic': 2.0,
                'social': -1.8
            }
        },
        'famous_figures': {
            'Figure 1': {
                'economic': -3.0,
                'social': 4.0
            },
            'Figure 2': {
                'economic': 6.0,
                'social': -2.0
            },
            'Figure 3': {
                'economic': -1.0,
                'social': 0.0
            }
        }
    }
    # Store answers in session for sharing
    session['user_answers'] = answers
    # Save user data to the database
    user_data = UserData(
        age=session['demographics']['age'],
        sex=session['demographics']['sex'],
        education=session['demographics']['education'],
        city=session['demographics']['city'],
        answers=answers,
        economic_score=economic_score,
        libertarian_authoritarian_score=libertarian_authoritarian_score)
    db.session.add(user_data)
    db.session.commit()
    # Log the saved data
    logging.info(f"Saved user data to database: {user_data}")
    response = jsonify({
        'economic': economic_score,
        'libertarian_authoritarian': libertarian_authoritarian_score,
        'plot_json': plot_json,
        'quadrant': quadrant,
        'explanation': explanation,
        'economic_intensity': abs(economic_score),
        'social_intensity': abs(libertarian_authoritarian_score),
        'comparisons': comparisons
    })
    logging.debug("Successfully created response")
    return response
  except Exception as e:
    logging.exception("An error occurred while processing the quiz submission")
    return jsonify({"error": str(e)}), 500


@bp.route('/shared_result')
def shared_result():
  try:
    economic = float(request.args.get('economic'))
    libertarian_authoritarian = float(
        request.args.get('libertarian_authoritarian'))
    answers = request.args.get('answers')
    if answers:
      answers = [int(a) for a in answers.split(',')]
    else:
      answers = [3] * 20  # Default to neutral if not provided
  except (TypeError, ValueError):
    return redirect(url_for('main.quiz'))
  plot_json = generate_plot(economic, libertarian_authoritarian)
  quadrant, explanation = get_quadrant_explanation(economic,
                                                   libertarian_authoritarian)
  return render_template('shared_result.html',
                         result={
                             'economic': economic,
                             'libertarian_authoritarian':
                             libertarian_authoritarian,
                             'plot_json': plot_json,
                             'user_answers': answers,
                             'quadrant': quadrant,
                             'explanation': explanation,
                             'economic_intensity': abs(economic),
                             'social_intensity': abs(libertarian_authoritarian)
                         },
                         questions=questions)
