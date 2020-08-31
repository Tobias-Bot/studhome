<template>
  <div>
    <img src="@/static/login.gif" class="imgLogin" />
    <div class="card">
      <div class="card-header">
        <h5>Вход</h5>
      </div>
      <div class="card-body">
        <h6>Имя пользователя</h6>
        <input
          v-model="username"
          type="name"
          class="form-control textInput"
          :class="{
            'is-invalid':
              $v.username.$dirty &&
              (!$v.username.required ||
                !$v.username.maxLength ||
                !$v.username.minLength),
          }"
        />
        <div v-show="$v.username.$invalid" class="invalid-feedback">
          ой, похоже, здесь что-то не так:
        </div>
        <div v-show="!$v.username.required" class="invalid-feedback">
          * это обязательное поле
        </div>
        <div v-show="!$v.username.maxLength" class="invalid-feedback">
          * максимальная длина {{ $v.username.$params.maxLength.max }}
        </div>
        <div v-show="!$v.username.minLength" class="invalid-feedback">
          * минимальная длина {{ $v.username.$params.minLength.min }}
        </div>
        <br />
        <h6>Пароль</h6>
        <input
          v-model.trim="password"
          type="password"
          class="form-control textInput"
          :class="{
            'is-invalid':
              $v.password.$dirty &&
              (!$v.password.required || !$v.password.minLength),
          }"
        />
        <div v-show="$v.password.$invalid" class="invalid-feedback">
          ой, похоже, здесь что-то не так:
        </div>
        <div v-show="!$v.password.required" class="invalid-feedback">
          * это обязательное поле
        </div>
        <div v-show="!$v.password.minLength" class="invalid-feedback">
          * минимальная длина {{ $v.password.$params.minLength.min }}
        </div>
      </div>
      <div class="card-footer">
        <router-link to="/home">
          <button class="btn btnMain" @click="LoginFunc" :disabled="loading">
            <span v-show="!loading">войти</span>
            <div v-show="loading" class="spinner-border" role="status">
            </div>
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { required, minLength, maxLength } from "vuelidate/lib/validators";

export default {
  data: function() {
    return {
      loading: false,

      username: "",
      password: "",
    };
  },
  validations: {
    username: { required, maxLength: maxLength(50), minLength: minLength(3) },
    password: { required, minLength: minLength(6) },
  },
  methods: {
    LoginFunc() {
      this.loading = true;

      if (this.$v.$invalid) {
        this.$v.$touch();
        return;
      }

      let loginData = {
        username: this.username,
        password: this.password,
      };

      let domain = this.$store.getters.getDomain;

      axios
        .post(`${domain}/api/v1/auth_token/token/login`, loginData)
        .then((response) => {
          let token = response.data.auth_token;

          this.$store.commit("setToken", token);
          localStorage.setItem("token", token);
          this.$store.dispatch("addUserData", token);
          this.$store.commit("setAuth", true);

          this.$router.push("/home");
          this.loading = false;
        });
    },
    RegisterFunc() {
      this.RegistrationData.username = this.UserData.username;
      this.RegistrationData.password = this.UserData.pass1;
      this.RegistrationData.email = this.UserData.email;

      let domain = this.$store.getters.getDomain;

      // axios
      //   .post(`${domain}/api/v1/auth/users/`, this.RegistrationData)
      //   .then(() => {
      //     this.LoginFunc();
      //   });
    },
  },
};
</script>

<style scoped>
.spinner-border {

}

.imgLogin {
  position: absolute;
  z-index: -1;
  width: 100%;
  height: 110%;
}

.btn {
  position: relative;
  width: 50%;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 5px 15px 5px 15px;
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.8);
  transition: 0.2s all;
}
.btn:hover {
  color: white;
  background-color: rgba(0, 0, 0, 0.9);
}

.card {
  position: absolute;
  width: 25%;
  top: 28%;
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.7);
  border-radius: 7px 30px 7px 30px;
}
.card-header {
  border-radius: 7px 30px 0 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(0, 0, 0, 0.6);
}
.card-footer {
  border-radius: 0 30px 7px 30px;
}
</style>
