var md = window.markdownit({breaks: true})
    .disable(['image']);
$('.markdown-text').each(
    function (nr, it) {
        let it_select = $(it);
        it_select.html(
            md.render(it_select.text())
                .replace(/<h5/g, "<h6")
                .replace(/<\/h5/g, "</h6")
                .replace(/<h4/g, "<h6")
                .replace(/<\/h4/g, "</h6")
                .replace(/<h3/g, "<h5")
                .replace(/<\/h3/g, "</h5")
                .replace(/<h2/g, "<h4")
                .replace(/<\/h2/g, "</h4")
                .replace(/<h1/g, "<h3")
                .replace(/<\/h1/g, "</h3")
        );
    });