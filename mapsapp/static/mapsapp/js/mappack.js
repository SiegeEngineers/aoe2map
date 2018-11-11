window.addEventListener("dragover", function (e) {
    e = e || event;
    e.preventDefault();
}, false);
window.addEventListener("drop", function (e) {
    e = e || event;
    e.preventDefault();
}, false);

function dropHandler(ev) {
    ev.preventDefault();
    for (var i = 0; i < ev.dataTransfer.files.length; i++) {
        let file = ev.dataTransfer.files[i];
        handleRmsFile(file);
    }
    removeDragData(ev)
}

function handleFiles(filelist) {
    for (let file of filelist) {
        handleRmsFile(file);
    }
}

function recalculatePercentages() {
    let percentages = $('.percentage');
    let chances = getChances(percentages.length);
    for (let i = 0; i < percentages.length; i++) {
        $(percentages[i]).val(chances[i]);
    }
}

function handleRmsFile(file) {
    if (file.name.endsWith(".rms")) {
        let reader = new FileReader();
        reader.onload = function (e) {
            let contents = e.target.result;
            let warnings = [];
            if (contents.startsWith('PK\x03\x04')) {
                $('<li class="list-group-item">\
                        <h5 class="mapname">' + file.name + '</h5>\
                        <p class="text-danger">Unfortunately, you cannot add ZR maps to a map pack.</p>\
                    </li>').appendTo('#filelist');
            } else {
                restructureMap(contents, "", [], warnings);
                console.log(warnings);
                let clazz = 'success';
                let text = 'Looks good!';
                if (warnings.length > 0) {
                    clazz = 'warning';
                    text = "This map might not be suitable for usage in a map pack and break the map pack you are about to create. Problems: \
                        <ul><li>" + warnings.join("</li>\n<li>") + "</li></ul>";
                }
                $('<li class="list-group-item map">\
                        <div class="row">\
                        <div class="col-9">\
                            <h5 class="mapname">' + file.name + '</h5>\
                            <p class="text-' + clazz + '">' + text + '</p>\
                        </div>\
                        <div class="col-3">\
                        <label>Probability</label>\
                            <div class="input-group mb-3">\
                                <input type="number" class="form-control percentage">\
                                <div class="input-group-append">\
                                    <span class="input-group-text">%</span>\
                                </div>\
                            </div>\
                        </div>\
                        </div>\
                    </li>').appendTo('#filelist').data('map', contents);
            }
            recalculatePercentages();
        };
        reader.readAsText(file);
    } else {
        $('#filelist').append('<li class="list-group-item">' + file.name + " is not a .rms file</li>");
    }
}

function getdata() {
    let allButtons = $('.map');
    let startData = 'start_random\n';
    let percentage_sum = 0;
    for (let i = 0; i < allButtons.length; i++) {
        let prefix = "M" + i + "_";
        let mapname = $(allButtons.get(i)).find('.mapname').text();
        let percentage = parseInt($(allButtons.get(i)).find('.percentage').val());
        if (!isNaN(percentage)) {
            percentage_sum += percentage;
        } else {
            alert("Error: Percentage for map '" + mapname + "' is not a number");
            return;
        }
        startData += "percent_chance " + percentage + " #define " + marker(prefix, mapname) + "\n"
    }
    startData += 'end_random\n';

    if (percentage_sum !== 100) {
        alert("Error: Sum of all percentages should be 100, but is " + percentage_sum);
        return;
    }


    let constLines = [];

    let mapsData = "";

    allButtons.each(function (i, it) {
        let ifVariant = "elseif";
        if (i === 0) {
            ifVariant = "if";
        }
        let prefix = "M" + i + "_";
        mapsData += "\n\n" + ifVariant + " " + marker(prefix, $(it).find('.mapname').text()) + "\n\n" + restructureMap($(it).data('map'), prefix, constLines, []);
    });
    mapsData += "\n\nendif";

    let wholeData = startData + "\n" + constLines.join("\n") + "\n" + mapsData;

    download("mappack.rms", wholeData);
}

function getChances(amount) {
    let a = [];
    let sum = 0;
    for (let i = 0; i < amount; i++) {
        let percentage = Math.floor(100 / amount);
        a.push(percentage);
        sum += percentage;
    }
    for (let i = 0; i < 100 - sum; i++) {
        a[i]++;
    }
    return a;
}

function marker(prefix, name) {
    let m = prefix + normalizeConstant(name);
    return m;
}

function normalizeConstant(name) {
    name = name.substr(0, name.length - 4);
    name = name.toUpperCase();
    name = name.replace(/\s+/g, "_");
    name = name.replace(/[^A-Z0-9_]/g, "X");
    return name;
}

