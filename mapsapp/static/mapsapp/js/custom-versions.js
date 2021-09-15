$(function () {initCustomVersions();});
function initCustomVersions() {
    $('.x256TechButton').unbind().click(function (event) {
        let url = $(event.target).closest('.btn-group').find('.map-download').attr('href');
        let mapName = $(event.target).closest('.map-info').find('.card-title a').text();
        let filename = getFilename(url);
        $.ajax({
            url: url,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=x-user-defined");
            }
        }).done(function (data) {
            if (data.startsWith('PK\x03\x04')) {
                const items = filename.split('@', 2);
                filename = items.length === 2 ? 'ZR@256x_' + items[1] : 'ZR@256x_' + items[0];
                downloadPatchedZipFile(data, filename, mapName, patchWith256xTech);
            } else {
                downloadPatchedRmsFile(data, '256x_' + filename, mapName, patchWith256xTech);
            }
        }).fail(function () {
            alert("Oops! Could not download rms script.");
        });
    });

    $('.explodingVillagersButton').unbind().click(function (event) {
        let url = $(event.target).closest('.btn-group').find('.map-download').attr('href');
        let mapName = $(event.target).closest('.map-info').find('.card-title a').text();
        let filename = getFilename(url);
        $.ajax({
            url: url,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=x-user-defined");
            }
        }).done(function (data) {
            if (data.startsWith('PK\x03\x04')) {
                const items = filename.split('@', 2);
                filename = items.length === 2 ? 'ZR@EV_' + items[1] : 'ZR@EV_' + items[0];
                downloadPatchedZipFile(data, filename, mapName, patchWithExplodingVillagers);
            } else {
                downloadPatchedRmsFile(data, 'EV_' + filename, mapName, patchWithExplodingVillagers);
            }
        }).fail(function () {
            alert("Oops! Could not download rms script.");
        });
    });

    $('.suddenDeathButton').unbind().click(function (event) {
        let url = $(event.target).closest('.btn-group').find('.map-download').attr('href');
        let mapName = $(event.target).closest('.map-info').find('.card-title a').text();
        let filename = getFilename(url);
        $.ajax({
            url: url,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=x-user-defined");
            }
        }).done(function (data) {
            if (data.startsWith('PK\x03\x04')) {
                const items = filename.split('@', 2);
                filename = items.length === 2 ? 'ZR@SD_' + items[1] : 'ZR@SD_' + items[0];
                downloadPatchedZipFile(data, filename, mapName, patchWithSuddenDeath);
            } else {
                downloadPatchedRmsFile(data, 'SD_' + filename, mapName, patchWithSuddenDeath);
            }
        }).fail(function () {
            alert("Oops! Could not download rms script.");
        });
    });
}

function getFilename(url) {
    const items = url.split('/');
    return decodeURI(items[items.length - 1]).replace('%40', '@');
}

function patchWith256xTech(content, mapName) {
    content = content.replace(/<PLAYER_SETUP>/g, `/* 256x tech patch */
#includeXS x256tech.xs
/* 256x tech patch end */
 
<PLAYER_SETUP>`);
    content = '/* 256x tech ' + mapName + ' */\n' +
        '/* auto-generated on aoe2map.net */\n\n' + content;
    return content;
}

function patchWithSuddenDeath(content, mapName) {
    if (content.includes('guard_state')) {
        alert('This map already contains a guard_state command.\nSorry, we can\'t patch it automatically.');
        return null;
    }
    content = content.replace(/<PLAYER_SETUP>/g, `/* Sudden Death patch part 1 of 2 start */
#const TOWN_CENTER 109
#const RI_TOWN_CENTER 187 
/* Sudden Death patch part 1 of 2 end */
 
<PLAYER_SETUP>
/* Sudden Death patch part 2 of 2 start */
guard_state TOWN_CENTER AMOUNT_GOLD 0 1
effect_amount ENABLE_TECH RI_TOWN_CENTER ATTR_DISABLE 187
/* Sudden Death patch part 2 of 2 end */\n`);
    content = '/* Sudden Death ' + mapName + ' */\n' +
        '/* auto-generated on aoe2map.net */\n\n' + content;
    return content;
}

function patchWithExplodingVillagers(content, mapName) {
    content = content.replace(/<PLAYER_SETUP>/g, `<PLAYER_SETUP>
/* Exploding villagers patch start */
effect_amount SET_ATTRIBUTE VILLAGER_CLASS ATTR_DEAD_ID 706
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_HITPOINTS 0
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_ATTACK 50
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_ATTACK 346
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_ATTACK 512
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_MAX_RANGE 2
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_BLAST_LEVEL 1
/* Exploding villagers patch end */\n`);
    content = '/* Exploding Villagers ' + mapName + ' */\n' +
        '/* auto-generated on aoe2map.net */\n\n' + content;
    return content;
}

function getMapName(){
    return $('.card-title a').text();
}

function downloadPatchedRmsFile(content, filename, mapName, patch) {
    content = patch(content, mapName);
    if (content === null) {
        return;
    }
    const blob = new Blob([content], {type: "text/plain;charset=utf-8"});
    saveAs(blob, filename);
}

function downloadPatchedZipFile(data, zipFilename, mapName, patch) {
    JSZip.loadAsync(data).then(function (d) {
        for (let filename in d.files) {
            if (d.files.hasOwnProperty(filename)) {
                if (filename.endsWith('.rms')) {
                    let currentRmsFileName = filename;
                    d.file(filename).async('text').then(function (content) {
                        content = patch(content, mapName);
                        if (content === null) {
                            return;
                        }
                        d.file(filename, content);
                        d.generateAsync({type: "blob"}).then(function (blob) {
                            saveAs(blob, zipFilename);
                        });
                    });
                    return;
                }
            }
        }
        alert("No .rms file found inside the archive!");
    });
}