$(document).ready(function() {
    $('.option-button').click(function() {
        $('.option-button').removeClass('active');
        $(this).addClass('active');
        $('#selectedAnswer').val($(this).text().trim());
        $('#submit-answer').prop('disabled', false);
    });

});