function normalizeMap(mapcontent, prefix) {
    mapcontent = mapcontent.replace(/#include_drs\s+random_map.def/g, "#include_drsrandom_mapdef");
    let commentMatches = mapcontent.match(/\n?\/\*.*?\*\//g);
    if (commentMatches !== null) {
        for (let i = 0; i < commentMatches.length; i++) {
            mapcontent = mapcontent.replace(commentMatches[i], `§comment§${i}§`);
        }
    }
    mapcontent = mapcontent.replace(/\r?\n/g, " ");
    mapcontent = mapcontent.replace(/\s+/g, " ");
    mapcontent = mapcontent.replace(/\s([a-z_]+)/g, "\n$1");
    mapcontent = mapcontent.replace(/#/g, "\n#");
    mapcontent = mapcontent.replace(/\{/g, "\n{");
    mapcontent = mapcontent.replace(/\}/g, "\n}\n");
    if (commentMatches !== null) {
        for (let i = 0; i < commentMatches.length; i++) {
            mapcontent = mapcontent.replace(`§comment§${i}§`, commentMatches[i]);
        }
    }
    mapcontent = mapcontent.replace(/\s+\*\//g, " */");
    mapcontent = mapcontent.replace(/ \n/g, "\n");
    mapcontent = mapcontent.replace(/#include_drsrandom_mapdef/g, "#include_drs random_map.def");
    mapcontent = mapcontent.replace(/\s+\n/g, "\n");
    mapcontent = mapcontent.replace(/</g, "\n\n<");
    mapcontent = mapcontent.replace(/\n\/\*/g, "\n\n/*");
    mapcontent = mapcontent.replace(/\*\/\n\s*\n\/\*/g, "*/\n/*");
    mapcontent = mapcontent.replace(/^\n+/g, "");
    return mapcontent;
}

function collectDeclaredConsts(lines) {
    let consts = new Map();
    for (let line of lines) {
        let matchArray = line.match(/#const ([A-Z_][A-Z0-9_]*)/);
        if (matchArray != null) {
            let key = matchArray[1];
            if (!consts.has(key)) {
                consts.set(key, []);
            }
            consts.get(key).push(line);
        }
    }
    return consts;
}

function restructureMap(mapcontent, prefix, constLines, warnings) {
    mapcontent = normalizeMap(mapcontent, prefix);

    let lines = mapcontent.split("\n");

    let declaredConsts = collectDeclaredConsts(lines);

    for (let key of declaredConsts.keys()) {
        let values = declaredConsts.get(key);
        if (values.length > 1) {
            let expected = values[0];
            for (let value of values) {
                if (value !== expected) {
                    warnings.push("constant " + key + " is declared twice: '" + value + "' vs. '" + expected + "'");
                }
            }
        }
    }


    let mapLines = [];
    let indent = 0;
    let lineNr = 0;
    let lineInError = 0;
    let latestIndent = 0;
    for (let line of lines) {
        lineNr++;
        line = addPrefixesToConsts(line, prefix, declaredConsts);
        if (line.startsWith("#const")) {
            constLines.push(line);
        } else {
            let indentBefore = getIndentBefore(line);
            let indentAfter = getIndentAfter(line);
            if (lineInError < 1 && indent + indentBefore < 0) {
                lineInError = lineNr;
            }
            mapLines.push(getIndent(indent + indentBefore) + line);
            indent += indentAfter;
            latestIndent = indent;
        }
    }
    if (lineInError < 1 && latestIndent !== 0) {
        lineInError = lineNr;
    }

    if (lineInError > 0) {
        warnings.push("The indentation revealed issues with your brackets or if/else statements.");
    }

    return mapLines.join("\n");
}

function addPrefixesToConsts(line, prefix, declaredConsts) {
    for (let key of declaredConsts.keys()) {
        if (line.includes(key)) {
            let re = new RegExp("(\\s)" + key + "(\\s|{|$)", "g");
            line = line.replace(re, "$1" + prefix + key + "$2");
        }
    }
    return line;
}

function addWarning(message) {
    console.log(message);
}

function getIndentBefore(line) {
    if (line.startsWith("elseif")) {
        return -1;
    }
    if (line.startsWith("else")) {
        return -1;
    }
    if (line.startsWith("endif")) {
        return -1;
    }
    if (line.startsWith("end_random")) {
        return -1;
    }
    if (line.startsWith("}")) {
        return -1;
    }
    return 0;
}

function getIndentAfter(line) {
    if (line.startsWith("if")) {
        return 1;
    }
    if (line.startsWith("endif")) {
        return -1;
    }
    if (line.startsWith("{")) {
        return 1;
    }
    if (line.startsWith("}")) {
        return -1;
    }
    if (line.startsWith("start_random")) {
        return 1;
    }
    if (line.startsWith("end_random")) {
        return -1;
    }
    return 0;
}

function getIndent(i) {
    //if (i < 0) { return "XXXXXX"; }
    return " ".repeat(Math.max(i * 4, 0));
}

function dragOverHandler(event) {
    $('#target').addClass('active');
}

function dragLeaveHandler(event) {
    $('#target').removeClass('active');
}

function removeDragData(ev) {
    if (ev.dataTransfer.items) {
        // Use DataTransferItemList interface to remove the drag data
        ev.dataTransfer.items.clear();
    } else {
        // Use DataTransfer interface to remove the drag data
        ev.dataTransfer.clearData();
    }
    dragLeaveHandler(ev);
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

function clearList() {
    $('#filelist').empty();
}