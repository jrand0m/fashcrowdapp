import base, {route} from './base'

import tasks from 'services/tasks'

import renderTasks from 'templates/tasks.jade'

export default class extends base {

    @route('/')
    index(ctx, next) {

        this.freeze();

        console.log('home', ctx);

        tasks.get_all()
            .then(_ => {
                this.push(renderTasks, _)
            })
            .catch(_ => {
                console.error(_);
            });
    }
}