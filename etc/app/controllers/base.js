import {Route, navigate} from 'lib/controller'

import $ from 'lib/jquery'

import Popup from 'templates/popup.jade'

function merge() {
    var x = {};
    [].slice
        .call(arguments)
        .filter(_ => _)
        .forEach(obj => {
            Object.keys(obj).forEach(key => {
                x[key] = x[key] || obj[key];
            })
        });

    return x;
}

export const route = Route;

export default class {

    freeze() {
        $('#page-cnt').addClass('freeze');
    }

    push(tpl, data, extra?) {
        $('#page-cnt')
            .html($.parseHTML(tpl(merge({model: data}, extra))))
            .removeClass('freeze');
    }

    update() {
        $('#page-cnt').removeClass('freeze');
    }

    shade(tpl, data, extra?) {
        $($.parseHTML(tpl(merge({model: data}, extra))))
            .appendTo($('#page-cnt').removeClass('freeze'));
    }

    navigate(path: string) {
        $('#page-cnt').removeClass('freeze');

        navigate(path)
    }

    popup(summary, message, redirect) {
        this.shade(Popup, {
            summary,
            message,
            href: redirect
        });
    }
}