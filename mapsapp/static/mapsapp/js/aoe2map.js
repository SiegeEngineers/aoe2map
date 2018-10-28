function partition(array, chunksize) {
    let i, j, nr, temparray;
    let retval = [];
    for (nr = 0, i = 0, j = array.length; i < j; i += chunksize) {
        temparray = array.slice(i, i + chunksize);
        retval.push({number: nr, data: temparray});
        nr++;
    }
    return retval;
}

function toggleMaxHeight(self){
    $(self).toggleClass('full');
}

$(function () {

    $.getJSON(API_URL, function (data) {
        addAllMaps(data);
    });

    function addAllMaps(data) {
        $('.maps').empty();
        if (data.maps.length === 0) {
            $('<div class="col-12 text-center">No result :-(</div>').appendTo('.maps');
        }
        for (let part of partition(data.maps, 10)) {
            setTimeout(function () {
                for (let map of part.data) {
                    if (map.images.length === 0) {
                        map.images.push({"url": "/static/mapsapp/images/empty.png"});
                    }
                    let alert = '';
                    if (map.newer_version !== null) {
                        alert = '<div class="alert alert-info" role="alert">\
                      A newer version of this map is available! \
                    <a href="' + map.newer_version + '" class="alert-link">Check it out!</a>\
                    </div>'
                    }
                    let url = '';
                    if (map.url) {
                        url = '<a href="' + map.url + '" class="card-link btn btn-outline-secondary" target="_blank">Website</a>';
                    }

                    let imageUrl = map.images[0].url;
                    if (map.images[0].preview_url !== null) {
                        imageUrl = map.images[0].preview_url;
                    }
                    $('<div class="col-lg-4 col-md-6 col-12"> \
                <div class="card"> \
                    <a href="' + map.pageurl + '">\
                        <img class="card-img-top rounded" src="' + imageUrl + '" />\
                    </a>\
                        <div class="card-body">\
                            ' + alert + '\
                            <h5 class="card-title"><a href="' + map.pageurl + '">' + map.name + '</a><small class="text-muted"> ' + map.version + '</small></h5>\
                            <h6 class="card-subtitle mb-2 text-muted">by ' + map.authors + '</h6>\
                            <p class="card-text font-italic map-description" onclick="toggleMaxHeight(this)">' + map.description + '</p>\
                            <p>\
                                <a href="' + map.fileurl + '" class="card-link btn btn-secondary map-download">Download map</a>\
                                ' + url + '\
                            </p>\
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
            }, part.number * 100);
        }
    }

    function getTags(tags) {
        let retval = "";
        for (tag of tags) {
            retval += '<a href="/tags/' + tag.id + '" class="badge badge-secondary">' + tag.name + '</a> ';
        }
        return retval;
    }

    function getVersiontags(tags) {
        let retval = "";
        for (tag of tags) {
            retval += '<a href="/version/' + tag + '" class="badge badge-secondary">' + tag + '</a> ';
        }
        return retval;
    }

});