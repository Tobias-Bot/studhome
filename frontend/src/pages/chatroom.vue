<template>
  <div>
    <div id="main_header2">
      <nav class="nav">
        <router-link class="nav-link" to="/rooms/me">
          <span class="tab">
            <i class="fas fa-house-user"></i>
            мои комнаты
          </span>
        </router-link>
        <router-link class="nav-link" to="">
          <span class="tab">
            <i class="fas fa-star"></i>
            избранное
          </span>
        </router-link>
        <router-link class="nav-link" to="">
          <span class="tab">
            <i class="fas fa-compass"></i>
            все комнаты
          </span>
        </router-link>
      </nav>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "chatroom",
  data: function() {
    return {
    };
  },
  methods: {},
};
</script>

<style scoped>
</style>
