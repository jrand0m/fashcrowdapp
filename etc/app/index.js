import $ from 'lib/jquery'

import Layout from 'templates/layout.jade'

$(() => {
    "use strict";

    var data = JSON.parse($('#profile').text());

    $($.parseHTML(Layout(data))).appendTo('body');
});