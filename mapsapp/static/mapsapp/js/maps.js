var mapnames = new Bloodhound({
    datumTokenizer: function (n) {
        return n.name.split(/,/)
    },
    queryTokenizer: function (n) {
        return n.split(/,/)
    },
    prefetch: {
        url: MAPS_PREFETCH_URL,
        filter: function (list) {
            return $.map(list.maps, function (map) {
                return {name: map.name, uuid: map.uuid};
            });
        }
    },
    remote: {
        url: MAPS_URL,
        wildcard: 'QUERY',
        filter: function (list) {
            return $.map(list.maps, function (map) {
                return {name: map.name, uuid: map.uuid};
            });
        }
    }
});
mapnames.initialize();
$('#id_rms').tagsinput({
    itemValue: function (item) {
        return item.uuid;
    },
    itemText: function (item) {
        return item.name;
    },
    typeaheadjs: {
        name: 'mapnames',
        displayKey: 'name',
        source: mapnames.ttAdapter()
    }
});
let prefilledUuidString = $('#id_rms').val();
let prefilledUuids = prefilledUuidString.split(',');
let promises = [];
let prefillData = [];
prefilledUuids.forEach(function (uuid) {
    promises.push(
        (function () {
            return $.getJSON(
                UUID_TO_MAP_NAME_URL.replace('00000000-0000-0000-0000-000000000000', uuid),
                function (data) {
                    data.uuid = uuid;
                    prefillData.push(data);
                }
            );
        })()
    );
});
$.when.apply($, promises).done(function () {
    $('#id_rms').val('');
    prefillData.sort(function (a, b) {
        return (a.name + ' by ' + a.authors) > (b.name + ' by ' + b.authors);
    });
    for (let item of prefillData) {
        $('#id_rms').tagsinput('add', {'uuid': item.uuid, 'name': item.name + ' by ' + item.authors});
    }
}).fail(function () {
    alert('Whoops! Something went wrong. Please check whether your maps at the bottom are still all there.');
});
