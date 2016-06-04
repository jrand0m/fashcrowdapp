import base from './base';

export default new class extends base {

    get_all(data?: Object): Promise {
        return this.get_('/api/tasks/', data || {})
    }

    post(data): Promise {
        return this.post_('/api/tasks/', data);
    }
}
