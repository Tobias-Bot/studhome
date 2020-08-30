<template>
  <div class="box-with-tools" ref="container" @scroll="LoadNewPosts">
    <div id="top"></div>
    <div v-if="!posts.length" class="loading">
      <div class="spinner-border" role="status"></div>
      <br />
      <span class="loadingText">одну секундочку...</span>
    </div>
    <div v-else ref="container_posts" class="row">
      <!-- <div class="card-columns">
        <post
          v-for="(post, id) in posts"
          :key="id"
          :post="post"
          :post_index="id"
          :topic="'all'"
        ></post>
      </div> -->
      <div class="col-3">
        <template v-for="(post, id) in posts">
          <post
            v-if="id < posts.length / 4 && id >= 0"
            :key="id"
            :post="post"
            :post_index="id"
            :topic="'all'"
          ></post>
        </template>
      </div>
      <div class="col-3">
        <template v-for="(post, id) in posts">
          <post
            v-if="id < (posts.length / 4) * 2 && id >= posts.length / 4"
            :key="id"
            :post="post"
            :post_index="id"
            :topic="'all'"
          ></post>
        </template>
      </div>
      <div class="col-3">
        <template v-for="(post, id) in posts">
          <post
            v-if="id < (posts.length / 4) * 3 && id >= (posts.length / 4) * 2"
            :key="id"
            :post="post"
            :post_index="id"
            :topic="'all'"
          ></post>
        </template>
      </div>
      <div class="col-3">
        <template v-for="(post, id) in posts">
          <post
            v-if="id < (posts.length / 4) * 4 && id >= (posts.length / 4) * 3"
            :key="id"
            :post="post"
            :post_index="id"
            :topic="'all'"
          ></post>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import post from "../../../components/post";

export default {
  components: {
    post,
  },
  data: function() {
    return {
      isWriting: false,
      PostsLoadCount: 12,
      load: true,
      postsCountOld: 0,
    };
  },
  created() {
    let topic = this.$route.params.topic;

    this.PostLoader(topic);
  },
  computed: {
    posts() {
      let elem = this.$refs.container;
      let posts = this.$store.getters.getPosts;
      let hash = this.$store.getters.getHash;

      if (elem && hash) {
        elem.querySelector("#" + hash).scrollIntoView({
          block: "center",
          inline: "center",
          behavior: posts.length < 40 ? "smooth" : "auto",
        });

        this.load && this.$store.commit("setHash", "");
      }

      if (posts.length > this.postsCountOld) {
        () => (this.load = true);
        () => (this.postsCountOld = posts.length);
      }

      return posts;
    },
  },
  methods: {
    LoadNewPosts() {
      let block = this.$refs.container;
      let Hmax =
        block && Math.floor((block.scrollHeight - block.clientHeight) * 0.2);
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
        value: topic,
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
    },
  },
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

.spinner-border {
  width: 4rem;
  height: 4rem;
  color: white;
}
/* #top {
  height: 1vh;
} */
</style>
