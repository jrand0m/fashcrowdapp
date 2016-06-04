import base from './base';

export default new class extends base {

    get(data?: Object): Promise {
        return this.get_('/api/calls/', data || {})
    }

    approve(id) {
        return this.get_(`/api/calls/${id}/approve/`, {})
    }

    decline(id) {
        return this.get_(`/api/calls/${id}/decline/`, {})
    }
}
