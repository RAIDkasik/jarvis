$(document).ready(function() {
    $('.links').click(function(event) {
        $.get('main.html', function(data) {
            $('body').html(data);
            $('.a_links').html("НАСТРОЙКИ");
        });
    });
});