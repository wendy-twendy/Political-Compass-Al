import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# List of questions
questions = [
    "The government should provide universal healthcare.",
    "Private property rights are essential for a free society.",
    "A strong welfare system is necessary to protect the poor.",
    "Corporations should have fewer regulations.",
    "Climate change is a serious threat that requires immediate action.",
    "The free market is more efficient than government intervention.",
    "Same-sex marriage should be legal.",
    "Gun ownership is a fundamental right.",
    "Immigration policies should be more restrictive.",
    "Higher taxes on the wealthy are necessary to reduce income inequality.",
    "Abortion should be legal and accessible.",
    "Privatization of public services leads to better efficiency.",
    "Military spending should be increased for national security.",
    "Labor unions are essential for protecting workers' rights.",
    "Stronger environmental regulations are needed to protect nature.",
    "School choice and voucher systems improve education.",
    "The death penalty should be abolished.",
    "Free trade agreements benefit the economy.",
    "Recreational drug use should be decriminalized.",
    "A strong social safety net discourages personal responsibility."
]

# Initialize an empty list to store quiz results
quiz_results = []

# Famous political figures with their positions
famous_figures = {
    "Bernie Sanders": {"economic": -8, "social": -7},
    "Donald Trump": {"economic": 7, "social": 6},
    "Joe Biden": {"economic": -2, "social": -3},
    "Elizabeth Warren": {"economic": -6, "social": -5},
    "Ron Paul": {"economic": 9, "social": -8},
    "Alexandria Ocasio-Cortez": {"economic": -9, "social": -8}
}

def generate_plot(economic, social):
    fig = go.Figure()

    # Add quadrants
    quadrants = [
        {"name": "Authoritarian Left", "x": [-10, 0, 0, -10], "y": [0, 0, 10, 10], "color": "#ff7575"},
        {"name": "Authoritarian Right", "x": [0, 10, 10, 0], "y": [0, 0, 10, 10], "color": "#42aaff"},
        {"name": "Libertarian Left", "x": [-10, 0, 0, -10], "y": [0, 0, -10, -10], "color": "#9aed97"},
        {"name": "Libertarian Right", "x": [0, 10, 10, 0], "y": [0, 0, -10, -10], "color": "#c09aec"}
    ]

    for quadrant in quadrants:
        fig.add_trace(go.Scatter(
            x=quadrant["x"], y=quadrant["y"],
            fill="toself",
            fillcolor=quadrant["color"],
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False,
            hoverinfo="skip"
        ))

    # Add grid lines
    for i in range(-10, 11):
        fig.add_shape(type="line", x0=-10, x1=10, y0=i, y1=i, line=dict(color="white", width=1))
        fig.add_shape(type="line", x0=i, x1=i, y0=-10, y1=10, line=dict(color="white", width=1))

    # Add black lines in the center
    fig.add_shape(type="line", x0=0, x1=0, y0=-10, y1=10, line=dict(color="black", width=2))
    fig.add_shape(type="line", x0=-10, x1=10, y0=0, y1=0, line=dict(color="black", width=2))

    # Add the main point
    fig.add_trace(go.Scatter(
        x=[economic],
        y=[social],
        mode="markers+text",
        marker=dict(color="red", size=12, symbol="square"),
        text=["You"],
        textposition="top center",
        textfont=dict(size=12, color="black"),
        name="Your Position"
    ))

    # Add famous figures
    for name, position in famous_figures.items():
        fig.add_trace(go.Scatter(
            x=[position['economic']],
            y=[position['social']],
            mode="markers+text",
            marker=dict(size=8, symbol="circle"),
            text=[name],
            textposition="top center",
            textfont=dict(size=10),
            name=name
        ))

    # Add axis labels
    fig.add_annotation(x=-10, y=0, text="Left", showarrow=False, xanchor="right", yanchor="middle", font=dict(size=16, weight="bold"))
    fig.add_annotation(x=10, y=0, text="Right", showarrow=False, xanchor="left", yanchor="middle", font=dict(size=16, weight="bold"))
    fig.add_annotation(x=0, y=10, text="Authoritarian", showarrow=False, xanchor="center", yanchor="bottom", font=dict(size=16, weight="bold"))
    fig.add_annotation(x=0, y=-10, text="Libertarian", showarrow=False, xanchor="center", yanchor="top", font=dict(size=16, weight="bold"))

    # Update layout
    fig.update_layout(
        xaxis=dict(range=[-10, 10], zeroline=False, showticklabels=False),
        yaxis=dict(range=[-10, 10], zeroline=False, showticklabels=False),
        showlegend=True,
        legend=dict(x=1.05, y=1, bordercolor="Black", borderwidth=1),
        width=800,
        height=800,
        margin=dict(l=50, r=150, t=50, b=50),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    return pio.to_json(fig)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user_info', methods=['GET'])
def user_info():
    return render_template('user_info.html')

@app.route('/submit_demographics', methods=['POST'])
def submit_demographics():
    age = request.form.get('age')
    location = request.form.get('location')
    gender = request.form.get('gender')
    
    session['user_info'] = {
        'age': age,
        'location': location,
        'gender': gender
    }
    
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=questions)

