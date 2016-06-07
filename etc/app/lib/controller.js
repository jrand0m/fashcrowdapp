import page from 'bower/page/page'

import queryParser from './query-parser'

var globalId = 10000,
    controllers = new WeakMap(),
    APP_BASE = (window.APP_BASE === undefined ? '/app' : '') || window.APP_BASE;

export function Route(path: string) {
    return function (target, method) {
        target.__ID = target.__ID || ('controller-' + (globalId++));
        page(APP_BASE + path, (ctx, next) => {
            var cnt = controllers[target.__ID];
            if (!cnt) {
                cnt = controllers[target.__ID] = new target.constructor;
            }

            ctx.querystring = queryParser(ctx.querystring);

            cnt[method].call(cnt, ctx, next);
        })
    }
}

export function navigate(path) {
    page.redirect(path.indexOf(APP_BASE) == 0 ? path : APP_BASE + path);
}

var fd = null;

page('*', (ctx, next) => {
    ctx.formData = fd;
    fd = null;
    next();
});

export function dispatchFormData(path, formData) {
    fd = formData;
    navigate(path);
}
