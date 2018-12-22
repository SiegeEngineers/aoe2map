$(function(){
    $('.vote').click(function(){
        $(this).removeClass('btn-secondary');
        $(this).addClass('btn-outline-primary');
        let votes = $(this).find('.votes');
        votes.text(parseInt(votes.text()) + 1);
    });
});