import base from './base';

export default new class extends base {

    me(): Promise {
        return this.get_('/api/users/me/', {})
    }
}
