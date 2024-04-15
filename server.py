import json, re
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

current_id = 6

Countries = {
   "1": {
        "countries_id": "1",
        "country": "Colombia",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/84/Flag-map_of_Venezuela.svg",
        #"audio_1":
        #"audio_2":

        "next_country": "2"
    },
    "2":{
        "countries_id": "2",
       "country": "Venezuela",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Flag-map_of_Colombia.svg",
        #"audio_1":
        #"audio_2":
        "next_country": "3"
    },
    "3":{
        "countries_id": "3",
        "country": "Argentina",
        "image": "https://upload.wikimedia.org/wikipedia/commons/7/79/Flag_map_of_Argentina.svg",
        #"audio_1":
        #"audio_2":
        "next_country": "4"
    },
    "4":{
       "countries_id": "4",
        "country": "Mexico",
        "image": "",
        #"audio_1":
        #"audio_2":
        "next_country": "5"
    },
    "5":{
        "countries_id": "5",
        "country": "Puerto Rico",
        "image": "",
        #"audio_1":
        #"audio_2":
        "next_country": "6"
    },
    "6":{
        "countries_id": "6",
        "country": "El Salvador",
        "image": "",
        #"audio_1":
        #"audio_2":
        "next_country": "end"
    },
}

quiz_questions = {
    "1": {
        "quiz_id": "1",
        "options": ["Colombia", "Venezuela", "Argentina", "Mexico"],
        "answer": "Colombia",
        "next_question": "2"
    },
    "2": {
        "quiz_id": "2",
        "options": ["Venezuela", "Argentina", "Mexico", "Puerto Rico"],
        "answer": "Venezuela",
        "next_question": "3"
    },
    "3": {
        "quiz_id": "3",
        "options": ["Argentina", "Mexico", "Puerto Rico", "El Salvador"],
        "answer": "Argentina",
        "next_question": "4"
    },
    "4": {
        "quiz_id": "4",
        "options": ["Mexico", "Puerto Rico", "El Salvador", "Colombia"],
        "answer": "Mexico",
        "next_question": "5"
    },
    "5": {
        "quiz_id": "5",
        "options": ["Puerto Rico", "El Salvador", "Colombia", "Venezuela"],
        "answer": "Puerto Rico",
        "next_question": "6"
    },
    "6": {
        "quiz_id": "6",
        "options": ["El Salvador", "Colombia", "Venezuela", "Argentina"],
        "answer": "El Salvador",
        "next_question": "end"
    }

}

#ROUTES: homepage, learn, quiz
@app.route('/')
def homepage():
    return render_template('homepage.html') #:data

@app.route('/learn')
def learn():
    return render_template('learn.html') #:data

@app.route('/quiz')
def quiz():
    return render_template('quiz.html') #:data

if __name__ == '__main__':
    app.run(debug=True)