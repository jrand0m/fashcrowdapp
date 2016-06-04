import base, {route} from './base'

import tasks from 'services/tasks'

import renderTasks from 'templates/tasks.jade'

export default class extends base {

    @route('/')
    index() {
        this.navigate('/task/feed')
    }
}