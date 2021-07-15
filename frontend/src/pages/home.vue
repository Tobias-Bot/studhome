<template>
  <div>
    <div id="main_header2">
      <nav class="nav">
        <router-link
          v-if="username"
          class="nav-link"
          :to="{
            name: 'profile',
            params: { username }
          }"
        >
          <span class="tab">
            <i class="fas fa-user"></i>
            профиль
          </span>
        </router-link>
        <router-link class="nav-link" to="/home/bookmarks">
          <span class="tab">
            <i class="fas fa-bookmark"></i>
            закладки
          </span>
        </router-link>
        <router-link class="nav-link" to="/home/settings">
          <span class="tab">
            <i class="fas fa-sliders-h"></i>
            настройки
          </span>
        </router-link>
      </nav>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "home",
  computed: {
    username() {
      return this.$store.getters.getUserData.username;
    }
  },
  methods: {
  }
};
</script>

<style scoped></style>
