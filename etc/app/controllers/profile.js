import base, {route} from './base'

import users from 'services/users'

import Profile from 'templates/profile.jade'
import Awards from 'templates/awards.jade'

export default class extends base {

    @route('/profile')
    profile() {
        this.freeze();

        users.me()
            .then(_ => this.push(Profile, _))
    }

    @route('/awards')
    awards() {
        this.freeze();

        users.me()
            .then(_ => this.push(Awards, _))
    }
}