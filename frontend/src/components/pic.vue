<template>
<div class="wrapper">
  <router-link
    :to="{
      name: 'pic',
      params: { post_id: item.post, pic_id: item.id, pic: item, post_index, username }
    }"
    style="text-decoration: none;"
  >
    <img
      :src="domain + item.image"
      class="image"
      alt="image"
      @click="$store.commit('setHash', 'post-' + post_index);"
    />
  </router-link>
</div>
</template>

<script>
export default {
  name: "pic",
  props: ["item", "post_index", "username"],
  data: function() {
    return {};
  },
  computed: {
    domain() {
      return this.$store.getters.getDomain;
    }
  },
  methods: {}
};
</script>

<style scoped>
.wrapper {
  width: 100%;
  height: auto;
  display: inline-block;
  position: relative;
  padding: 3% 0% 2% 0%;
}

.image {
  width: 100%;
  height: auto;
  z-index: 1;
  transition: 0.1s all;
  box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.6);
  position: relative;
  border-radius: 4px;
  transition: 0.2s all;
}
.image:hover {
  transform: rotate(-2deg);
  cursor: pointer;
}
</style>