def calculate_average_scores():
    if not quiz_results:
        return 0, 0
    avg_economic = sum(result['economic'] for result in quiz_results) / len(quiz_results)
    avg_social = sum(result['social'] for result in quiz_results) / len(quiz_results)
    return avg_economic, avg_social

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    answers = request.json
    
    economic_score = sum(answers[i-1] for i in [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]) / 50 * 20 - 10
    libertarian_authoritarian_score = sum(answers[i-1] for i in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]) / 50 * 20 - 10
    
    result = {
        'economic': economic_score,
        'social': libertarian_authoritarian_score,
        'timestamp': datetime.now().isoformat(),
        'user_info': session.get('user_info', {})
    }
    quiz_results.append(result)
    
    avg_economic, avg_social = calculate_average_scores()
    plot_json = generate_plot(economic_score, libertarian_authoritarian_score)
    
    quadrant = get_quadrant(economic_score, libertarian_authoritarian_score)
    explanation = get_quadrant_explanation(quadrant, economic_score, libertarian_authoritarian_score)
    
    comparisons = []
    for name, position in famous_figures.items():
        distance = ((economic_score - position['economic'])**2 + (libertarian_authoritarian_score - position['social'])**2)**0.5
        comparisons.append({'name': name, 'distance': distance})
    comparisons.sort(key=lambda x: x['distance'])
    closest_figure = comparisons[0]['name']
    
    return jsonify({
        'economic': economic_score,
        'libertarian_authoritarian': libertarian_authoritarian_score,
        'plot_json': plot_json,
        'quadrant': quadrant,
        'explanation': explanation,
        'average_economic': avg_economic,
        'average_social': avg_social,
        'closest_figure': closest_figure,
        'comparisons': comparisons[:3]  # Return top 3 closest figures
    })

def get_quadrant(economic, social):
    if economic >= 0 and social >= 0:
        return "Authoritarian Right"
    elif economic >= 0 and social < 0:
        return "Libertarian Right"
    elif economic < 0 and social >= 0:
        return "Authoritarian Left"
    else:
        return "Libertarian Left"

def get_quadrant_explanation(quadrant, economic, social):
    intensity = max(abs(economic), abs(social)) / 10  # Normalize to 0-1 range
    
    if quadrant == "Authoritarian Right":
        return f"You fall in the Authoritarian Right quadrant. With an economic score of {economic:.2f} and a social score of {social:.2f}, you tend to favor free-market capitalism and traditional social values. Your intensity score of {intensity:.2f} suggests a {'strong' if intensity > 0.6 else 'moderate'} alignment with these principles."
    
    elif quadrant == "Libertarian Right":
        return f"You are in the Libertarian Right quadrant. Your economic score of {economic:.2f} indicates a preference for free markets, while your social score of {social:.2f} suggests a belief in personal freedoms. With an intensity of {intensity:.2f}, you have a {'strong' if intensity > 0.6 else 'moderate'} libertarian right leaning."
    
    elif quadrant == "Authoritarian Left":
        return f"Your results place you in the Authoritarian Left quadrant. An economic score of {economic:.2f} shows a tendency towards economic regulation, while a social score of {social:.2f} indicates support for more government involvement in social issues. Your intensity score of {intensity:.2f} implies a {'strong' if intensity > 0.6 else 'moderate'} authoritarian left stance."
    
    elif quadrant == "Libertarian Left":
        return f"You're situated in the Libertarian Left quadrant. With an economic score of {economic:.2f}, you lean towards economic regulation, but your social score of {social:.2f} suggests a strong belief in personal freedoms. Your intensity of {intensity:.2f} indicates a {'strong' if intensity > 0.6 else 'moderate'} libertarian left position."
    
    else:  # Centrist
        return f"Your scores (Economic: {economic:.2f}, Social: {social:.2f}) place you near the center of the political compass. This suggests a balanced or moderate view on both economic and social issues. With an intensity of {intensity:.2f}, you have a {'slight' if intensity < 0.3 else 'moderate'} tendency towards centrist positions."

@app.route('/shared_result')
def shared_result():
    economic = float(request.args.get('economic', 0))
    libertarian_authoritarian = float(request.args.get('libertarian_authoritarian', 0))
    answers = list(map(int, request.args.get('answers', '').split(',')))
    
    plot_json = generate_plot(economic, libertarian_authoritarian)
    
    quadrant = get_quadrant(economic, libertarian_authoritarian)
    explanation = get_quadrant_explanation(quadrant, economic, libertarian_authoritarian)
    
    result = {
        'economic': economic,
        'libertarian_authoritarian': libertarian_authoritarian,
        'plot_json': plot_json,
        'quadrant': quadrant,
        'explanation': explanation,
        'user_answers': answers
    }
    
    return render_template('shared_result.html', result=result, questions=questions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
