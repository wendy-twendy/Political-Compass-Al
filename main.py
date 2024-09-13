from flask import Flask, render_template, request, jsonify
import plotly.graph_objects as go
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Updated Quiz questions
questions = [
    "The free market is the most effective way to distribute resources.",
    "Government intervention in the economy is necessary to protect citizens.",
    "Private property rights should be protected at all costs.",
    "A strong welfare system is essential for a just society.",
    "Corporations should be subject to strict regulations.",
    "Labor unions are essential for protecting workers' rights.",
    "Taxation is a form of theft.",
    "Universal healthcare should be provided by the government.",
    "Education should be privatized.",
    "Environmental regulations are necessary to combat climate change.",
    "The government should have a strong military presence.",
    "Police powers should be limited to protect civil liberties.",
    "Freedom of speech should be absolute, with no restrictions.",
    "The death penalty is a just form of punishment for severe crimes.",
    "Gun ownership is a fundamental right that should not be infringed upon.",
    "Same-sex marriage should be legally recognized.",
    "Abortion should be legal and accessible.",
    "Immigration policies should be more restrictive.",
    "Racial and ethnic minorities should receive special protections.",
    "Religion should play a role in government policy-making."
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=questions)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    try:
        answers = request.json
        logging.debug(f"Received answers: {answers}")
        
        if not answers or len(answers) != 20:
            return jsonify({"error": "Invalid input: 20 answers required"}), 400
        
        # Calculate political compass coordinates
        economic_score = 0
        libertarian_authoritarian_score = 0
        
        economic_questions = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
        libertarian_authoritarian_questions = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        
        for i, answer in enumerate(answers):
            if not isinstance(answer, (int, float)) or answer < 1 or answer > 5:
                return jsonify({"error": f"Invalid answer for question {i+1}: must be between 1 and 5"}), 400
            
            if i in economic_questions:
                economic_score += (answer - 3) * 0.5
            elif i in libertarian_authoritarian_questions:
                libertarian_authoritarian_score += (answer - 3) * 0.5
        
        # Normalize scores to be between -10 and 10
        economic_score = max(min(economic_score, 10), -10)
        libertarian_authoritarian_score = max(min(libertarian_authoritarian_score, 10), -10)
        
        logging.debug(f"Calculated scores: economic={economic_score}, libertarian_authoritarian={libertarian_authoritarian_score}")
        
        fig = go.Figure()
        
        # Add quadrants with updated colors
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
        
        # Update grid lines to stay within [-10, 10] range
        for i in range(-4, 5):
            fig.add_shape(type="line", x0=-10, x1=10, y0=i*2.5, y1=i*2.5, line=dict(color="rgba(255,255,255,0.8)", width=1))
            fig.add_shape(type="line", x0=i*2.5, x1=i*2.5, y0=-10, y1=10, line=dict(color="rgba(255,255,255,0.8)", width=1))
        
        # Add black center lines
        fig.add_shape(type="line", x0=0, x1=0, y0=-10, y1=10, line=dict(color="black", width=2))
        fig.add_shape(type="line", x0=-10, x1=10, y0=0, y1=0, line=dict(color="black", width=2))
        
        # Update layout with exact [-10, 10] plot range
        fig.update_layout(
            xaxis=dict(range=[-10, 10], zeroline=False, showticklabels=False),
            yaxis=dict(range=[-10, 10], zeroline=False, showticklabels=False),
            showlegend=False,
            width=700,
            height=700,
            margin=dict(l=80, r=80, t=80, b=80),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        
        # Add axis labels with adjusted positions, font size, and weight
        fig.add_annotation(x=-10, y=0, text="Left", showarrow=False, xanchor="right", yanchor="middle", xref="x", yref="y", font=dict(size=16, weight=900, color="black"))
        fig.add_annotation(x=10, y=0, text="Right", showarrow=False, xanchor="left", yanchor="middle", xref="x", yref="y", font=dict(size=16, weight=900, color="black"))
        fig.add_annotation(x=0, y=10, text="Authoritarian", showarrow=False, xanchor="center", yanchor="bottom", xref="x", yref="y", font=dict(size=16, weight=900, color="black"))
        fig.add_annotation(x=0, y=-10, text="Libertarian", showarrow=False, xanchor="center", yanchor="top", xref="x", yref="y", font=dict(size=16, weight=900, color="black"))
        
        # Add user's position as the last element
        fig.add_trace(go.Scatter(
            x=[economic_score],
            y=[libertarian_authoritarian_score],
            mode="markers+text",
            marker=dict(color="red", size=12, symbol="square"),
            text=["You"],
            textposition="top center",
            textfont=dict(size=12, color="black")
        ))
        
        # Convert the figure to JSON for frontend rendering
        plot_json = fig.to_json()
        
        response = jsonify({
            'economic': economic_score,
            'libertarian_authoritarian': libertarian_authoritarian_score,
            'plot_json': plot_json
        })
        logging.debug("Successfully created response")
        return response
    except Exception as e:
        logging.exception("An error occurred while processing the quiz submission")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
