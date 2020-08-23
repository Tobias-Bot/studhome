<template>
  <div class="box-with-tools" ref="container" @scroll="LoadNewPosts">
    <div v-if="!posts.length" class="loading">
      <div class="spinner-border" role="status"></div>
      <br />
      <span class="loadingText">ого, сколько тут всего..</span>
    </div>
    <div class="stream" ref="stream">
      <div id="top"></div>
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
    return {
      PostsLoadCount: 10,
      load: true,
      postsCountOld: 0
    };
  },
  created() {
    this.getData();
  },
  mounted() {
    let posts = this.$store.getters.getMyNewsPosts;
    let elem = this.$refs.stream;
    let hash = this.$store.getters.getHash;

    console.log(elem);
    console.log(hash);

    if (elem && hash) {
      elem.querySelector("#" + hash).scrollIntoView({
        block: "center",
        inline: "center",
        behavior: posts.length < 30 ? "smooth" : "auto"
      });

      this.load && this.$store.commit("setHash", "");
    }
  },
  computed: {
    posts() {
      let posts = this.$store.getters.getMyNewsPosts;

      if (posts.length > this.postsCountOld) {
        this.load = true;
        this.postsCountOld = posts.length;
      }

      return posts;
    },
    getDate() {
      let date = new Date();
      let month = date.getMonth();
      let day = date.getDate();
      let year = date.getFullYear();

      if (!month) month++;
      if (String(month).length == 1) month = "0" + month;
      if (String(day).length == 1) day = "0" + day;

      let result = year + "-" + month + "-" + day;

      return result;
    }
  },
  methods: {
    LoadNewPosts() {
      let block = this.$refs.container;
      let Hmax =
        block && Math.floor((block.scrollHeight - block.clientHeight) * 0.6);
      let h = block.scrollTop;

      if (h > Hmax) {
        this.load && this.PostLoader();
        this.load = false;
      } else {
        this.load = true;
      }
    },
    PostLoader() {
      let top = this.posts.length;
      let bottom = top + this.PostsLoadCount;
      let date = this.getDate;

      let data = {
        top,
        bottom,
        date
      };

      this.$store.dispatch("MyNewsPostLoader", data);
    },
    getData() {
      let time = setInterval(() => {
        let username = this.$store.getters.getUserProfile.username;
        
        if (username) {
          clearInterval(time);
          this.PostLoader();
        }
      }, 100);
    }
  }
};
</script>

<style scoped>
.stream {
  width: 40%;
  position: relative;
  left: 45%;
  transform: translateX(-50%);
}

.spinner-border {
  width: 4rem;
  height: 4rem;
  color: white;
}
</style>
