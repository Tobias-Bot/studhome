export default {
    state: {
        maxPictureSize: 5242880,
        domain: 'http://127.0.0.1:8000',
    },
    mutations: {
    },
    getters: {
        getDomain(state) {
            return state.domain;
        }
    }
}