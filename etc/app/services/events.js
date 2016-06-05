import base from './base';

var handlers = [],
    timestamp = (new Date).getTime() * 1000,
    delay_min = 557,
    delay_max = 10000,
    delay = delay_min;

function _update_delay(ml) {
    delay = Math.ceil(Math.max(delay_min, Math.min(delay_max, delay * ml)));
}


function _start(service) {

    service
        .get_('/api/events/', {min: timestamp})
        .then(_ => {
            _update_delay(.7);

            timestamp = _.reduce((x, a) => Math.max(x, a.date), timestamp);
            if (_.length > 0)
                handlers.forEach(cb => setTimeout(() => cb(_), 1));

            setTimeout(() => _start(service), delay);
        })
        .catch(() => {
            _update_delay(2);

            setTimeout(() => _start(service), delay);
        });
}

export default new class extends base {

    constructor() {
        super();
        _start(this);
    }

    on(cb: Function<void, Array>): void {
        handlers.push(cb);
    }

    off(cb) {
        handlers = handlers.filter(_ => _ != cb);
    }
}