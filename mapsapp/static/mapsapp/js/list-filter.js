function applyFilter() {
    let input, filter, lists, list, li, a, i;
    input = document.getElementById('filterInput');
    filter = input.value.toLowerCase();
    lists = document.querySelectorAll(".maplist,.mapslist");
    for (list of lists) {
        li = list.getElementsByTagName('li');

        for (i = 0; i < li.length; i++) {
            a = li[i].getElementsByTagName("a")[0];
            if (a.innerHTML.toLowerCase().indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }
}

document.getElementById('filterInput').addEventListener('keyup', function () {
    applyFilter();
});

applyFilter();
