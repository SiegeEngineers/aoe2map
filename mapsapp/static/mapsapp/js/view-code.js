$(function () {
    hljs.registerLanguage('rmslanguage', rmslanguage);
    $('#viewCodeButton').click(function () {
        let url = $('#downloadButton').attr('href');
        $.get(url, function (data) {
            console.log(data);
            showRmsCode(data);
        }).fail(function () {
            alert("Oops! Could not download rms script.");
        });
    });
});

function showRmsCode(content) {
    let codearea = document.querySelector('#codearea');
    codearea.textContent = content;
    hljs.highlightBlock(codearea);
    hljs.lineNumbersBlock(codearea, {singleLine: true});
    $('#showCodeModal').modal('show');
}