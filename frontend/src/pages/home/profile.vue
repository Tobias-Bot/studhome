<template>
  <div class="box" ref="container" @scroll="LoadNewPosts">
    <div class="body">
      <div class="row">
        <div class="col-2">
          <img
            v-if="Profile.avatar"
            class="avatar"
            :src="Profile.avatar"
            alt="avatar"
          />
          <br />
          <button
            class="btn btn-light btnMain profileTab"
            type="button"
            @click="setTab('description')"
          >
            описание
          </button>
          <button
            v-if="Profile.posts_count"
            class="btn btn-light btnMain profileTab"
            type="button"
            @click="
              LoadUserPosts();
              setTab('posts');
            "
          >
            записи
          </button>
          <a
            v-if="Profile.subs_profiles && Profile.subs_profiles.length > 1"
            class="btn btn-light btnMain profileTab"
            type="button"
            @click="
              LoadUserSubsProfiles();
              setTab('blogs');
            "
            >подписки</a
          >
          <button
            v-if="Profile.contacts"
            class="btn btn-light btnMain profileTab"
            type="button"
            @click="setTab('contacts')"
          >
            контакты
          </button>
        </div>
        <div class="col-8">
          <span class="username"
            >{{ Profile.username }}
            <span class="readersCount"
              >читают: {{ Profile.readers }}</span
            ></span
          >
          <div v-show="ProfileTab === 'description'" class="block">
            <div class="card">
              <div class="card-body">
                <template v-if="Profile.status">
                  <span class="status">{{ Profile.status }}</span>
                  <br />
                  <br />
                </template>
                <div class="bio">
                  <template v-if="Profile.bio">
                    <span class="hint" style="text-align: left;">Обо мне</span>
                    {{ Profile.bio }}
                    <hr />
                  </template>
                  <template v-if="Profile.school">
                    <span
                      v-if="Profile.school"
                      class="hint"
                      style="text-align: left;"
                      >Школа/универ</span
                    >
                    {{ Profile.school }}
                    <hr />
                  </template>
                  <template v-if="Profile.interests.length > 2">
                    <span class="hint" style="text-align: left;">Интересы</span>
                    <tag
                      v-for="(tag, i) in userInterests"
                      :key="tag + i"
                      :text="tag"
                    ></tag>
                  </template>
                </div>
              </div>
            </div>
          </div>
          <template v-if="Profile.posts_count">
            <div v-show="ProfileTab === 'posts'" class="block">
              <div class="infoBar">
                записи: {{ Profile.posts_count }}
                <template v-if="isLoading">
                  <div
                    class="spinner-border spinner-border-sm"
                    role="status"
                  ></div>
                </template>
              </div>
              <div ref="container_posts" class="row">
                <!-- <post
                  v-for="(post, id) in UserPosts"
                  :key="id"
                  :post="post"
                  :post_index="id"
                  :topic="'profile'"
                ></post> -->
                <div class="col-6">
                  <post
                    v-for="(post, id) in UserPosts"
                    :key="id"
                    v-if="id % 2 == 0"
                    :post="post"
                    :post_index="id"
                    :topic="'profile'"
                  ></post>
                </div>
                <div class="col-6">
                  <post
                    v-for="(post, id) in UserPosts"
                    :key="id"
                    v-if="id % 2 !== 0"
                    :post="post"
                    :post_index="id"
                    :topic="'profile'"
                  ></post>
                </div>
              </div>
            </div>
          </template>
          <template
            v-if="Profile.subs_profiles && Profile.subs_profiles.length > 1"
          >
            <div v-show="ProfileTab === 'blogs'" class="block">
              <div class="infoBar">
                подписки: {{ UserSubs.length }}
                <template v-if="isLoading">
                  <div
                    class="spinner-border spinner-border-sm"
                    role="status"
                  ></div>
                </template>
              </div>
              <div class="card-columns">
                <blog
                  v-for="(blog, id) in UserSubs"
                  :key="id"
                  :blog="blog"
                ></blog>
              </div>
            </div>
          </template>
          <template v-if="Profile.contacts">
            <div v-show="ProfileTab === 'contacts'" class="block">
              <template v-for="contact in Profile.contacts.split('|')">
                <a
                  v-if="contact.indexOf('instagram.com/') > -1"
                  class="contact"
                  :href="contact"
                  target="_blank"
                >
                  <i class="fab fa-instagram-square"></i>
                  {{ contact.substring(8) }}
                </a>
                <a
                  v-if="contact.indexOf('vk.com/') > -1"
                  class="contact"
                  :href="contact"
                  target="_blank"
                >
                  <i class="fab fa-vk"></i>
                  {{ contact.substring(8) }}
                </a>
                <a
                  v-if="contact.indexOf('youtube.com/') > -1"
                  class="contact"
                  :href="contact"
                  target="_blank"
                >
                  <i class="fab fa-youtube"></i>
                  {{ contact.substring(8) }}
                </a>
                <br />
              </template>
            </div>
          </template>
        </div>
        <div class="col">
          <profileTools
            :profile="Profile"
            :userInterests="userInterests"
          ></profileTools>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import post from "../../components/post";
