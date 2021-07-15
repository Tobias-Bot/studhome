<template>
  <div class="box-with-tools">
    <div class="card-columns">
      <post
        v-for="(post, id) in posts"
        :key="id"
        :post="post"
        :post_index="id"
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
    return {
    };
  },
  computed: {
    posts() {
      return this.$store.getters.getPopularPosts;
    }
  },
  methods: {}
};
</script>

<style scoped>
/* 2 колонки на sm */
@media (min-width: 576px) {
  .card-columns {
    column-count: 2;
  }
}
/* 3 колонки на md */
@media (min-width: 768px) {
  .card-columns {
    column-count: 3;
  }
}
/* 4 колонки на lg и xl */
@media (min-width: 992px) {
  .card-columns {
    column-count: 4;
  }
}
</style>
