import base, {route} from './base'

import tasks from 'services/tasks'

import taskForm from 'templates/task-new.jade'

export default class extends base {

    @route('/task/new')
    create() {
        this.push(taskForm, {});
    }

    @route('/task/save')
    save(ctx) {
        this.freeze();

        tasks.post(ctx.querystring)
            .then(_ => this.update())
            .then(_ => this.navigate("/"))
    }
}