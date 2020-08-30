<template>
  <div class="card">
    <div class="card-header">
      <h4>аккаунт</h4>
    </div>
    <div class="card-body">
      <label
        >вы вошли как <b>{{ this.username }}</b></label
      ><br />
      <router-link
        type="button"
        class="btn btn-outline-danger btn-sm btnOption"
        to="/login"
      >
        <span style="width: 100%;" @click="LogoutFunc">выйти</span>
      </router-link>
    </div>
  </div>
</template>

<script>

export default {
  name: "account",
  data() {
    return {};
  },
  computed: {
    username() {
      return this.$store.getters.getUserData.username;
    },
  },
  methods: {
    LogoutFunc() {
      let token = localStorage.getItem("token");

      axios
        .options("/api/v1/auth_token/token/logout", {
          headers: { Authorization: "Token " + token },
        })
        .then(() => {
          this.$store.commit("setToken", "");
          this.$store.commit("setAuth", false);
          localStorage.removeItem("token");
          this.DropStorage("settings");
          this.DropStorage("profile");
          this.DropStorage("post-drafts");
        });
    },
    DropStorage(objstore) {
      this.$store.dispatch("DropStorage", objstore);
    },
  },
};
</script>

<style scoped></style>
