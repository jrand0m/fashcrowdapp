import base, {route} from './base'

import tasks from 'services/tasks'

import TaskForm from 'templates/task-new.jade'
import TaskFeed from 'templates/task-feed.jade'
import TaskDetails from 'templates/task-details.jade'
import Tasks from 'templates/tasks.jade'

export default class extends base {

    @route('/task/new')
    create() {
        this.push(TaskForm, {});
    }

    @route('/task/save')
    save(ctx) {
        this.freeze();

        tasks.post(ctx.querystring)
            .then(_ => this.update())
            .then(_ => this.navigate("/"))
    }

    @route('/task/feed')
    feed() {
        this.freeze();

        tasks.get_available()
            .then(_ => this.push(TaskFeed, _))
    }

    @route('/task/my')
    my() {
        this.freeze();

        tasks.get_posted()
            .then(_ => this.push(Tasks, _))
    }

    @route('/task/:id/details')
    details(ctx) {
        this.freeze();

        console.log(ctx);

        tasks.get(ctx.params.id)
            .then(_ => this.shade(TaskDetails, _))
    }

    @route('/task/:id/accept')
    accept(ctx) {
        this.freeze();

        tasks.accept(ctx.params.id)
            .then(_ => this.navigate('/task/my'));
    }

    @route('/task/:id/reject')
    accept(ctx) {
        this.freeze();

        tasks.reject(ctx.params.id)
            .then(_ => this.navigate('/task/feed'));
    }
}