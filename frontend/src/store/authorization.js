export default {
  state: {
    IsAuthorized: false,
    Token: "",
    RegistrationData: {
      username: "",
      email: "",
      pass1: "",
      pass2: ""
    },
    LoginData: {
      username: "",
      password: ""
    },
    UserData: {
      id: null,
      username: "",
      email: ""
    }
  },
  getters: {
    getRegistrationData(state) {
      return state.RegistrationData;
    },
    getLoginData(state) {
      return state.LoginData;
    },
    getToken(state) {
      return state.Token;
    },
    getAuth(state) {
      return state.IsAuthorized;
    },
    getUserData(state) {
      return state.UserData;
    }
  },
  mutations: {
    setRegistationDate(state, payload) {
      state.RegistrationData = payload;
    },
    setLoginDate(state, payload) {
      state.LoginData = payload;
    },
    setToken(state, payload) {
      state.Token = payload;
    },
    setAuth(state, payload) {
      state.IsAuthorized = payload;
    },
    setUserData(state, payload) {
      state.UserData = payload;
    }
  },
  actions: {
    addUserData(context, token) {
      let domain = context.getters.getDomain;

      axios
        .get(`${domain}/api/v1/auth/users/me`, {
          headers: { Authorization: "Token " + token }
        })
        .then(response => {
          let data = response.data;

          context.commit("setUserData", data);
          context.dispatch("loadUserBookmarks");
          context.dispatch("loadUserSettings");
          context.dispatch("loadUserProfile");
        });
    }
  }
};
