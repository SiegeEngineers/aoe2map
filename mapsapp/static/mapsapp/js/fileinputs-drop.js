let target = document.documentElement;
let body = document.body;
let fileInput = document.querySelector('#id_file');
let imageInput = document.querySelector('#id_images');

window.addEventListener('dragover', (e) => {
    e.preventDefault();
    body.classList.add('dragging');
});
window.addEventListener('dragleave', (e) => {
    if (e.pageX !== 0 && e.pageY !== 0) {
        return false;
    }
    body.classList.remove('dragging');
});

$('#drop-info').click(function(){
    body.classList.remove('dragging');
});

target.addEventListener('drop', (e) => {
    e.preventDefault();
    body.classList.remove('dragging');

    if (e.dataTransfer.files.length > 0) {
        let firstFile = e.dataTransfer.files[0];
        if (ACCEPT_DROP.includes('image') && hasImageExtension(firstFile.name)) {
            addImageFiles(e.dataTransfer.files);
        }
        if (ACCEPT_DROP.includes('rms') && hasRmsExtension(firstFile.name)) {
            addRmsFile(e.dataTransfer.files);
        }
    } else {
        console.log("no files found for drop event");
    }
});

function addImageFiles(files) {
    for (let i = 0; i < files.length; i++) {
        if (!hasImageExtension(files[i].name)) {
            showAlert("warning", "Please drop only one single rms file or only images file(s) at a time!");
            return;
        }
    }
    let warning = " ";
    if (imageInput.files.length > 0) {
        warning += "<strong>" + imageInput.files.length + " Previously added images have been removed</strong>!";
    }
    imageInput.files = files;
    showAlert("info", files.length + " dropped images have been put into this form." + warning);

}

function addRmsFile(files) {
    if (files.length > 1) {
        showDropCompositionWarning();
    } else {
        fileInput.files = files;
        showAlert("info", "The rms file in this form has been updated.");
    }

}

function hasImageExtension(name) {
    let nameLower = name.toLowerCase();
    for (let ext of [".png", ".jpg", ".jpeg", ".bmp"]) {
        if (nameLower.endsWith(ext)) {
            return true;
        }
    }
    return false;
}

function hasRmsExtension(name) {
    return name.toLowerCase().endsWith(".rms");
}

function showDropCompositionWarning() {
    showAlert("warning", "Please drop only one single rms file or only images file(s) at a time!");
}

function showAlert(type, message) {
    $('#alert-area').prepend('<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">\n' +
        '  ' + message + '\n' +
        '  <button type="button" class="close" data-dismiss="alert" aria-label="Close">\n' +
        '    <span aria-hidden="true">&times;</span>\n' +
        '  </button>\n' +
        '</div>');
}