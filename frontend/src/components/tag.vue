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
      let top = 0;
      let bottom = top + 10;

      let data = {
        top,
        bottom,
      };

      data.text = this.text;

      this.$store.commit("setSearchTag", data.text);
      this.$store.dispatch("FindData", data);
    }
  }
};
</script>

<style scoped>

</style>
