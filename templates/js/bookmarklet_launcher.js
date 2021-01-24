(function () {
    var baseUrl = 'https://raju-social.herokuapp.com/';
    if (window.myBookmarklet !== undefined) {
        myBookmarklet();
    } else {
        document.body.appendChild(document.createElement('script')).src = '' +
            baseUrl + 'static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 99999999999999999999);
    }
})();