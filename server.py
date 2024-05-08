import json
import re
from flask import Flask, render_template, Response, request, jsonify, session


app = Flask(__name__)

current_id = 6
current_score = 0

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
        "audio_1": "VenezuelaExamanes.m4a",
        "audio_2": "VenezuelaFiesta.m4a",
        "next_country": "/learn/3",
        "tips": "Like in many other Spanish-speaking cultures, Venezuelans frequently use diminutives to express affection, make things sound smaller or cuter, or simply as part of everyday speech."
    },
    "3": {
        "countries_id": "3",
        "country": "Argentina",
        "image": "https://upload.wikimedia.org/wikipedia/commons/7/79/Flag_map_of_Argentina.svg",
        "audio_1": "argentinaExamenes.mp3",
        "audio_2": "ArgentinaFiesta.mp3",
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
        "audio_1": "PuertoRicoExamenes.mp3",
        "audio_2": "PuertoRicoFiesta.mp3",
        "next_country": "/learn/6",
        "tips": " In casual speech, especially in rapid conversation, Puerto Ricans often drop the 's' sound at the end of words or syllables. For example, \"gracias\" might sound like \"gracia.\""
    },
    "6": {
        "countries_id": "6",
        "country": "El Salvador",
        "image": " https://upload.wikimedia.org/wikipedia/commons/9/99/Flag-map_of_El_Salvador.png",
        "audio_1": "ElSalvadorExamenes.m4a",
        "audio_2": "ElSalvadorFiesta.m4a",
        "next_country": "/quiz/1",
        "tips": "El Salvador predominantly uses \"vos\" instead of \"tú\" for the informal second-person singular pronoun."
    },
}

quiz_id = 6
quiz_questions = {
    "1": {
        "quiz_id": "1",
        "audio_quiz": "venezuela carro.m4a",
        "audio_quiz_2": "venezuelan.mp3",
        "options": ["Colombia 🇨🇴", "Venezuela 🇻🇪", "Argentina 🇦🇷", "Mexico 🇲🇽"],
        "answer": "Venezuela 🇻🇪",
        "next_question": "2",
        "previous_question": None
    },
    "2": {
        "quiz_id": "2",
        "audio_quiz": "argentinaAuto.mp3",
        "audio_quiz_2": "ArgentinaFiesta.mp3",
        "options": ["Venezuela 🇻🇪", "Argentina 🇦🇷", "Mexico 🇲🇽", "Puerto Rico 🇵🇷"],
        "answer": "Argentina 🇦🇷",
        "next_question": "3",
        "previous_question": "1"
    },
    "3": {
        "quiz_id": "3",
        "audio_quiz": "colombiaCarro.mp3",
        "audio_quiz_2": "ColombiaFiesta.m4a",
        "options": ["Argentina 🇦🇷", "Colombia 🇨🇴", "Puerto Rico 🇵🇷", "El Salvador 🇸🇻"],
        "answer": "Colombia 🇨🇴",
        "next_question": "4",
        "previous_question": "2"
    },
    "4": {
        "quiz_id": "4",
        "audio_quiz": "ElSalvadorExamenes.m4a",
        "audio_quiz_2": "ElSalvadorFiesta.m4a",
        "options": ["Mexico 🇲🇽", "Puerto Rico 🇵🇷", "El Salvador 🇸🇻", "Colombia 🇨🇴"],
        "answer": "El Salvador 🇸🇻",
        "next_question": "5",
        "previous_question": "3"
    },
    "5": {
        "quiz_id": "5",
        "audio_quiz": "mexico.mp3",
        "audio_quiz_2": "mexicoFiesta.mp3",
        "options": ["Puerto Rico 🇵🇷", "El Salvador 🇸🇻", "Mexico 🇲🇽", "Venezuela 🇻🇪"],
        "answer": "Mexico 🇲🇽",
        "next_question": "6",
        "previous_question": "4"
    },
    "6": {
        "quiz_id": "6",
        "audio_quiz": "Puerto Rico.mp3",
        "audio_quiz_2": "PuertoRicoFiesta.mp3",
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
    global current_score
    audio_filename = quiz_questions[quiz_id]["audio_quiz"]
    audio_filename2 = quiz_questions[quiz_id]["audio_quiz_2"]
    current_question_number = list(quiz_questions.keys()).index(quiz_id) + 1
    total_questions = len(quiz_questions)
    item = quiz_questions.get(quiz_id)
    total_questions=len(quiz_questions)

    if request.method == 'POST':
        data = request.get_json()
        selected_option = data['option']
        attempts = data['attempts']
        score = data['score']
        current_answer = item['answer']


        if selected_option == item['answer']:
            feedback = "Correct!"
            feedback_class = "correct-feedback"
            current_score += 1  # Increment score
        else:
            feedback_class = "incorrect-feedback"
            if attempts == 0:
                feedback = "Incorrect! Try again."
                attempts += 1
            else:
                feedback = f"Incorrect! The correct answer was {current_answer}."
                attempts += 1

        return jsonify({
            'feedback': feedback,
            'feedback_class': feedback_class,
            'score': current_score,
            'attempts': attempts,
            'current_question_number': current_question_number,
            'total_questions': total_questions
        })

    return render_template('quiz.html', item=item, quiz_id=quiz_id, feedback=None,
                           feedback_class=None, attempts=0,
                           score=current_score, audio_filename=audio_filename, audio_filename2 =audio_filename2,
                           current_question_number=current_question_number,  # Update accordingly
                           total_questions=len(quiz_questions))



@app.route('/audio/<path:filename>')
def download_file(filename):
    return send_from_directory('path/to/audio/directory', filename)


@app.route('/score/<int:score>')
def score(score):
    global current_score 
    current_score = 0
    return render_template('score.html', score=score)

@app.route('/reset_score')
def reset_score():
    global current_score
    current_score = 0
    return "Score has been reset"


if __name__ == '__main__':
    app.run(debug=True)
