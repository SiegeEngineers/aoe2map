$(function () {

    $.getJSON(API_URL, function (data) {
        addAllMaps(data);
    });

    function addAllMaps(data) {
        if (data.maps.length === 0) {
            $('<div class="col-12 text-center">No result :-(</div>').appendTo('.maps');
        }
        for (let map of data.maps) {
            if (map.images.length === 0) {
                map.images.push({"url": "/static/mapsapp/images/empty.png"});
            }
            $('<div class="col-lg-4 col-md-6 col-12"> \
            <div class="card"> \
                <img class="card-img-top mapscreenshot rounded" src="' + map.images[0].url + '" />\
                    <div class="card-body">\
                            <h5 class="card-title">' + map.name + '<small class="text-muted"> ' + map.version + '</small></h5>\
                            <h6 class="card-subtitle mb-2 text-muted">by ' + map.authors + '</h6>\
                            <p class="card-text">' + map.description + '</p>\
                            <a href="' + map.fileurl + '" class="card-link">Download map</a>\
                            <a href="' + map.url + '" class="card-link" target="_blank">Website</a>\
                            <div class="tags">Tags: \
                            ' + getTags(map.tags) + '\
                            </div>\
                            <div class="tags">Versions: \
                            ' + getVersiontags(map.versiontags) + '\
                            </div>\
                        </div>\
                    </div>\
            </div>').appendTo('.maps');
        }
    }

    function getTags(tags) {
        let retval = "";
        for (tag of tags) {
            retval += '<a href="/tags/' + tag.id + '"><span class="badge badge-secondary">' + tag.name + '</span></a> ';
        }
        return retval;
    }

    function getVersiontags(tags) {
        let retval = "";
        for (tag of tags) {
            retval += '<a href="/version/' + tag + '"><span class="badge badge-secondary">' + tag + '</span></a> ';
        }
        return retval;
    }

});