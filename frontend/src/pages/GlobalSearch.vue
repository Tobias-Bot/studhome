<template>
  <div class="box" ref="container" @scroll="LoadNewPosts">
    <div class="block">
      <input
        v-model="SearchText"
        class="form-control MainInput"
        placeholder="Что будем искать?"
        @input="setSearchTag"
        @keyup.enter="FindData"
      />
      <button
        class="btn btn-light ClearInputBtn btnMain"
        type="button"
        title="сбросить поиск"
        :hidden="isBlank"
        @click="ClearInput"
      >
        <i class="fas fa-times"></i>
      </button>
    </div>
    <select class="category" ref="CategorySelector">
      <option>публикации</option>
      <option>люди</option>
    </select>
    <div v-if="!Posts.length && !Blogs.length" class="interests">
      <tag v-for="(tag, index) in Interests" :key="index" :text="tag"></tag>
    </div>
    <div class="block">
      <div v-show="this.cat == 'публикации'" ref="content" class="row">
        <!-- <post
          v-for="(post, id) in Posts"
          :key="id"
          :post="post"
          :post_index="id"
          :topic="'search'"
        ></post> -->
        <div class="col-4">
          <template v-for="(post, id) in Posts">
            <post
              :key="id"
              v-if="id < Posts.length / 3 && id >= 0"
              :post="post"
              :post_index="id"
              :topic="'search'"
            ></post>
          </template>
        </div>
        <div class="col-4">
          <template v-for="(post, id) in Posts">
            <post
              :key="id"
              v-if="id < (Posts.length / 3) * 2 && id >= Posts.length / 3"
              :post="post"
              :post_index="id"
              :topic="'search'"
            ></post>
          </template>
        </div>
        <div class="col-4">
          <template v-for="(post, id) in Posts">
            <post
              :key="id"
              v-if="id < (Posts.length / 3) * 3 && id >= (Posts.length / 3) * 2"
              :post="post"
              :post_index="id"
              :topic="'search'"
            ></post>
          </template>
        </div>
      </div>
      <div v-show="this.cat == 'люди'" class="card-columns">
        <blog v-for="(profile, id) in Blogs" :key="id" :blog="profile"></blog>
      </div>
    </div>
  </div>
</template>

<script>
import post from "../components/post";
import tag from "../components/tag";
import blog from "../components/Profile/profileView";

export default {
  components: {
    post,
    tag,
    blog,
  },
  mounted() {
    this.cat = this.$refs.CategorySelector.value;

    // let elem = this.$refs.content;
    // let posts = this.Posts;
    // let hash = this.$store.getters.getHash;

    // console.log(elem);
    // console.log(hash);

    // if (elem && hash && posts) {
    //   elem.querySelector("#" + hash).scrollIntoView({
    //     block: "center",
    //     inline: "center",
    //     behavior: posts.length < 50 ? "smooth" : "auto"
    //   });

    //   this.load && this.$store.commit("setHash", "");
    // }
  },
  data() {
    return {
      SearchText: "",
      postsByInterests: [],
      cat: "",

      PostsLoadCount: 9,
      load: true,
      postsCountOld: 0,
    };
  },
  computed: {
    Posts() {
      () => (this.SearchText = this.$store.getters.getSearchTag);

      let posts = this.$store.getters.getSearchPost;

      this.goToHash(posts);

      if (posts.length > this.postsCountOld) {
        () => (this.load = true);
        () => (this.postsCountOld = posts.length);
      }

      return posts;
    },
    Blogs() {
      return this.$store.getters.getFoundProfiles;
    },
    isBlank() {
      if (this.SearchText || this.Posts.length) {
        return false;
      } else {
        return true;
      }
    },
    SearchTag: {
      get() {
        return this.$store.getters.getSearchTag;
      },
      set(text) {
        this.SearchText = text;
      },
    },
    Interests() {
      let tags = this.$store.getters.getUserProfile.interests;
      let arr = '';

      if (tags) {
        arr = tags.split("|");
        arr.splice(0, 1);
        arr.splice(arr.length - 1, 1);
      }

      return arr;
    },
  },
  methods: {
    goToHash(posts) {
      let elem = this.$refs.content;
      let hash = this.$store.getters.getHash;

      if (hash) {
        let timerId = setInterval(() => {
          elem = this.$refs.content;

          if (elem) {
            elem.querySelector("#" + hash).scrollIntoView({
              block: "center",
              inline: "center",
              behavior: posts.length < 30 ? "smooth" : "auto",
            });

            clearInterval(timerId);
            this.load && this.$store.commit("setHash", "");
          }
        }, 100);
      }
    },
    FindData() {
      let top = this.Posts.length;
      let bottom = top + this.PostsLoadCount;
      let text = this.$store.getters.getSearchTag;

      let data = {
        top,
        bottom,
        text,
      };

      this.cat = this.$refs.CategorySelector.value;

      switch (this.cat) {
        case "публикации":
          this.$store.dispatch("FindData", data);
          break;
        case "люди":
          this.$store.dispatch("FindPeople", data.text);
          break;
      }
    },
    ClearInput() {
      this.$store.commit("setSearchTag", "");
      this.$store.commit("dropFoundProfiles", 0);
      this.$store.commit("dropSearchPost", 0);
      this.SearchText = "";
    },
    LoadNewPosts() {
      let block = this.$refs.container;
      let Hmax =
        block && Math.floor((block.scrollHeight - block.clientHeight) * 0.3);
      let h = block.scrollTop;

      if (h > Hmax) {
        this.load && this.FindData();
        this.load = false;
      } else {
        this.load = true;
      }
    },
    setSearchTag() {
      this.$store.commit("setSearchTag", this.SearchText);
    },
  },
};
</script>

<style scoped>
.box {
  overflow-y: auto;
  overflow-x: hidden;
  padding: 7% 18% 10% 18%;
  height: 100vh;
}

.block {
  position: relative;
  margin: 2% 0 1% 0;
}

.interests {
  position: relative;
  text-align: center;
  margin: 2% 5% 0 5%;
}

.category {
  position: relative;
  left: 0.5%;
  margin-bottom: 2%;
  font-size: 18px;
  font-weight: 500;
  border-radius: 5px;
  border: none;
  background-color: rgba(255, 255, 255, 0.9);
  color: rgba(0, 0, 0, 0.9);
  box-shadow: 0 6px 4px rgba(0, 0, 0, 0.6);
}

.MainInput {
  width: 100%;
  height: 10%;
  border: none;
  outline: none;
  border-radius: 5px;
  padding: 1% 8% 1% 1.5%;
  margin-bottom: 1.5%;
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.8);
  background-color: rgba(0, 0, 0, 0.8);
  font-size: 30px;
  font-weight: 600;
  color: white;
}

.ClearInputBtn {
  height: 70%;
  position: absolute;
  top: 0;
  bottom: 0;
  right: 1%;
  margin: auto 0;
}

.spinner-border {
  width: 4rem;
  height: 4rem;
  color: white;
}
</style>
