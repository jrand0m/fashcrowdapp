import base, {route} from './base'

import tasks from 'services/tasks'
import calls from 'services/calls'

import TaskForm from 'templates/task-new.jade'
import TaskFeed from 'templates/task-feed.jade'
import TaskDetails from 'templates/task-details.jade'
import Tasks from 'templates/tasks.jade'
import Calls from 'templates/calls.jade'

export default class extends base {

    @route('/task/new')
    create() {
        this.push(TaskForm, {});
    }

    @route('/task/save')
    save(ctx) {
        this.freeze();

        console.log('formData in context', ctx.formData);

        tasks.post(ctx.formData)
            .then(_ => this.popup("Task created", "Now others can complete it", "/task/my"))
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

        tasks.get_created()
            .then(_ => this.push(Tasks, _, {tab: 'my'}))
    }

    @route('/task/active')
    active() {
        this.freeze();

        tasks.get_active()
            .then(_ => this.push(Tasks, _, {tab: 'active'}))
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
            .then(_ => this.popup('Challenge accepted', "Now good luck completing your flash", '/task/active'));
    }

    @route('/task/:id/reject')
    reject(ctx) {
        this.freeze();

        tasks.reject(ctx.params.id)
            .then(_ => this.navigate('/task/feed'));
    }

    @route('/task/:id/complete')
    complete(ctx) {
        this.freeze();

        tasks.complete(ctx.params.id, ctx.formData)
            .then(_ => this.popup('Challenge completed', "Now wait for approval to get your reward", '/task/active'));
    }

    @route('/calls')
    calls(ctx) {
        this.freeze();

        calls.get()
            .then(_ => this.push(Calls, _));
    }

    @route('/call/:id/approve')
    approve(ctx) {
        this.freeze();

        calls.approve(ctx.params.id)
            .then(_ => this.popup('Proof approved!', "You have approved the flasher's proof", '/calls'));
    }

    @route('/call/:id/decline')
    decline(ctx) {
        this.freeze();

        calls.decline(ctx.params.id)
            .then(_ => this.popup('Proof rejected!', "You have rejected the flasher's proof", '/calls'));
    }
}