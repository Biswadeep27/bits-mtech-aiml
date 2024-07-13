from flask import Flask, request, jsonify, render_template
from spelling_correction import SpellingCorrector

app = Flask(__name__)
corrector = SpellingCorrector('./data/spam_txt_msg_20170820.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/correct', methods=['POST'])
def correct():
    data = request.json
    text = data['text']
    corrected_text = corrector.correct_text(text)
    return jsonify({'corrected_text': corrected_text})

if __name__ == '__main__':
    app.run(debug=True)