import tag from "../../components/tag";
import profileTools from "../../components/Profile/profileTools";
import blog from "../../components/Profile/profileView";

export default {
  components: {
    post,
    profileTools,
    tag,
    blog
  },
  data() {
    return {
      isLoading: false,
      PostsLoadCount: 8,
      load: true,
      postsCountOld: 0
    };
  },
  mounted() {
    let elem = this.$refs.container_posts;
    let posts = this.$store.getters.getUserPosts;
    let hash = this.$store.getters.getHash;

    if (elem && hash) {
      elem.querySelector("#" + hash).scrollIntoView({
        block: "center",
        inline: "center",
        behavior: posts.length < 30 ? "smooth" : "auto"
      });
    }
  },
  computed: {
    Profile() {
      if (!this.isAdmin) return this.$store.getters.getCurrProfile;
      else return this.$store.getters.getUserProfile;
    },
    UserProfile() {
      return this.$store.getters.getUserProfile;
    },
    UserData() {
      return this.$store.getters.getUserData;
    },
    isAdmin() {
      let username = this.$route.params.username;
      let user = this.UserData.username;

      return user === username;
    },
    UserPosts() {
      // let elem = this.$refs.container_posts;
      let posts = this.$store.getters.getUserPosts;
      // let hash = this.$store.getters.getHash;

      // if (hash) {
      //   let timerId = setInterval(() => {
      //     elem = this.$refs.container_posts;

      //     if (elem) {
      //       elem.querySelector("#" + hash).scrollIntoView({
      //         block: "center",
      //         inline: "center",
      //         behavior: posts.length < 40 ? "smooth" : "auto"
      //       });

      //       clearInterval(timerId);

      //       this.load && this.$store.commit("setHash", "");
      //     }
      //   }, 100);
      // }

      if (posts.length > this.postsCountOld) {
        this.load = true;
        this.postsCountOld = posts.length;
      }

      return posts;
    },
    UserSubs() {
      return this.$store.getters.getUserSubs;
    },
    userInterests() {
      if (this.Profile.interests) {
        let len = this.Profile.interests.length;
        return this.Profile.interests.substring(1, len - 1).split("|");
      }
    },
    ProfileTab() {
      return this.$store.getters.getProfileTab;
    }
  },
  methods: {
    LoadNewPosts() {
      let block = this.$refs.container;
      let Hmax =
        block && Math.floor((block.scrollHeight - block.clientHeight) * 0.3);
      let h = block.scrollTop;
      let topic = this.$route.params.topic;

      if (h > Hmax) {
        if (this.load) {
          this.load = false;
          this.LoadUserPosts();
        }
      } else {
        this.load = true;
      }
    },
    LoadUserPosts() {
      if (this.Profile.posts_count) {
        this.isLoading = true;

        let top = this.UserPosts.length;
        let bottom = top + this.PostsLoadCount;
        let token = localStorage.getItem("token");
        let username = this.Profile.username;
        let domain = this.$store.getters.getDomain;

        axios
          .get(
            `${domain}/api/v1/news/post/list/${username}/?a=${top}&b=${bottom}`,
            {
              headers: { Authorization: "Token " + token }
            }
          )
          .then(response => {
            this.$store.commit("setUserPosts", { top, posts: response.data });
            this.isLoading = false;
          });
      }
    },
    LoadUserSubsProfiles() {
      this.isLoading = true;
      let token = localStorage.getItem("token");
      let users = this.Profile.subs_profiles;
      let domain = this.$store.getters.getDomain;

      axios
        .get(`${domain}/api/v1/home/profile/get_profiles/${users}`, {
          headers: { Authorization: "Token " + token }
        })
        .then(response => {
          this.$store.commit("setUserSubs", response.data);
          this.isLoading = false;
        });
    },
    setTab(tabName) {
      this.$store.commit("setProfileTab", tabName);
    }
  }
};
</script>

