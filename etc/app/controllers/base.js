import {Route, navigate} from 'lib/controller'

import $ from 'lib/jquery'

export const route = Route;

export default class {

    freeze() {
        $('#page-cnt').addClass('freeze');
    }

    push(tpl, data) {
        var html = $.parseHTML(tpl({model: data}));
        $('#page-cnt').html(html).removeClass('freeze');
    }

    update() {
        $('#page-cnt').removeClass('freeze');
    }

    navigate(path: string) {
        $('#page-cnt').removeClass('freeze');

        navigate(path)
    }
}