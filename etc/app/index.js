import $ from 'lib/jquery'
import {navigate} from 'lib/controller'

import btAlerts from 'bootstrap/alert'

import feed from 'controllers/feed'
import task from 'controllers/task'

import events from 'services/events'

import Layout from 'templates/layout.jade'
import Alerts from 'templates/alerts.jade'

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
        })
        .on('click', '.dialog .close-me', e => {
            e.preventDefault();
            $(e.target).closest('.dialog').remove()
        });

    console.log('Start');

    navigate(window.location.pathname + window.location.search);

    events.on(_ => {
        console.log('events', _);
        $($.parseHTML(Alerts({model: _}))).prependTo('#alerts')
    })
});