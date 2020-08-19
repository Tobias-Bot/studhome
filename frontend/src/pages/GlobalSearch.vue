<template>
  <div class="box">
    <div class="block">
      <input
        v-model="SearchText"
        class="form-control MainInput"
        placeholder="Что будем искать?"
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
    <div v-else class="block">
      <div v-if="this.cat == 'публикации'" class="card-columns">
        <post
          v-for="(post, id) in Posts"
          :key="id"
          :post="post"
          :post_index="id"
          :topic="'search'"
        ></post>
      </div>
      <div v-else-if="this.cat == 'люди'" class="card-columns">
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
    blog
  },
  mounted() {
    this.cat = this.$refs.CategorySelector.value;
  },
  data() {
    return {
      SearchText: "",
      postsByInterests: [],
      cat: ""
    };
  },
  computed: {
    Posts() {
      return this.$store.getters.getSearchPost;
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
      }
    },
    Interests() {
      let tags = this.$store.getters.getUserProfile.interests;
      if (tags) {
        let arr = tags.split("|");
        arr.splice(0, 1);
        arr.splice(arr.length - 1, 1);

        return arr;
      }
    }
  },
  methods: {
    FindData() {
      this.cat = this.$refs.CategorySelector.value;

      if (this.cat == "публикации") {
        let text = `|${this.SearchText}|`;
        this.$store.dispatch("FindData", text);
      }
      if (this.cat == "люди") {
        let text = this.SearchText;
        this.$store.dispatch("FindPeople", text);
      }
    },
    ClearInput() {
      this.$store.commit("setSearchTag", "");
      this.$store.commit("dropFoundProfiles", 0);
      this.$store.commit("dropSearchPost", 0);
      this.SearchText = "";
    }
  }
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
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 2%;
  font-size: 18px;
  font-weight: 500;
  border-radius: 5px;
  border: none;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
}

.MainInput {
  width: 100%;
  height: 10%;
  border: none;
  outline: none;
  border-radius: 5px;
  padding: 1% 8% 1% 1.5%;
  margin-bottom: 3%;
  box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.8);
  background-color: rgba(0, 0, 0, 0.9);
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
</style>
