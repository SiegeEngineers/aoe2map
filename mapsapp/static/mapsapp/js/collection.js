function normalizeName(name) {
    name = name.replace(/%40/g, "@");
    return name.replace(/[^@A-Za-z0-9\-_ ()\[\].+]/g, "_");
}

let collectionDownloadFunction = (folderPrefix, includeMetadataFile) => function () {
    let zip = new JSZip();
    let promises = [];
    let mapUrls = $('.map-download');
    let collectionName = $('#collection-name').text() || $('#map-name').text();
    let authorNames = $('#author-names').text();
    let description = $('#description').text();
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
                return fetch(url)
                    .then(response => response.arrayBuffer())
                    .then(buffer => {
                        zip.file(folderPrefix + name, buffer);
                    })
                    .catch(err => console.error(err));
            })()
        );
    }
    if (includeMetadataFile) {
        zip.file('info.json', JSON.stringify({Author: authorNames, Description: description, Title: collectionName}));
    }

    $.when.apply($, promises).done(function () {
        zip.generateAsync({type: "blob"})
            .then(function (content) {
                saveAs(content, normalizeName(collectionName + ".zip"));
            });
    }).fail(function () {
        alert('Download failed due to technical reasons. Sorry!');
    });
};

$('#download').click(collectionDownloadFunction('', false));
$('#deModButton').click(collectionDownloadFunction('resources/_common/random-map-scripts/', true));
$('#wkVooblyModButton').click(collectionDownloadFunction('Voobly Mods/AOC/Data Mods/WololoKingdoms/Script.Rm/', false));

$('.roll-random-item').click(function () {
    $('#modal-scouting').slideDown(500);
    $('#modal-result').slideUp(500);
    $('#random_choice_modal .modal-footer').hide();

    $('#random_choice_modal').modal();

    setTimeout(() => {
        const maps = $('.maps .card');
        const index = Math.floor(Math.random() * maps.length);
        $('#modal-result .image').empty();
        $('#modal-result .description').empty();
        $($(maps[index]).find('a').get(0)).clone().appendTo('#modal-result .image');
        $(maps[index]).find('.card-body').clone().appendTo('#modal-result .description');

        $('#modal-scouting').slideUp(500);
        $('#modal-result').slideDown(500);
        $('#random_choice_modal .modal-footer').slideDown(500);
    }, 3000);
});