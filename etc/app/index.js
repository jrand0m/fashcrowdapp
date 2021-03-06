import $ from 'lib/jquery'
import {navigate, dispatchFormData} from 'lib/controller'

import touchEvents from 'bower/jQuery-Touch-Events/index'

import btAlerts from 'bootstrap/alert'

import feed from 'controllers/feed'
import task from 'controllers/task'
import profile from 'controllers/profile'

import events from 'services/events'

import Layout from 'templates/layout.jade'
import Alerts from 'templates/alerts.jade'

$(() => {
    var data = {};

    $($.parseHTML(Layout(data))).appendTo('body');

    $('body')
        .on('click tap', '[data-href]', function (e) {
            e.preventDefault();
            navigate($(this).data('href'));
        })
        .on('submit', '[data-action]', e => {
            e.preventDefault();
            dispatchFormData($(e.target).data('action'), new FormData(e.target));
        })
        .on('click tap', '.dialog .close-me', e => {
            e.preventDefault();
            $(e.target).closest('.dialog').remove()
        });

    console.log('Start');

    navigate(window.location.pathname + window.location.search);

    events.on(_ => {
        $($.parseHTML(Alerts({model: _}))).prependTo('#alerts')
    })
});