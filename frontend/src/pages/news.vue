<template>
  <div>
    <div id="main_header2">
      <nav class="nav">
        <router-link class="nav-link" to="/news/me">
          <span class="tab" @click="MyNewsPostLoader">
            <i class="fas fa-poll-h"></i>
            моя лента
          </span>
        </router-link>
        <router-link
          class="nav-link"
          :to="{
            name: 'AllPosts',
            params: { topic: 'new' }
          }"
        >
          <span class="tab" @click="PostLoader('new')">
            <i class="fas fa-rss"></i>
            свежее
          </span>
        </router-link>
        <router-link
          class="nav-link"
          :to="{
            name: 'AllPosts',
            params: { topic: 'popular' }
          }"
        >
          <span class="tab" @click="PostLoader('popular')">
            <i class="fas fa-fire-alt"></i>
            популярное
          </span>
        </router-link>
        <router-link
          class="nav-link"
          :to="{
            name: 'AllPosts',
            params: { topic: 'note' }
          }"
        >
          <span class="tab" @click="PostLoader('note')">
            <i class="fas fa-sticky-note"></i>
            текст
          </span>
        </router-link>
        <router-link
          class="nav-link"
          :to="{
            name: 'AllPosts',
            params: { topic: 'photo' }
          }"
        >
          <span class="tab" @click="PostLoader('photo')">
            <i class="fas fa-images"></i>
            фото
          </span>
        </router-link>
        <span
          class="nav-link tab"
          @mouseover="isMarkSection = true"
          @mouseout="isMarkSection = false"
        >
          <i class="fas fa-tags"></i>
          метки
          <span class="sub_index" v-if="postMarksCount">{{
            postMarksCount
          }}</span>
          <div v-show="isMarkSection" class="postsMarksSection">
            <postMark :name="'книга'" :index="0"></postMark>
            <postMark :name="'вопрос'" :index="1"></postMark>
            <postMark :name="'видео'" :index="2"></postMark>
          </div>
        </span>
      </nav>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import postMark from "../components/News/postMark";

export default {
  name: "news",
  components: {
    postMark
  },
  data: function() {
    return {
      isMarkSection: false,
      PostsLoadCount: 15
    };
  },
  beforeDestroy() {
    this.$store.commit("dropPostMarks");
  },
  computed: {
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
    },
    postMarksCount() {
      return this.$store.getters.getPostMarks.length;
    }
  },
  methods: {
    MyNewsPostLoader() {
      let token = this.$store.getters.getToken;
      let username = this.$store.getters.getUserData.username;

      axios
        .get(
          "http://127.0.0.1:8000/api/v1/news/post/mysubs/all/?me=" +
            username +
            "&d=" +
            this.getDate,
          {
            headers: { Authorization: "Token " + token }
          }
        )
        .then(response => {
          let posts = response.data;
          this.$store.commit("setMyNewsPost", posts);
        })
        .catch(function(e) {
          console.log(e);
        });
    },
    PostLoader(topic) {
      let top = 0;
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
      }
    }
  }
};
</script>

<style scoped>
.postsMarksSection {
  width: 100%;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
  padding: 15% 6% 3% 6%;
  background: white;
  border-radius: 2px 2px 5px 5px;
  color: white;
  text-align: center;
  margin: 4% 0 0 0;
  font-size: 16px;
  font-weight: 600;
  text-shadow: none;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.8);
}

.sub_index {
  position: absolute;
  right: 3%;
  font-size: 14px;
  font-weight: 500;
  color: white;
  opacity: 0.9;
}
</style>
