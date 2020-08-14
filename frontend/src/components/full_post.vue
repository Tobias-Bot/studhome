<template>
  <div class="box">
    <div class="row">
      <div class="col-2">
        <div class="card">
          <div class="card-header">
            <div class="postInfo">
              <i class="far fa-calendar"></i>
              <template v-if="getDate == PostDate">
                сегодня в {{ PostTime }}
              </template>
              <template v-else> {{ PostDate }} в {{ PostTime }} </template>
            </div>
          </div>
          <div v-if="CurrPost.username" class="card-body">
            <router-link
              class="username"
              style="text-align: center;"
              :to="{ name: 'profile', params: { username: CurrPost.username } }"
              ><h5>{{ CurrPost.username }}</h5></router-link
            >
            <template v-if="CurrPost.username !== UserData.username">
              <button
                v-if="!inUserSubs"
                class="btn btn-outline-dark btnMain"
                type="button"
                style="width: 100%;"
                @click="Subscribe(CurrPost.username, UserData.username)"
              >
                читать
              </button>
              <button
                v-else
                class="btn btn-dark btnMain"
                type="button"
                style="width: 100%;"
                @click="unSubscribe(CurrPost.username, UserData.username)"
              >
                отписаться
              </button>
            </template>
            <template v-else>
              <router-link
                :to="{
                  name: 'CreatePost',
                  params: { editMode: true, post: CurrPost }
                }"
                class="btn btn-light btnMain"
                type="button"
                style="width: 100%;"
              >
                изменить
              </router-link>
              <button
                class="btn btn-light btnMain"
                type="button"
                style="width: 100%;"
                @click="
                  $store.dispatch('deletePostFromServer', {
                    post_id: CurrPost.id
                  })
                "
              >
                удалить
              </button>
            </template>
          </div>
        </div>
      </div>
      <div class="col-6">
        <div class="card">
          <div class="card-body">
            <template v-if="CurrPost.title">
              <h4 style="margin: 0 0 4% 2%;">{{ CurrPost.title }}</h4>
            </template>
            <div
              v-if="CurrPost.text"
              class="post"
              :style="'background-color:' + CurrPost.note_color"
            >
              <template
                v-if="
                  CurrPost.text &&
                    (CurrPost.text.includes('</b>') ||
                      CurrPost.text.includes('</i>') ||
                      CurrPost.text.includes('</u>') ||
                      CurrPost.text.includes('<br>') ||
                      CurrPost.text.includes('</strike>') ||
                      CurrPost.text.includes('</ul>') ||
                      CurrPost.text.includes('</ol>') ||
                      CurrPost.text.includes('</span>')) &&
                    !CurrPost.text.includes('</script>')
                "
              >
                <span
                  v-html="CurrPost.text"
                  :style="'color:' + CurrPost.text_color + ';'"
                ></span>
              </template>
              <template v-else>
                <span :style="'color:' + CurrPost.text_color + ';'">
                  {{ CurrPost.text }}
                </span>
              </template>
            </div>
            <template v-if="CurrPost.images">
              <template v-if="CurrPost.images.length <= 3">
                <template v-for="img in CurrPost.images">
                  <pic :item="img" :username="CurrPost.username"></pic>
                </template>
              </template>
              <template v-else>
                <div class="card-columns">
                  <template v-for="img in CurrPost.images">
                    <pic :item="img" :username="CurrPost.username"></pic>
                  </template>
                </div>
              </template>
            </template>
          </div>
          <div class="card-footer">
            <span class="views">
              <i class="far fa-eye"></i>
              {{ CurrPost.views }}
            </span>
            <share-panel
              :post_index="post_index"
              :post_id="CurrPost.id"
              :text="true"
            ></share-panel>
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <h5 v-if="CurrComms.length">
              Комментарии: {{ CurrPost.comments_count }}
            </h5>
          </div>
          <div class="card-body">
            <template v-if="CurrComms.length">
              <comment
                v-for="(comm, id) in CurrComms"
                :key="id"
                :index="id"
                :post_id="CurrPost.id"
                :args="comm"
                :mates="CurrComms"
              ></comment>
            </template>
            <template v-else>
              <div style="text-align: center; width: 100%; opacity: 0.8;">
                Еще никто не отвечал. Будь первым!
              </div>
            </template>
          </div>
        </div>
      </div>
      <div class="col-4">
        <div class="apps">
          <div v-if="CurrPost.video_url" class="card card_video">
            <div class="card-header">
              <h5>видео</h5>
            </div>
            <div class="card-body">
              <iframe
                class="video"
                :src="video_url"
                frameborder="0"
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              ></iframe>
            </div>
          </div>
          <!-- <div v-if="CurrPost.docs && CurrPost.docs[0]" class="card">
            <div class="card-header">
              файлы
            </div>
            <div class="card-body"></div>
          </div> -->
          <div v-if="tags" class="card">
            <div class="card-header">
              <h5>облако тегов</h5>
            </div>
            <div class="card-body">
              <tag v-for="(tag, index) in tags" :key="index" :text="tag"></tag>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import comment from "./comment";
