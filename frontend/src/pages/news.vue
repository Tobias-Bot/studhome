<template>
  <div>
    <div id="main_header2">
      <nav class="nav">
        <router-link class="nav-link" to="/news/me">
          <span class="tab" @click="PostLoader('me')">
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
        <span
          class="nav-link tab"
          @mouseover="isTypeSection = true"
          @mouseout="isTypeSection = false"
        >
          <i class="fas fa-icons"></i>
          публикации
          <span class="sub_index" v-if="postTypesCount">{{
            postTypesCount
          }}</span>
          <div v-show="isTypeSection" class="postsMarksSection">
            <postType :name="'заметка'" :index="0" @loadPostsByTypes="PostLoader('type')"></postType>
            <postType :name="'текст'" :index="1" @loadPostsByTypes="PostLoader('type')"></postType>
            <postType :name="'фото'" :index="2" @loadPostsByTypes="PostLoader('type')"></postType>
            <postType :name="'видео'" :index="3" @loadPostsByTypes="PostLoader('type')"></postType>
          </div>
        </span>
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
            <postMark :name="'вопрос'" :index="0" @loadPostsByMarks="PostLoader('marks')"></postMark>
          </div>
        </span>
      </nav>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import postMark from "../components/News/postMark";
import postType from "../components/News/postType";

export default {
  name: "news",
  components: {
    postMark,
    postType
  },
  data: function() {
    return {
      isMarkSection: false,
      isTypeSection: false,
      PostsLoadCount: 15
    };
  },
  beforeDestroy() {
    this.$store.commit("dropPostMarks");
  },
  computed: {
    postMarksCount() {
      return this.$store.getters.getPostMarks.length;
    },
    postTypesCount() {
      return this.$store.getters.getPostTypes.length;
    }
  },
  methods: {
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
        case "type":
          this.$store.dispatch("AllPostByTypeLoader", data);
          break;
        case "marks":
          this.$store.dispatch("PostsByMarksLoader", data);
          break;
      }

      this.postMarksCount && (topic !== 'marks') && this.$store.commit('dropPostMarks');
      this.postTypesCount && (topic !== 'type') && this.$store.commit('dropPostTypes');

      this.$store.commit('setHash', 'top');
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
  z-index: 5;
  padding: 12% 6% 3% 6%;
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
