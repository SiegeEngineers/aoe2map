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

function toggleMaxHeight(self) {
    $(self).toggleClass('full');
}

function addAllMaps(data, selector = '.maps') {
    $(selector).empty();
    if (data.maps.length === 0) {
        $('<div class="col-12 text-center">No result :-(</div>').appendTo(selector);
    }
    let partitions = partition(data.maps, 10);
    for (let part of partitions) {
        setTimeout(function () {
            for (let map of part.data) {
                if (map.images.length === 0) {
                    if (map.versiontags.includes("DE")) {
                        const number = Math.floor(Math.random() * 2);
                        map.images.push({
                            "url": `/static/mapsapp/images/empty-de-${number}.png`,
                            "preview_url": null
                        });
                    } else {
                        map.images.push({"url": "/static/mapsapp/images/empty.png", "preview_url": null});
                    }
                }
                let alert = '';
                if (map.newer_version !== null) {
                    alert = '<div class="alert alert-info" role="alert">\
                      A newer version of this map is available! \
                    <a href="' + map.latest_version + '" class="alert-link">Check it out!</a>\
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
                <div class="card map-info"> \
                    <a href="' + map.pageurl + '">\
                        <img class="card-img-top rounded" src="' + imageUrl + '" />\
                    </a>\
                        <div class="card-body">\
                            ' + alert + '\
                            <h5 class="card-title"><a href="' + map.pageurl + '">' + map.name + '</a><small class="text-muted"> ' + map.version + '</small></h5>\
                            <h6 class="card-subtitle mb-2 text-muted">by ' + map.authors + '</h6>\
                            <p class="card-text font-italic map-description" onclick="toggleMaxHeight(this)">' + map.description + '</p>\
                            <p>\
                                <div class="btn-group mr-3">\
                            <a href="' + map.fileurl + '" class="card-link btn btn-secondary map-download">Download map</a>\
                            <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split"\
                                    data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">\
                                <span class="sr-only">Toggle Dropdown</span>\
                            </button>\
                            <div class="dropdown-menu">\
                                <button class="dropdown-item viewCodeButton">View rms code</button>\
                                <button class="dropdown-item x256TechButton">\
                                    256x tech version (DE)\
                                </button>\
                                <button class="dropdown-item suddenDeathButton">\
                                    Sudden Death version (UP)\
                                </button>\
                                <button class="dropdown-item explodingVillagersButton">\
                                    Exploding Villagers version (UP)\
                                </button>\
                            </div>\
                        </div>\
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
            </div>').appendTo(selector);
            }
        }, part.number * 100);
    }
    setTimeout(()=>{initViewCode(); initCustomVersions();}, partitions.length * 100);
}

function getTags(tags) {
    let retval = "";
    for (let tag of tags) {
        retval += '<a href="/tags/' + tag.id + '" class="badge badge-secondary">' + tag.name + '</a> ';
    }
    return retval;
}

function getVersiontags(tags) {
    let retval = "";
    for (let tag of tags) {
        retval += '<a href="/version/' + tag + '" class="badge badge-secondary">' + tag + '</a> ';
    }
    return retval;
}

$(function () {
    if (API_URL !== '') {
        $.getJSON(API_URL, function (data) {
            addAllMaps(data);
        });
    }
    if (LATEST_MAPS_URL !== '') {
        $.getJSON(LATEST_MAPS_URL, function (data) {
            addAllMaps(data, '.latestmaps');
        });
    }
    if (LATEST_UPDATED_MAPS_URL !== '') {
        $.getJSON(LATEST_UPDATED_MAPS_URL, function (data) {
            addAllMaps(data, '.latestupdatedmaps');
        });
    }
});