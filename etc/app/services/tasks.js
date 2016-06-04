import base from './base';

export default new class extends base {

    get(id) {
        return this.get_(`/api/tasks/${id}/`, {})
    }

    get_available(data?: Object): Promise {
        return this.get_('/api/tasks/available_tasks/', data || {})
    }

    get_active(data?: Object): Promise {
        return this.get_('/api/tasks/active_tasks/', data || {})
    }

    accept(id) {
        return this.get_(`/api/tasks/${id}/accept/`, {})
    }

    reject(id) {
        return this.get_(`/api/tasks/${id}/reject/`, {})
    }

    post(data): Promise {
        return this.post_('/api/tasks/', data);
    }
}
