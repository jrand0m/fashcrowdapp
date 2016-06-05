import base, {route} from './base'

import users from 'services/users'

import Profile from 'templates/profile.jade'

export default class extends base {

    @route('/profile')
    index() {
        this.freeze();

        users.me()
            .then(_ => this.push(Profile, _))
    }
}