<template>
  <div class="box-with-tools" ref="container" @scroll="LoadNewPosts">
    <div class="card-columns">
      <post
        v-for="(post, id) in posts"
        :key="id"
        :post="post"
        :post_index="id"
        :topic="'all'"
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
      isWriting: false,
      PostsLoadCount: 10,
    };
  },
  created() {
    let topic = this.$route.params.topic;
    this.PostLoader(topic);
  },
  computed: {
    posts() {
      return this.$store.getters.getPosts;
    }
  },
  methods: {
    LoadNewPosts() {
      let block = this.$refs.container;
      let Hmax = block.scrollHeight - block.clientHeight;
      let h = block.scrollTop;
      let topic = this.$route.params.topic;

      if (h == Hmax) {
        this.PostLoader(topic);
      }
    },
    PostLoader(topic) {
      let top = this.posts.length;
      let bottom = top + this.PostsLoadCount;

      let data = {
        top,
        bottom
      }

      switch (topic) {
        case "new":
          this.$store.dispatch('AllPostLoader', data);
          break;
      }
    }
  }
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
