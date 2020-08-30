<template>
  <div class="card" :id="'post-' + post_index">
    <div class="card-header">
      <router-link
        style="text-decoration: none;"
        :to="{ name: 'profile', params: { username: post.username } }"
      >
        <span class="username" @click="LoadProfile()">{{ post.username }}</span>
      </router-link>
      <template v-if="post.username !== UserData.username">
        <span
          v-if="!inUserSubs"
          class="btnSubscribe"
          title="подписаться"
          @click="Subscribe(post.username, UserData.username)"
          ><i class="fas fa-plus-circle"></i
        ></span>
        <span
          v-else
          class="btnSubscribe"
          title="отписаться"
          @click="unSubscribe(post.username, UserData.username)"
          ><i class="far fa-times-circle"></i
        ></span>
      </template>
      <div class="post_header">
        <div class="btn-group" role="group">
          <router-link
            :to="{
              name: 'post',
              params: { post_id: post.id, post: post, post_index: post_index },
            }"
            style="text-decoration: none; color: white; font-weight: 500;"
          >
            <button class="btn btn-dark btn-sm" @click="addUserView(post.id)">
              читать
            </button>
          </router-link>
          <template v-if="post.user === UserData.id">
            <router-link
              v-if="isEditable"
              :to="{ name: 'CreatePost', params: { editMode: true, post } }"
              type="button"
              title="редактировать"
              class="btn btn-light btn-sm"
            >
              <i class="fas fa-edit"></i>
            </router-link>
            <button
              type="button"
              title="удалить пост"
              class="btn btn-light btn-sm"
              @click="DeletePost(post_index, post.id, topic)"
            >
              <i class="fas fa-times"></i>
            </button>
          </template>
          <template v-else>
            <button
              type="button"
              class="btn btn-light btn-sm"
              title="добавить в закладки"
              @click="
                !inUserBookmarks ? addToBookmarks() : deleteFromBookmarks()
              "
            >
              <i v-if="!inUserBookmarks" class="far fa-bookmark"></i>
              <i v-else class="fas fa-bookmark"></i>
            </button>
          </template>
        </div>
      </div>
    </div>
    <div class="card-body">
      <template v-if="post.title">
        <h4 style="margin-bottom: 5%; color: #323232">{{ post.title }}</h4>
      </template>
      <NoteText
        v-if="post.text.length"
        :post="post"
        :index="post_index"
      ></NoteText>
      <template v-if="post.images[0]">
        <pic
          :item="post.images[0]"
          :post_index="post_index"
          :username="post.username"
        ></pic>
      </template>
      <template v-if="post.tags.length > 2">
        <hr />
        <template v-for="(tag, index) in tags">
          <tag
            v-if="index < TagsViewCount"
            :key="index"
            :text="tag"
            :textColor="post.text_color"
            :noteColor="post.note_color"
          ></tag>
        </template>
      </template>
    </div>
    <div class="card-footer">
      <span class="views"><i class="far fa-eye"></i> {{ post.views }}</span>
      <share-panel :post_index="post_index" :post_id="post.id"></share-panel>
    </div>
  </div>
</template>

<script>
import tag from "./tag";
import SharePanel from "./SharePanel";
import pic from "./pic";
import NoteText from "./NoteText";

export default {
  components: {
    tag,
    SharePanel,
    pic,
    NoteText,
  },
  props: ["post", "post_index", "topic"],
  data: function() {
    return {
      TagsViewCount: 5,
    };
  },
  computed: {
    UserData() {
      return this.$store.getters.getUserData;
    },
    tags() {
      let tags = this.post.tags
        .substring(1, this.post.tags.length - 1)
        .split("|");
      return tags;
    },
    inUserSubs() {
      let names = this.$store.getters.getUserProfile.subs_profiles;
      if (names && names.indexOf(this.post.username) == -1) return false;
      else return true;
    },
    inUserBookmarks() {
      let ids = this.$store.getters.getUserBookmarks;
      let post_id = this.post.id;
      let result = false;

      for (let post of ids) {
        if (post.id == post_id) return true;
      }

      return result;
    },
    PostDate() {
      let date = "";

      if (this.post.date) {
        date = this.post.date
          .substring(0, 10)
          .split("-")
          .reverse()
          .join(".");
      }

      return date;
    },
    isEditable() {
      let day = parseInt(this.PostDate.substring(0, 2));
      let month = parseInt(this.PostDate.substring(3, 5));
      let year = parseInt(this.PostDate.substring(6, 10));
      let date = new Date();
      let result = true;

      if (
        date.getDate() - day > 0 ||
        date.getMonth() + 1 - month > 0 ||
        date.getFullYear() - year > 0
      ) {
        result = false;
      }

      return result;
    },
  },
  methods: {
    DeletePost(post_index, post_id, topic) {
      this.$store.dispatch("deletePostFromServer", {
        post_index,
        post_id,
        topic,
      });
    },
    Subscribe(sub_user, username) {
      let token = localStorage.getItem("token");

      let data = {
        token,
        q: sub_user,
        me: username,
      };

      this.$store.dispatch("addUserProfileInSubs", data);
    },
    unSubscribe(sub_user, username) {
      let token = localStorage.getItem("token");

      let data = {
        token,
        q: sub_user,
        me: username,
      };

      this.$store.dispatch("deleteUserProfileFromSubs", data);
    },
    addToBookmarks() {
      let token = localStorage.getItem("token");
      let username = this.UserData.username;
      let post_id = this.post.id;
      let domain = this.$store.getters.getDomain;

      axios.get(
        `${domain}/api/v1/news/post/bookmarks_add/?q=${post_id}&me=${username}`,
        {
          headers: { Authorization: "Token " + token },
        }
      );

      this.$store.commit("addUserBookmark", this.post);
      this.saveToDB(this.$store.getters.getUserBookmarks);
    },
    saveToDB(objs) {
      var openRequest = indexedDB.open("profile", 1);

      openRequest.onupgradeneeded = () => {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains("profile")) {
          DB.createObjectStore("profile");
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
      };

      openRequest.onsuccess = () => {
        var DB = openRequest.result;

        let tx = DB.transaction("profile", "readwrite");
        let store = tx.objectStore("profile");

        store.put(JSON.stringify(objs), "bookmarks");
      };
    },
    deleteFromBookmarks() {
      let token = localStorage.getItem("token");
      let username = this.UserData.username;
      let post_id = this.post.id;
      let MarkedPosts = this.$store.getters.getUserBookmarks;
      let domain = this.$store.getters.getDomain;

      axios
        .get(
          `${domain}/api/v1/news/post/bookmarks_delete/?q=${post_id}&me=${username}`,
          {
            headers: { Authorization: "Token " + token },
          }
        )
        .then(() => {
          let index = 0;

          for (let post of MarkedPosts) {
            if (post.id == post_id) {
              break;
            }

            index++;
          }

          MarkedPosts.splice(index, 1);

          this.$store.commit("setUserBookmarks", MarkedPosts);
          this.saveToDB(MarkedPosts);
        });
    },
    addUserView(post_id) {
      let post_index = this.post_index;
      let data = {
        post_id,
        post_index,
      };

      this.$store.dispatch("addUserView", data);
    },
    LoadProfile() {
      this.$store.commit("dropUserPosts");
      this.$store.commit("dropUserSubs");
      this.$store.commit("setProfileTab", "description");
    },
  },
};
</script>

<style scoped>
.card {
  margin-bottom: 8%;
}

.post_header {
  position: absolute;
  right: 20px;
  top: 6px;
  border-radius: 10px;
  height: auto;
  text-align: right;
  display: inline-block;
}
</style>
