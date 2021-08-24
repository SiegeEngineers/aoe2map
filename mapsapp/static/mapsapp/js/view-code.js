function initViewCode() {
    hljs.registerLanguage('rmslanguage', rmslanguage);
    $('.viewCodeButton').unbind().click(function (event) {
        let url = $(event.target).closest('.btn-group').find('.map-download').attr('href');
        $.ajax({
            url: url,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=x-user-defined");
            }
        }).done(function (data) {
            if (data.startsWith('PK\x03\x04')) {
                extractAndShowRmsFromZr(data);
            } else {
                showRmsCode(data);
            }
        }).fail(function () {
            alert("Oops! Could not download rms script.");
        });
    });
}
$(function (){initViewCode()});

function showRmsCode(content) {
    let codearea = document.querySelector('#codearea');
    codearea.textContent = content;
    hljs.highlightBlock(codearea);
    hljs.lineNumbersBlock(codearea, {singleLine: true});
    $('#showCodeModal').modal('show');
}

function extractAndShowRmsFromZr(data) {
    JSZip.loadAsync(data).then(function (d) {
        for (let filename in d.files) {
            if (d.files.hasOwnProperty(filename)) {
                if (filename.endsWith('.rms')) {
                    currentRmsFileName = filename;
                    d.file(filename).async('text').then(function (content) {
                        showRmsCode(content);
                    });
                    return;
                }
            }
        }
        alert("No .rms file found inside the archive!");
    });
}