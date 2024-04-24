import json
import re
from flask import Flask, render_template, Response, request, jsonify, session


app = Flask(__name__)

current_id = 6

Countries = {
    "1": {
        "countries_id": "1",
        "country": "Colombia",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Flag-map_of_Colombia.svg",
        "audio_1": "colombiaExamenes.m4a",
        "audio_2": "ColombiaFiesta.m4a",
        "next_country": "/learn/2",
        "tips": "Colombian Spanish is known for its clear and precise pronunciation of words. Unlike some other Latin American accents, Colombians typically articulate each syllable distinctly."
    },
    "2": {
        "countries_id": "2",
        "country": "Venezuela",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/84/Flag-map_of_Venezuela.svg",
        "audio_1": "venezuelan.mp3",
        "audio_2": "venezuelan.mp3",
        "next_country": "/learn/3",
        "tips": "Like in many other Spanish-speaking cultures, Venezuelans frequently use diminutives to express affection, make things sound smaller or cuter, or simply as part of everyday speech."
    },
    "3": {
        "countries_id": "3",
        "country": "Argentina",
        "image": "https://upload.wikimedia.org/wikipedia/commons/7/79/Flag_map_of_Argentina.svg",
        "audio_1": "argentinaExamenes.mp3",
        "audio_2": "argentinaLearning1.mp3",
        "next_country": "/learn/4",
        "tips": "In Argentina, the \'ll\' and \'y\' sounds are often pronounced like the English \'sh\' in \"sheep\" or \"shy.\" This is called yeísmo. For example, \"pollo\" (chicken) may sound like \"po-sho\"."
    },
    "4": {
        "countries_id": "4",
        "country": "Mexico",
        "image": " https://upload.wikimedia.org/wikipedia/commons/a/aa/Mexico_Flag_Map.svg",
        "audio_1": "mexicoExamenes.mp3",
        "audio_2": "mexicoFiesta.mp3",
        "next_country": "/learn/5",
        "tips": "Mexican Spanish tends to have clear and distinct vowel sounds. However, there are regional variations, and in some areas, vowels may be pronounced differently or with a nasal tone."
    },
    "5": {
        "countries_id": "5",
        "country": "Puerto Rico",
        "image": " https://upload.wikimedia.org/wikipedia/commons/5/56/PR_flag_island.svg",
        "audio_1": "Puerto Rico.mp3",
        "audio_2": "Puerto Rico.mp3",
        "next_country": "/learn/6",
        "tips": " In casual speech, especially in rapid conversation, Puerto Ricans often drop the 's' sound at the end of words or syllables. For example, \"gracias\" might sound like \"gracia.\""
    },
    "6": {
        "countries_id": "6",
        "country": "El Salvador",
        "image": " https://upload.wikimedia.org/wikipedia/commons/9/99/Flag-map_of_El_Salvador.png",
        "audio_1": "salvadoran.mp3",
        "audio_2": "salvadoran.mp3",
        "next_country": "/quiz/1",
        "tips": "El Salvador predominantly uses \"vos\" instead of \"tú\" for the informal second-person singular pronoun."
    },
}

quiz_id = 6
quiz_questions = {
    "1": {
        "quiz_id": "1",
        "audio_quiz": "venezuelan.mp3",
        "options": ["Colombia 🇨🇴", "Venezuela 🇻🇪", "Argentina 🇦🇷", "Mexico 🇲🇽"],
        "answer": "Venezuela 🇻🇪",
        "next_question": "2",
        "previous_question": None
    },
    "2": {
        "quiz_id": "2",
        "audio_quiz": "argentinan.mp3",
        "options": ["Venezuela 🇻🇪", "Argentina 🇦🇷", "Mexico 🇲🇽", "Puerto Rico 🇵🇷"],
        "answer": "Argentina 🇦🇷",
        "next_question": "3",
        "previous_question": "1"
    },
    "3": {
        "quiz_id": "3",
        "audio_quiz": "Colombia.mp3",
        "options": ["Argentina 🇦🇷", "Colombia 🇨🇴", "Puerto Rico 🇵🇷", "El Salvador 🇸🇻"],
        "answer": "Colombia 🇨🇴",
        "next_question": "4",
        "previous_question": "2"
    },
    "4": {
        "quiz_id": "4",
        "audio_quiz": "salvadoran.mp3",
        "options": ["Mexico 🇲🇽", "Puerto Rico 🇵🇷", "El Salvador 🇸🇻", "Colombia 🇨🇴"],
        "answer": "El Salvador 🇸🇻",
        "next_question": "5",
        "previous_question": "3"
    },
    "5": {
        "quiz_id": "5",
        "audio_quiz": "mexico.mp3",
        "options": ["Puerto Rico 🇵🇷", "El Salvador 🇸🇻", "Mexico 🇲🇽", "Venezuela 🇻🇪"],
        "answer": "Mexico 🇲🇽",
        "next_question": "6",
        "previous_question": "4"
    },
    "6": {
        "quiz_id": "6",
        "audio_quiz": "Puerto Rico.mp3",
        "options": ["El Salvador 🇸🇻", "Colombia 🇨🇴", "Puerto Rico 🇵🇷", "Argentina 🇦🇷"],
        "answer": "Puerto Rico 🇵🇷",
        "next_question": "end",
        "previous_question": "5"
    }

}

# ROUTES: homepage, learn, quiz


@app.route('/')
def homepage():
    return render_template('homepage.html')  # :data


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/learn/<countries_id>')
def learn(countries_id):
    audio_filename = Countries[countries_id]["audio_1"]
    audio_filename2 = Countries[countries_id]["audio_2"]
    item = Countries.get(countries_id)
    if item:
        return render_template('learn.html', item=item, audio_filename=audio_filename, audio_filename2=audio_filename2)
    else:
        return "Item not found", 404


@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    audio_filename = quiz_questions[quiz_id]["audio_quiz"]
    current_question_number = list(quiz_questions.keys()).index(quiz_id) + 1
    total_questions = len(quiz_questions)
    item = quiz_questions.get(quiz_id)

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        attempts = int(request.form.get('attempts', 0)) + 1
        score = int(request.form.get('score', 0))
        correct_answer = quiz_questions[quiz_id]['answer']
        was_correct = (user_answer == correct_answer)

        feedback_class = "correct-feedback" if was_correct else "incorrect-feedback"
        feedback = "Correct! Well done." if was_correct else "Incorrect! Try again." if attempts < 2 else f"Incorrect! The correct answer was {correct_answer}."
        score += 1 if was_correct else 0

        next_id = quiz_questions[quiz_id]['next_question'] if was_correct or attempts >= 2 else quiz_id
        
        if next_id == "end":
            return render_template('score.html', score=score)
        else:
            item = quiz_questions.get(next_id)
            return render_template('quiz.html', item=item, quiz_id=next_id, feedback=feedback, feedback_class=feedback_class, attempts=0 if was_correct else attempts, score=score, was_correct=was_correct, audio_filename=audio_filename, current_question_number=current_question_number, total_questions=total_questions)
    else:
        return render_template('quiz.html', item=item, quiz_id=quiz_id, feedback=None, feedback_class=None, attempts=0, score=0, was_correct=None, audio_filename=audio_filename, current_question_number=current_question_number, total_questions=total_questions)

@app.route('/audio/<path:filename>')
def download_file(filename):
    return send_from_directory('path/to/audio/directory', filename)


@app.route('/score/<int:score>')
def score(score):
    return render_template('score.html', score=score)


if __name__ == '__main__':
    app.run(debug=True)
