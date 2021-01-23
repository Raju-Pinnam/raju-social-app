(function () {
    var baseUrl = 'http://127.0.0.1:8000/'
    if (window.myBookmarklet !== undefined) {
        myBookmarklet();
    } else {
        document.body.appendChild(document.createElement('script')).src = '' +
            baseUrl + 'static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 99999999);
    }
})();