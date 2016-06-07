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

const BASE_URL = window.BASE_URL || '';

export default class Base {

    get_(url: string, data: Object): Promise {
        return new Promise((resolve, reject) => {
            $.getJSON(BASE_URL + url, data)
                .done(resolve)
                .fail(reject);

        })
    }

    post_(url: string, data: FormData): Promise {

        data.append('csrfmiddlewaretoken', getCookie('csrftoken'));

        return new Promise((resolve, reject) => {

            var oReq = new XMLHttpRequest();
            oReq.open("POST", BASE_URL + url + (url.indexOf('?') >= 0 ? '&': '?') + 'format=json');

            oReq.addEventListener("load", _ => resolve(JSON.parse(oReq.responseText)));
            oReq.addEventListener("error", _ => reject());

            oReq.send(data);
        })
    }
}