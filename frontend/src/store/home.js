export default {
  state: {
    currentProfile: {},
    currentProfileTab: 'description',
    userProfile: {},
    settings: {},
    userPosts: [],
    userSubs: [],
    foundProfiles: [],
    bookMarks: [],
    savedData: {},
    ImgBlur: 0,
  },
  getters: {
    getProfileTab(state) {
      return state.currentProfileTab;
    },
    getImgBlur(state) {
      return state.ImgBlur;
    },
    getFoundProfiles(state) {
      return state.foundProfiles;
    },
    getSavedData(state) {
      return state.savedData;
    },
    getUserSubs(state) {
      return state.userSubs;
    },
    getCurrProfile(state) {
      return state.currentProfile;
    },
    getUserProfile(state) {
      return state.userProfile;
    },
    getUserPosts(state) {
      return state.userPosts;
    },
    getUserBookmarks(state) {
      return state.bookMarks;
    },
    getUserSettings(state) {
      return state.settings;
    }
  },
  mutations: {
    setProfileTab(state, payload) {
      state.currentProfileTab = payload;
    },
    setFoundProfiles(state, payload) {
      state.foundProfiles = payload;
    },
    dropFoundProfiles(state, payload) {
      let len = state.foundProfiles.length;
      state.foundProfiles.splice(payload, len);
    },
    deleteProfilePost(state, payload) {
      state.userPosts.splice(payload, 1);
    },
    setImgBlur(state, payload) {
      state.ImgBlur = payload;
    },
    setSavedData(state, payload) {
      state.savedData = payload;
    },
    setUserSubs(state, payload) {
      state.userSubs = payload;
    },
    dropUserSubs(state) {
      state.userSubs.splice(0, state.userSubs.length);
    },
    setCurrProfile(state, payload) {
      state.currentProfile = payload;
    },
    setUserProfile(state, payload) {
      state.userProfile = payload;
    },
    setUserPosts(state, payload) {
      if (!payload.top) {
        let len = state.userPosts.length;
        state.userPosts.splice(0, len);
      }

      state.userPosts = state.userPosts.concat(payload.posts);
    },
    dropUserPosts(state) {
      state.userPosts.splice(0, state.userPosts.length);
    },
    setUserBookmarks(state, payload) {
      state.bookMarks = payload;
    },
    addUserBookmark(state, payload) {
      state.bookMarks.unshift(payload);
    },
    setUserSettings(state, payload) {
      state.settings = payload;
    }
  },
  actions: {
    addUserProfileInSubs(context, data) {
      axios
        .get(
          "http://127.0.0.1:8000/api/v1/news/subscribe/?q=" +
            data.q +
            "&me=" +
            data.me,
          {
            headers: { Authorization: "Token " + data.token }
          }
        )
        .then(() => {
          let profile = context.getters.getUserProfile;
          profile.subs_profiles += data.q + "|";

          let currProfile = context.getters.getCurrProfile;
          currProfile.readers++;

          context.commit("setUserProfile", profile);
          context.commit("setCurrProfile", currProfile);
          context.dispatch('saveToDB', { store: "profile", key: "userprofile", data: profile });
        });
    },
    deleteUserProfileFromSubs(context, data) {
      axios
        .get(
          "http://127.0.0.1:8000/api/v1/news/unsubscribe/?q=" +
            data.q +
            "&me=" +
            data.me,
          {
            headers: { Authorization: "Token " + data.token }
          }
        )
        .then(() => {
          let profile = context.getters.getUserProfile;
          profile.subs_profiles = profile.subs_profiles.replace(
            "|" + data.q + "|",
            "|"
          );
          
          let currProfile = context.getters.getCurrProfile;
          currProfile.readers--;

          context.commit("setUserProfile", profile);
          context.commit("setCurrProfile", currProfile);
          context.dispatch('saveToDB', { store: "profile", key: "userprofile", data: profile });
        });
    },
    loadBookmarksFromServer(context) {
      let token = localStorage.getItem("token");
      let username = context.getters.getUserData.username;

      axios
        .get(
          "http://127.0.0.1:8000/api/v1/news/post/bookmarks/?me=" + username,
          {
            headers: { Authorization: "Token " + token }
          }
        )
        .then(response => {
          context.commit("setUserBookmarks", response.data);
          context.dispatch("saveToDB", {
            store: "profile",
            key: "bookmarks",
            data: response.data
          });
        });
    },
    loadSettingsFromServer(context) {
      let token = localStorage.getItem("token");
      let user_id = context.getters.getUserData.id;

      axios
        .get("http://127.0.0.1:8000/api/v1/home/settings_get/?q=" + user_id, {
          headers: { Authorization: "Token " + token }
        })
        .then(response => {
          context.commit("setUserSettings", response.data[0]);
          context.dispatch("saveToDB", {
            store: "settings",
            key: "settings",
            data: response.data[0]
          });
        });
    },
    loadUserProfileFromServer(context) {
      let token = localStorage.getItem("token");
      let username = context.getters.getUserData.username;

      axios
        .get("http://127.0.0.1:8000/api/v1/home/profile/" + username, {
          headers: { Authorization: "Token " + token }
        })
        .then(response => {
          context.commit("setUserProfile", response.data[0]);
          context.dispatch("saveToDB", {
            store: "profile",
            key: "userprofile",
            data: response.data[0]
          });
        });
    },
    saveToDB(context, obj) {
      var openRequest = indexedDB.open(obj.store, 1);

      openRequest.onupgradeneeded = () => {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains(obj.store)) {
          DB.createObjectStore(obj.store);
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
      };

      openRequest.onsuccess = () => {
        var DB = openRequest.result;

        let tx = DB.transaction(obj.store, "readwrite");
        let store = tx.objectStore(obj.store);

        store.put(obj.data, obj.key);
      };
    },
    loadUserBookmarks(context) {
      var openRequest = indexedDB.open("profile", 1);

      openRequest.onupgradeneeded = () => {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains("profile")) {
          DB.createObjectStore("profile");
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
      };

      openRequest.onsuccess = () => {
        var DB = openRequest.result;

        let tx = DB.transaction("profile", "readonly");
        let store = tx.objectStore("profile");

        let bookmarks = store.get("bookmarks");

        tx.oncomplete = () => {
          if (bookmarks.result) {
            if (typeof(bookmarks.result) == 'string') context.commit("setUserBookmarks", JSON.parse(bookmarks.result));
            if (typeof(bookmarks.result) == 'object') context.commit("setUserBookmarks", bookmarks.result);
          } else {
            context.dispatch("loadBookmarksFromServer");
          }
        };
      };
    },
    loadUserSettings(context) {
      var openRequest = indexedDB.open("settings", 1);

      openRequest.onupgradeneeded = () => {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains("settings")) {
          DB.createObjectStore("settings");
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
      };

      openRequest.onsuccess = () => {
        var DB = openRequest.result;

        let tx = DB.transaction("settings", "readonly");
        let store = tx.objectStore("settings");

        let settings = store.get("settings");

        tx.oncomplete = () => {
          if (settings.result) {
            context.commit("setUserSettings", settings.result);
          } else {
            context.dispatch("loadSettingsFromServer");
          }
        };
      };
    },
    loadUserProfile(context) {
      var openRequest = indexedDB.open("profile", 1);

      openRequest.onupgradeneeded = () => {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains("profile")) {
          DB.createObjectStore("profile");
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
      };

      openRequest.onsuccess = () => {
        var DB = openRequest.result;

        let tx = DB.transaction("profile", "readonly");
        let store = tx.objectStore("profile");

        let profile = store.get("userprofile");

        tx.oncomplete = () => {
          if (profile.result) {
            context.commit("setUserProfile", profile.result);
          } else {
            context.dispatch("loadUserProfileFromServer");
          }
        };
      };
    },
    LoadProfile(context, data) {

      if (data.blog) {
        context.commit("setCurrProfile", data.blog);
      } else if (!data.isAdmin) {
        let token = localStorage.getItem("token");
        let domain = context.getters.getDomain;
        let username = data.username;

        axios
          .get(`${domain}/api/v1/home/profile/${username}/`, {
            headers: {
              Authorization: "Token " + token
            }
          })
          .then(response => {
            context.commit("setCurrProfile", response.data[0]);
          })
          .catch(function(e) {
            console.log(e);
          });
      }
    }
  }
};
