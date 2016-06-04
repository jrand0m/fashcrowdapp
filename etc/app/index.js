import $ from 'lib/jquery'
import {navigate} from 'lib/controller'

import feed from 'controllers/feed'
import task from 'controllers/task'

import Layout from 'templates/layout.jade'

$(() => {
    var data = JSON.parse($('#profile').text());

    $($.parseHTML(Layout(data))).appendTo('body');

    $('body')
        .on('click', '[data-href]', e => {
            e.preventDefault();
            navigate($(e.target).data('href'));
        })
        .on('submit', '[data-action]', e => {
            e.preventDefault();
            navigate($(e.target).data('action') + '?' + $(e.target).serialize());
        });

    console.log('Start');

    navigate(window.location.pathname + window.location.search);
});