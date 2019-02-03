const activeClass = 'btn-outline-primary';
const inactiveClass = 'btn-secondary';

function update_votes(votes, self_voted) {
    let votesButton = $('#vote-button');
    votesButton.find('.votes').text(votes);
    if (self_voted) {
        votesButton.removeClass(inactiveClass);
        votesButton.addClass(activeClass);
    } else {
        votesButton.addClass(inactiveClass);
        votesButton.removeClass(activeClass);
    }
}

$(function(){
    $('#vote-button').click(function(){
        if ($(this).hasClass(activeClass)) {
            $.post(REMOVE_VOTE_URL, function (data) {
                update_votes(data.votes, data.self_voted);
            });
        } else {
            $.post(ADD_VOTE_URL, function (data) {
                update_votes(data.votes, data.self_voted);
            });
        }
    });
});
