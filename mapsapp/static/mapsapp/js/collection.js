function normalizeName(name) {
    name =  name.replace(/%40/g, "@");
    return name.replace(/[^@A-Za-z0-9\-_ ()\[\].+]/g, "_");
}

$('#download').click(function () {
    let zip = new JSZip();
    let promises = [];
    let mapUrls = $('.map-download');
    let collectionName = $('#collection-name').text();
    let i = 0;
    let names = new Set();
    for (let mapUrl of mapUrls) {
        i++;
        let filename = normalizeName(decodeURI(mapUrl.href.substring(mapUrl.href.lastIndexOf('/') + 1)));
        if (names.has(filename)) {
            filename = normalizeName(i.toString(10) + "-" + filename);
        }
        names.add(filename);

        promises.push(
            (function () {
                let url = mapUrl.href;
                let name = filename;
                return $.get(url, function (data) {
                    zip.file(name, data);
                });
            })()
        );
    }

    $.when.apply($, promises).done(function () {
        zip.generateAsync({type: "blob"})
            .then(function (content) {
                saveAs(content, normalizeName(collectionName + ".zip"));
            });
    }).fail(function () {
        alert('Download failed due to technical reasons. Sorry!');
    });


});