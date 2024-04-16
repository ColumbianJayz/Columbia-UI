import json, re
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

current_id = 6

Countries = {
   "1": {
        "countries_id": "1",
        "country": "Colombia",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/84/Flag-map_of_Venezuela.svg",
        #"audio_1": "",
        #"audio_2": "",
        "next_country": "2",
        "tips": "Que mas puessssssss!"
    },
    "2":{
        "countries_id": "2",
       "country": "Venezuela",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Flag-map_of_Colombia.svg",
        #"audio_1": "",
        #"audio_2": "",
        "next_country": "3"
    },
    "3":{
        "countries_id": "3",
        "country": "Argentina",
        "image": "https://upload.wikimedia.org/wikipedia/commons/7/79/Flag_map_of_Argentina.svg",
        #"audio_1": "",
        #"audio_2": "",
        "next_country": "4"
    },
    "4":{
       "countries_id": "4",
        "country": "Mexico",
        "image": " https://upload.wikimedia.org/wikipedia/commons/a/aa/Mexico_Flag_Map.svg",
        #"audio_1": "",
        #"audio_2": "",
        "next_country": "5"
    },
    "5":{
        "countries_id": "5",
        "country": "Puerto Rico",
        "image": " https://upload.wikimedia.org/wikipedia/commons/5/56/PR_flag_island.svg",
        #"audio_1": "",
        #"audio_2": "",
        "next_country": "6"
    },
    "6":{
        "countries_id": "6",
        "country": "El Salvador",
        "image": " https://upload.wikimedia.org/wikipedia/commons/9/99/Flag-map_of_El_Salvador.png",
        #"audio_1": "",
        #"audio_2": "",
        "next_country": "end"
    },
}

quiz_id = 6
quiz_questions = {
    "1": {
        "quiz_id": "1",
        "audio_quiz": "",
        "options": ["Colombia", "Venezuela", "Argentina", "Mexico"],
        "answer": "Venezuela",
        "next_question": "2"
    },
    "2": {
        "quiz_id": "2",
        "audio_quiz": "",
        "options": ["Venezuela", "Argentina", "Mexico", "Puerto Rico"],
        "answer": "Argentina",
        "next_question": "3"
    },
    "3": {
        "quiz_id": "3",
        "audio_quiz": "",
        "options": ["Argentina", "Mexico", "Puerto Rico", "El Salvador"],
        "answer": "Colombia",
        "next_question": "4"
    },
    "4": {
        "quiz_id": "4",
        "audio_quiz": "",
        "options": ["Mexico", "Puerto Rico", "El Salvador", "Colombia"],
        "answer": "El Salvador",
        "next_question": "5"
    },
    "5": {
        "quiz_id": "5",
        "audio_quiz": "",
        "options": ["Puerto Rico", "El Salvador", "Colombia", "Venezuela"],
        "answer": "Mexico",
        "next_question": "6"
    },
    "6": {
        "quiz_id": "6",
        "audio_quiz": "",
        "options": ["El Salvador", "Colombia", "Venezuela", "Argentina"],
        "answer": "Puerto Rico",
        "next_question": "end"
    }

}

#ROUTES: homepage, learn, quiz
@app.route('/')
def homepage():
    return render_template('homepage.html') #:data


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/learn/<countries_id>')
def learn(countries_id):
    item = Countries.get(countries_id)
    if item:
        return render_template('learn.html', item=item)
    else:
        return "Item not found", 404

@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    if request.method == 'POST':
        # Process answer here
        next_id = quiz_questions[quiz_id]['next_question']
        quiz_id = next_id if next_id != "end" else '1'  # Reset or redirect to some end page

    item = quiz_questions.get(quiz_id)
    if item:
        return render_template('quiz.html', item=item, quiz_id=quiz_id)
    else:
        return "Item not found", 404
    
"""
@app.route('/quiz/end')
def quiz_end():
    return render_template('quiz_end.html')
"""

if __name__ == '__main__':
    app.run(debug=True)