<template>
  <router-link to="/search">
    <span
      class="tag"
      @click="loadPostsByTag"
    >
      {{ this.text }}
    </span>
  </router-link>
</template>

<script>
export default {
  props: ["text"],
  data: function() {
    return {};
  },
  computed: {},
  methods: {
    loadPostsByTag() {
      this.$store.dispatch("FindData", "|" + this.text + "|");
    }
  }
};
</script>

<style scoped>

</style>
