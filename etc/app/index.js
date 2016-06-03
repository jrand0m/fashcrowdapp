import jQuery from 'lib/jquery'

import Layout from 'templates/layout.jade'

jQuery(() => {
    "use strict";

    jQuery.parseHTML(Layout({})).appendTo('body');
});