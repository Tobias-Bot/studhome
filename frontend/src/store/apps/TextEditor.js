export default {
  state: {
    pages: []
  },
  mutations: {
    addPage(state, payload) {
      state.pages.push(payload);
    },
    setPage(state, payload) {
      let len = state.pages.length;
      state.pages.splice(0, len);

      state.pages.push(payload);
    }
  },
  getters: {
    getPages(state) {
      return state.pages;
    }
  },
  actions: {
    InitDB(context, storeName) {
      let openRequest = indexedDB.open(storeName, 1);

      openRequest.onupgradeneeded = () => {
        let DB = openRequest.result;
        if (!DB.objectStoreNames.contains(storeName)) {
          DB.createObjectStore(storeName);
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB :(", openRequest.error);
      };
    },
    SaveDocToDB() {}
  }
};