<style scoped>
@media (max-width: 1920px) {
  .card-columns {
    column-count: 2;
  }
}

.profileTab {
  width: 100%;
}

.avatar {
  width: 100%;
  height: auto;
  left: 50%;
  transform: translateX(-50%);
  border: 3px solid white;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.8);
  position: relative;
  margin-bottom: 15%;
}

.box {
  padding: 3% 150px 10% 150px;
}

.header {
  width: 100%;
  height: auto;
  position: relative;
  margin-bottom: 5%;
}

.body {
  position: relative;
  width: 100%;
  height: auto;
  padding-top: 3%;
}

.readersCount {
  position: absolute;
  right: 2%;
  top: 1%;
  font-weight: 500;
  font-size: 17px;
  color: white;
  text-shadow: 0 3px 4px rgba(0, 0, 0, 0.8);
}

.status {
  font-size: 15px;
  font-weight: 500;
  font-style: italic;
  color: rgba(0, 0, 0, 0.5);
  padding: 1% 3% 1% 2%;
}

.bio {
  max-height: 50vh;
  overflow-y: auto;
  overflow-x: hidden;
  width: 100%;
  padding: 2.5% 5% 3% 3%;
  background-color: white;
  color: rgba(0, 0, 0, 0.8);
  font-size: 18px;
  font-weight: 500;
  line-height: 1.6;
  box-shadow: 0px 1px 10px silver;
  border-radius: 5px;
  text-align: left;
}

.contact {
  font-size: 18px;
  font-weight: 550;
  color: rgba(0, 0, 0, 0.8);
  box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.7);
  background-color: rgba(255, 255, 255, 1);
  border-radius: 5px;
  padding: 1% 2% 1% 2%;
  position: relative;
  display: inline-block;
  margin-bottom: 1.5%;
  text-decoration: none;
  left: 0;
  transition: 0.2s all;
}
.contact:hover {
  cursor: pointer;
  left: 1%;
  background-color: rgba(255, 255, 255, 0.8);
}

.infoBar {
  width: 100%;
  display: inline-block;
  margin-bottom: 3%;
  background-color: #f8f8ff;
  border-radius: 5px;
  color: rgba(0, 0, 0, 0.8);
  box-shadow: 0px 5px 8px rgba(0, 0, 0, 0.7);
  font-size: 20px;
  font-weight: 500;
  padding: 1% 2% 1% 2%;
}

.username {
  font-size: 35px;
  font-weight: 600;
  color: white;
  display: block;
  position: relative;
  margin-bottom: 1%;
  text-shadow: 0 5px 10px rgba(0, 0, 0, 0.8);
}

.card {
  margin-bottom: 3%;
}
</style>
