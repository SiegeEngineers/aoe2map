function addToCollection(rmsId, collectionId) {
    $.post(COLLECTION_ENDPOINT, {"rms_id": rmsId, "collection_id": collectionId, "action": "add"}, function (response) {
        $('#alert-area').append("<div class='alert alert-" + response.class + " alert-dismissible' role='alert'>\n" +
            response.message +
            "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>\n" +
            "<span aria-hidden='true'>&times;</span>\n" +
            "</button>" +
            "</div>");
    }, 'json');
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", $("[name=csrfmiddlewaretoken]").val());
        }
    }
});