import SharePanel from "./SharePanel";
import pic from "./pic";
import tag from "./tag";
import scrollbar from "./scrollbar";

var Cookies = localStorage;
var token = Cookies.getItem("token");

export default {
  components: {
    comment,
    SharePanel,
    pic,
    tag,
    scrollbar
  },
  data: function() {
    return {
      showLink: false
    };
  },
  computed: {
    UserData() {
      return this.$store.getters.getUserData;
    },
    post_index() {
      return this.$route.params.post_index;
    },
    video_url() {
      return (
        "https://www.youtube-nocookie.com/embed/" +
        this.CurrPost.video_url.slice(32)
      );
    },
    CurrPost() {
      return this.$store.getters.getCurrentPost;
    },
    CurrComms() {
      return this.$store.getters.getCurrentComms;
    },
    tags() {
      if (this.CurrPost.tags) {
        let tags = this.CurrPost.tags.split("|");
        tags.splice(0, 1);
        tags.splice(tags.length - 1, 1);
        if (tags.length > 1) return tags;
      }
    },
    getDate() {
      let date = new Date();
      let month = date.getMonth() + 1;
      let day = date.getDate();
      let year = date.getFullYear();

      if (String(month).length == 1) month = "0" + month;
      if (String(day).length == 1) day = "0" + day;

      let result = day + "." + month + "." + year;

      return result;
    },
    PostDate() {
      if (this.CurrPost.date) {
        let date = this.CurrPost.date
          .substring(0, 10)
          .split("-")
          .reverse()
          .join(".");

        return date;
      }
    },
    PostTime() {
      if (this.CurrPost.date) {
        let date = this.CurrPost.date.substring(11, 16);
        return date;
      }
    },
    inUserSubs() {
      let names = this.$store.getters.getUserProfile.subs_profiles;
      if (names && names.indexOf(this.CurrPost.username) == -1) return false;
      else return true;
    }
  },
  created() {
    let posts = this.$store.getters.getPosts;
    let myNewsPosts = this.$store.getters.getMyNewsPosts;
    let userPosts = this.$store.getters.getUserPosts;
    let popularPosts = this.$store.getters.getPopularPosts;
    let textPosts = this.$store.getters.getTextPosts;
    let photoPosts = this.$store.getters.getPhotoPosts;
    let searchPosts = this.$store.getters.getSearchPost;
    let post_id = this.$route.params.post_id;
    let post = this.$route.params.post;

    if (
      post &&
      (posts.length ||
        userPosts.length ||
        myNewsPosts.length ||
        popularPosts.length ||
        textPosts.length ||
        searchPosts.length ||
        photoPosts.length)
    ) {
      this.$store.commit("setCurrentPost", post);
      this.CommentsLoader(post_id);
    } else {
      if (!post && !this.CurrPost.id)
        axios
          .get("http://127.0.0.1:8000/api/v1/news/post/" + post_id + "/", {
            headers: { Authorization: "Token " + token }
          })
          .then(response => {
            let post = response.data[0];
            this.$store.commit("setCurrentPost", post);
            this.CommentsLoader(post.id);
          })
          .catch(function(e) {
            console.log(e);
          });
    }
  },
  methods: {
    CommentsLoader(post_id) {
      let domain = this.$store.getters.getDomain;

      if (this.CurrPost.comments_count) {
        axios
          .get(`${domain}/api/v1/news/post/${post_id}/comment/list/`, {
            headers: { Authorization: "Token " + token }
          })
          .then(response => {
            this.$store.commit("setCurrentComms", response.data);
          })
          .catch(function(e) {
            console.log(e);
          });
      } else {
        this.$store.commit("setCurrentComms", []);
      }
    },
    Subscribe(sub_user, username) {
      let token = localStorage.getItem("token");

      let data = {
        token,
        q: sub_user,
        me: username
      };

      this.$store.dispatch("addUserProfileInSubs", data);
    },
    unSubscribe(sub_user, username) {
      let token = localStorage.getItem("token");

      let data = {
        token,
        q: sub_user,
        me: username
      };

      this.$store.dispatch("deleteUserProfileFromSubs", data);
    }
  }
};
</script>

<style scoped>
.card {
  margin-bottom: 6%;
}

.card_video {
  background-color: #1e1e1e;
  color: white;
}

.post {
  max-height: 70vh;
  overflow-y: auto;
  overflow-x: hidden;
  width: 100%;
  padding: 4% 4% 12% 4%;
  background-color: white;
  color: rgba(0, 0, 0, 0.8);
  line-height: 1.6;
  font-size: 18px;
  font-weight: 450;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
  border-radius: 3px;
  text-align: left;
}

.video {
  width: 100%;
  height: 29.5vh;
  box-shadow: 0px 1px 12px black;
  border-radius: 8px;
}

.postInfo {
  width: 100%;
  font-size: 15px;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.7);
  font-style: italic;
}
</style>
