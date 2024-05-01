$(document).ready(function() {
    var lastClickedButton = null;
    
    $('.option-button').click(function() {
        $('.option-button').removeClass('active');
        $(this).addClass('active');
        $('#selectedAnswer').val($(this).text().trim());
        $('#submit-answer').prop('disabled', false);
        lastClickedButton = $(this);
    });

    $('.nav-link').click(function() {
        // Call the reset score endpoint
        $.ajax({
            url: '/reset_score',
            type: 'GET',  // Change to GET as your endpoint is designed to handle GET requests
            success: function(response) {
                console.log("Score reset successful.");
            },
            error: function() {
                console.error("Failed to reset score.");
            }
        });
    });

    $('#submit-answer').click(function(){
        let selectedOption = $('#selectedAnswer').val();
        let attempts = parseInt($('input[name="attempts"]').val()) || 0;
        let score = parseInt($('input[name="score"]').val()) || 0;
        let quizId = $('#quiz-id').data('quiz-id');
        let url = $(this).data('url');
        console.log("Data:", { option: selectedOption, quiz_id: quizId, score: score, attempts: attempts });
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                option: selectedOption,
                quiz_id: quizId,
                score: score,
                attempts: attempts
            }),
            dataType: 'json',
            success: function(response) {
                console.log("Received response:", response);
                
                $('#feedback-container').remove();

                var feedbackContainer = $('<div>', {
                    id: 'feedback-container',
                    class: 'feedback-style mx-auto mt-2 ' + response.feedback_class,
                    text: response.feedback
                });
            
                $('.feedbackbox').prepend(feedbackContainer);
                $('#feedback-container').fadeIn();

                $('input[name="attempts"]').val(response.attempts);
                console.log("Updated attempts in hidden input:", $('input[name="attempts"]').val());
                if (response.feedback === 'Correct!') {
                    $('input[name="score"]').val(response.score);
                    $('#next-question').prop('disabled', false);
                    $('#score-and-question').html('Question ' + response.current_question_number + ' of ' + response.total_questions + ' Score: ' + response.score);
                    $('.option-button').prop('disabled', true);
                }
                if (response.attempts >= 2) {
                    $('#next-question').prop('disabled', false);
                    $('.option-button').prop('disabled', true);

                    $('.option-button').each(function() {
                        if ($(this).text().trim() === response.correctAnswer) {
                            $(this).addClass('correct-feedback')
                        }
                    });

                }
                $('#submit-answer').prop('disabled', true);
                lastClickedButton.prop('disabled', true); 
                lastClickedButton.addClass(response.feedback_class);
            },
            error: function(xhr, status, error) {
                console.error('Error occurred:', error);
            }
        });
    
    });


    $('#next-question').click(function() {
        let currentQuizId = $('#quiz-id').data('quiz-id');
        
        if(currentQuizId == '6'){
            $.ajax({
                url: '/reset_score',
                type: 'GET',
                success: function(response) {
                }
            });
            let score = parseInt($('input[name="score"]').val()) || 0;
            let baseUrl = window.location.origin;
            let nextUrl = `${baseUrl}/score/${score}`;
            window.location.href = nextUrl;
        }
        else{
            let nextQuizId = currentQuizId + 1;
            let baseUrl = window.location.origin;
            let nextUrl = `${baseUrl}/quiz/${nextQuizId}`;
            window.location.href = nextUrl;
        }
    
    });
});