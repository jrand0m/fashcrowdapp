import $ from 'lib/jquery'

function getCookie(c_name) {
    var i, x, y, cookies = document.cookie.split(";");

    for (i = 0; i < cookies.length; i++) {
        x = cookies[i].substr(0, cookies[i].indexOf("="));
        y = cookies[i].substr(cookies[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, "");
        if (x == c_name) {
            return unescape(y);
        }
    }
}

export default class Base {

    get_(url: string, data: Object): Promise {
        return new Promise((resolve, reject) => {
            $.getJSON(url, data)
                .done(resolve)
                .fail(reject);

        })
    }

    post_(url: string, data: Object): Promise {
        url += (url.indexOf('?') >= 0 ? '&' : '?') + `_csrf=${getCookie('csrftoken')}`;

        return new Promise((resolve, reject) => {
            $.post(url, data, null, 'json')
                .done(resolve)
                .fail(reject);
        })
    }
}