var tagnames = new Bloodhound({
    datumTokenizer: function (n) {
        return n.name.split(/,/)
    },
    queryTokenizer: function (n) {
        return n.split(/,/)
    },
    prefetch: {
        url: ALLTAGS_PREFETCH_URL,
        filter: function (list) {
            return $.map(list.tags, function (tagname) {
                return {name: tagname};
            });
        }
    }
});
tagnames.initialize();
$('#id_tags').tagsinput({
    "maxTags": 8,
    typeaheadjs: {
        name: 'tagnames',
        displayKey: 'name',
        valueKey: 'name',
        source: tagnames.ttAdapter()
    }
});