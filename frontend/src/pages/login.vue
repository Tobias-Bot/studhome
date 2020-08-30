<template>
  <div class="box">
    <div class="nav nav-tabs" id="v-pills-tab" role="tablist">
      <a
        class="login-tab"
        id="v-pills-settings-tab"
        data-toggle="tab"
        href="#registration"
        role="tab"
        aria-selected="false"
        >регистрация</a
      >
      <a
        class="login-tab"
        id="v-pills-settings-tab"
        data-toggle="tab"
        href="#login"
        role="tab"
        aria-selected="false"
        >войти</a
      >
    </div>
    <div class="tab-content">
      <div class="tab-pane fade show" id="registration" role="tabpanel">
        <div class="card">
          <div class="card-header">
            <h5>Регистрация</h5>
          </div>
          <div class="card-body">
            <h6>Имя пользователя</h6>
            <input v-model="UserData.username" type="name" class="form-control textInput" />
            <br />
            <h6>Пароль</h6>
            <input v-model="UserData.pass1" type="password" class="form-control textInput" />
            <br />
            <h6>Повторите пароль</h6>
            <input v-model="UserData.pass2" type="password" class="form-control textInput" />
          </div>
          <div class="card-footer">
            <router-link to="/home">
              <button class="btn btn-dark btnMain" @click="RegisterFunc">
                начать
              </button>
            </router-link>
          </div>
        </div>
      </div>
      <div class="tab-pane fade show active" id="login" role="tabpanel">
        <div class="card">
          <div class="card-header">
            <h5>Вход</h5>
          </div>
          <div class="card-body">
            <h6>Имя пользователя</h6>
            <input v-model="UserData.username" type="name" class="form-control textInput" />
            <br />
            <h6>Пароль</h6>
            <input v-model="UserData.pass1" type="password" class="form-control textInput" />
          </div>
          <div class="card-footer">
            <router-link to="/home">
              <button class="btn btn-dark btnMain" @click="LoginFunc">
                войти
              </button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      UserData: {
        username: "",
        pass1: "",
        pass2: ""
      },
      RegistrationData: {
        username: "",
        password: ""
      },
      LoginData: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    LoginFunc() {
      this.LoginData.username = this.UserData.username;
      this.LoginData.password = this.UserData.pass1;
      
      let domain = this.$store.getters.getDomain;

      axios
        .post(
          `${domain}/api/v1/auth_token/token/login`,
          this.LoginData
        )
        .then(response => {
          let token = response.data.auth_token;

          this.$store.commit("setToken", token);
          localStorage.setItem("token", token);
          this.$store.dispatch("addUserData", token);
          this.$store.commit("setAuth", true);
        });
    },
    RegisterFunc() {
      this.RegistrationData.username = this.UserData.username;
      this.RegistrationData.password = this.UserData.pass1;
      this.RegistrationData.email = this.UserData.email;

      let domain = this.$store.getters.getDomain;

      axios
        .post(`${domain}/api/v1/auth/users/`, this.RegistrationData)
        .then(() => {
          this.LoginFunc();
        });
    }
  }
};
</script>

<style scoped>
.btn {
  float: right;
}

.card {
  width: 40%;
  left: 50%;
  transform: translateX(-50%);
}

.nav-tabs {
  margin-bottom: 2%;
  border: none;
}

.login-tab {
  position: relative;
  display: inline;
  margin-right: 2%;
  font-size: 25px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: -2px 2px 3px rgba(0, 0, 0, 0.5);
  text-decoration: none;
}
.login-tab:hover {
  color: rgba(255, 255, 255, 1);
}
</style>
