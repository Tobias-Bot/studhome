<template>
  <div class="box-with-tools">
    <div class="stream">
      <post
        v-for="(post, id) in posts"
        :key="id"
        :post="post"
        :post_index="id"
        :topic="'mynews'"
      ></post>
    </div>
  </div>
</template>

<script>
import post from "../../../components/post";

export default {
  components: {
    post
  },
  data: function() {
    return {};
  },
  computed: {
    posts() {
      return this.$store.getters.getMyNewsPosts;
    }
  },
  methods: {}
};
</script>

<style scoped>
.stream {
  width: 40%;
  position: relative;
  left: 45%;
  transform: translateX(-50%);
}
</style>
