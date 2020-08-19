<template>
  <div class="box-with-tools" ref="container" @scroll="LoadNewPosts">
    <div v-if="!posts.length" class="loading">
      <div class="spinner-border" role="status"></div>
      <br />
      <span class="loadingText">одну секундочку...</span>
    </div>
    <div v-else class="card-columns" ref="container_posts">
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
      PostsLoadCount: 15,
      load: true,
      postsCountOld: 0
    };
  },
  created() {
    let topic = this.$route.params.topic;

    this.PostLoader(topic);
  },
  computed: {
    posts() {
      let elem = this.$refs.container_posts;
      let posts = this.$store.getters.getPosts;
      let hash = this.$store.getters.getHash;

      if (elem && hash) {
        elem.querySelector("#" + hash).scrollIntoView({
          block: "center",
          inline: "center",
          behavior: "smooth"
        });
      }

      if (posts.length > this.postsCountOld) {
        this.load = true;
        this.postsCountOld = posts.length;
      }

      return posts;
    },
  },
  methods: {
    LoadNewPosts() {
      let block = this.$refs.container;
      let Hmax = Math.floor((block.scrollHeight - block.clientHeight) * 0.3);
      let h = block.scrollTop;
      let topic = this.$route.params.topic;

      if (h > Hmax) {
        this.load && this.PostLoader(topic);
        this.load = false;
      } else {
        this.load = true;
      }
    },
    PostLoader(topic) {
      let top = this.posts.length;
      let bottom = top + this.PostsLoadCount;

      let data = {
        top,
        bottom,
        value: topic
      };

      switch (topic) {
        case "new":
          this.$store.dispatch("AllPostLoader", data);
          break;
        case "popular":
          this.$store.dispatch("AllPopularPostLoader", data);
          break;
        case "note":
          this.$store.dispatch("AllPostByTypeLoader", data);
          break;
        case "photo":
          this.$store.dispatch("AllPostByTypeLoader", data);
          break;
        case "marks":
          this.$store.dispatch("PostsByMarksLoader", data);
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

.loading {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 45%;
  text-align: center;
}

.loadingText {
  color: white;
  font-size: 22px;
  font-weight: 500;
}

.spinner-border {
  width: 4rem;
  height: 4rem;
  color: white;
}
</style>
