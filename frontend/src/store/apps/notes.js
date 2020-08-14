export default {
    state: {
        notes: [],
    },
    mutations: {
        addNote(state, payload) {
            state.notes.push(payload);
        },
        setNote(state, payload) {
            state.notes.splice(payload.index, 1, payload.data);
        },
        deleteNote(state, payload) {
            state.notes.splice(payload, 1);
        },
    },
    getters: {
        getNotes(state) {
            return state.notes;
        },
        getNote(state, i) {
            return state.notes[i];
        }
    }
}