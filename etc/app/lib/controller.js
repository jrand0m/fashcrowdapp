import page from 'bower/page/page'

import queryParser from './query-parser'

var globalId = 10000,
    controllers = new WeakMap();

export function Route(path: string) {
    return function (target, method) {
        target.__ID = target.__ID || ('controller-' + (globalId++));
        page('/app' + path, (ctx, next) => {
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
    page.redirect(path.match(/^\/app/) ? path : '/app' + path);
}

var fd = null;

page('*', (ctx, next) => {
    console.log('adding FormData to context', fd);
    ctx.formData = fd;
    fd = null;
    next();
});

export function dispatchFormData(path, formData) {
    console.log('caching FormData', formData);
    fd = formData;
    navigate(path);
}
