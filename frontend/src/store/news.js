export default {
  state: {
    SearchTag: "",

    posts: [],
    myNewsPosts: [],
    searchPosts: [],

    currentPost: {},
    postMarks: [],
    createdPostMarks: [],
    currentComments: [],

    hash: '',
  },
  mutations: {
    setHash(state, payload) {
      state.hash = payload;
    },
    dropCreatedPostMarks(state, payload) {
      let len = state.createdPostMarks.length;
      state.createdPostMarks.splice(payload, len);
    },
    setPostMarks(state, payload) {
      state.createdPostMarks = payload;
    },
    addCreatedPostMarks(state, payload) {
      state.createdPostMarks.push(payload);
    },
    deleteCreatedPostMarks(state, payload) {
      let len = state.createdPostMarks.length;
      let buf = state.createdPostMarks.filter(mark => mark != payload);

      state.createdPostMarks.splice(0, len);
      state.createdPostMarks = buf;
    },
    addPostMark(state, payload) {
      state.postMarks.push(payload);

      console.log(state.postMarks);
    },
    deletePostMark(state, payload) {
      let index = state.postMarks.findIndex(mark => mark.id == payload);
      state.postMarks.splice(index, 1);

      console.log(state.postMarks);
    },
    dropPostMarks(state) {
      state.postMarks.splice(0, state.postMarks.length);
    },
    setSearchTag(state, payload) {
      state.SearchTag = payload;
    },
    setPost(state, payload) {
      if (!payload.top) {
        let len = state.posts.length;
        state.posts.splice(0, len);
      }

      state.posts = state.posts.concat(payload.posts);
    },
    setPhotoPost(state, payload) {
      state.photoPosts = payload;
    },
    setTextPost(state, payload) {
      state.textPosts = payload;
    },
    setPopularPost(state, payload) {
      state.popularPosts = payload;
    },
    setMyNewsPost(state, payload) {
      state.myNewsPosts = payload;
    },
    setPostsByMarks(state, payload) {
      state.postsByMarks = payload;
    },
    deletePost(state, payload) {
      state.posts.splice(payload, 1);
    },
    setSearchPost(state, payload) {
      state.searchPosts = payload;
    },
    deleteSearchPost(state, payload) {
      state.searchPosts.splice(payload, 1);
    },
    dropSearchPost(state, payload) {
      let len = state.searchPosts.length;
      state.searchPosts.splice(payload, len);
    },
    setCurrentPost(state, payload) {
      state.currentPost = payload;
    },
    setCurrentComms(state, payload) {
      state.currentComments = payload;
    },
    addCurrentComm(state, payload) {
      if (!payload.parent) {
        state.currentComments.unshift(payload);
      }

      state.currentPost.comments_count += 1;
    },
    deleteCurrentComm(state, payload) {
      state.currentPost.comments_count -= 1;
    }
  },
  getters: {
    getHash(state) {
      return state.hash;
    },
    getCreatedPostMarks(state) {
      return state.createdPostMarks;
    },
    getPostsByMarks(state) {
      return state.postsByMarks;
    },
    getPostMarks(state) {
      return state.postMarks;
    },
    getSearchTag(state) {
      return state.SearchTag;
    },
    getPosts(state) {
      return state.posts;
    },
    getPhotoPosts(state) {
      return state.photoPosts;
    },
    getTextPosts(state) {
      return state.textPosts;
    },
    getPopularPosts(state) {
      return state.popularPosts;
    },
    getMyNewsPosts(state) {
      return state.myNewsPosts;
    },
    getSearchPost(state) {
      return state.searchPosts;
    },
    getCurrentPost(state) {
      return state.currentPost;
    },
    getCurrentComms(state) {
      return state.currentComments;
    }
  },
  actions: {
    FindData(context, searchData) {
      let token = context.getters.getToken;

      context.commit(
        "setSearchTag",
        searchData.substring(1, searchData.length - 1)
      );

      axios
        .get("http://127.0.0.1:8000/api/v1/news/search/?q=" + searchData, {
          headers: {
            Authorization: "Token " + token
          }
        })
        .then(response => {
          context.commit("setSearchPost", response.data);
        })
        .catch(function(e) {
          console.log(e);
        });
    },
    FindPeople(context, searchData) {
      let token = context.getters.getToken;
      let domain = context.getters.getDomain;

      context.commit("setSearchTag", searchData);

      axios
        .get(`${domain}/api/v1/news/search_people/?q=${searchData}`, {
          headers: {
            Authorization: "Token " + token
          }
        })
        .then(response => {
          context.commit("setFoundProfiles", response.data);
        })
        .catch(function(e) {
          console.log(e);
        });
    },
    SendComment(context, data) {
      let token = context.getters.getToken;
      let domain = context.getters.getDomain;
      let result;

      result = axios
        .post(`${domain}/api/v1/news/post/${data.post}/comment/`, data, {
          headers: { Authorization: "Token " + token }
        })
        .then(function(response) {
          context.commit("addCurrentComm", response.data);
          return response.data;
        })
        .catch(function(e) {
          console.log(e);
        });

      return result;
    },
    deletePostFromServer(context, data) {
      let token = context.getters.getToken;
      let username = context.getters.getUserData.username;
      let profile = context.getters.getUserProfile;

      axios
        .delete(
          "http://127.0.0.1:8000/api/v1/news/post_delete/" +
            data.post_id +
            "/" +
            username +
            "/",
          {
            headers: { Authorization: "Token " + token }
          }
        )
        .catch(function(e) {
          console.log(e);
        });

      if (data.topic == "all") context.commit("deletePost", data.post_index);
      if (data.topic == "search")
        context.commit("deleteSearchPost", data.post_index);
      if (data.topic == "profile")
        context.commit("deleteProfilePost", data.post_index);

      profile.posts_count = profile.posts_count - 1;

      context.dispatch("saveToDB", {
        store: "profile",
        key: "userprofile",
        data: profile
      });
    },
    DropStorage(context, objstore) {
      var openRequest = indexedDB.open(objstore, 1);

      openRequest.onupgradeneeded = () => {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains(objstore)) {
          DB.createObjectStore(objstore);
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
      };

      openRequest.onsuccess = () => {
        var DB = openRequest.result;

        let tx = DB.transaction(objstore, "readwrite");
        let store = tx.objectStore(objstore);

        store.clear();
      };
    },
    MyNewsPostLoader(context, data) {
      let token = context.getters.getToken;
      let username = context.getters.getUserData.username;
      let domain = context.getters.getDomain;

      axios
        .get(
          `${domain}/api/v1/news/post/mysubs/all/?me=${username}&d=${data}`,
          {
            headers: { Authorization: "Token " + token }
          }
        )
        .then(response => {
          let posts = response.data;
          context.commit("setMyNewsPost", posts);
        })
        .catch(function(e) {
          console.log(e);
        });
    },
    AllPostLoader(context, data) {
      let token = context.getters.getToken;
      let domain = context.getters.getDomain;

      axios
        .get(`${domain}/api/v1/news/post/all/?a=${data.top}&b=${data.bottom}`, {
          headers: { Authorization: "Token " + token }
        })
        .then(response => {
          let posts = response.data;
          context.commit("setPost", { top: data.top, posts });
        })
        .catch(function(e) {
          console.log(e);
        });
    },
    AllPostByTypeLoader(context, data) {
      let token = context.getters.getToken;
      let domain = context.getters.getDomain;

      axios
        .get(`${domain}/api/v1/news/post/type/?q=|${data.value}|&a=${data.top}&b=${data.bottom}`, {
          headers: { Authorization: "Token " + token }
        })
        .then(response => {
          let posts = response.data;

          context.commit("setPost", { top: data.top, posts });
        })
        .catch(function(e) {
          console.log(e);
        });
    },
    AllPopularPostLoader(context, data) {
      let token = context.getters.getToken;
      let domain = context.getters.getDomain;

      axios
        .get(`${domain}/api/v1/news/post/popular/?a=${data.top}&b=${data.bottom}`, {
          headers: { Authorization: "Token " + token }
        })
        .then(response => {
          let posts = response.data;
          
          context.commit("setPost", { top: data.top, posts });
        })
        .catch(function(e) {
          console.log(e);
        });
    },
    PostsByMarksLoader(context, data) {
      let marks = context.getters.getPostMarks;

      if (marks.length) {
        let token = context.getters.getToken;
        let domain = context.getters.getDomain;
        let buf = marks.map(mark => mark.name);

        axios
          .get(`${domain}/api/v1/news/post/marks/?q=|${buf.join("|")}|&a=${data.top}&b=${data.bottom}`, {
            headers: { Authorization: "Token " + token }
          })
          .then(response => {

            context.commit("setPost", { posts: response.data, top: data.top });
          })
          .catch(function(e) {
            console.log(e);
          });
      }
    }
  }
};
