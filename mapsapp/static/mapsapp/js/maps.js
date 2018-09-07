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

$('#id_rms').val('');
for (let item of RMS_INITIAL_DATA) {
    $('#id_rms').tagsinput('add', {'uuid': item.uuid, 'name': item.name + ' by ' + item.authors});
}
