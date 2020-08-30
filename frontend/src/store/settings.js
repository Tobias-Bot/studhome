export default {
    state: {
        maxPictureSize: 5242880,
        domain: 'http://192.168.1.57:8000',
    },
    mutations: {
    },
    getters: {
        getDomain(state) {
            return state.domain;
        }
    }
}