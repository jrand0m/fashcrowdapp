import {Route, navigate} from 'lib/controller'

import $ from 'lib/jquery'

export const route = Route;

export default class {

    freeze() {
        $('#page-cnt').addClass('freeze');
    }

    push(tpl, data) {
        $('#page-cnt')
            .html($.parseHTML(tpl({model: data})))
            .removeClass('freeze');
    }

    update() {
        $('#page-cnt').removeClass('freeze');
    }

    shade(tpl, data) {
        $($.parseHTML(tpl({model: data})))
            .appendTo($('#page-cnt').removeClass('freeze'));
    }

    navigate(path: string) {
        $('#page-cnt').removeClass('freeze');

        navigate(path)
    }
}