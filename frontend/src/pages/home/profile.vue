<template>
  <div class="box">
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
          <div
            class="nav flex-column nav-tabs"
            id="v-pills-tab"
            role="tablist"
            aria-orientation="vertical"
          >
            <a
              v-if="Profile.bio"
              class="btn btn-light active btnMain"
              data-toggle="tab"
              href="#description"
              role="tab"
              aria-selected="true"
              >описание</a
            >
            <a
              v-if="Profile.posts_count"
              class="btn btn-light btnMain"
              type="button"
              data-toggle="tab"
              href="#posts"
              role="tab"
              aria-selected="false"
              @click="LoadUserPosts"
              >записи</a
            >
            <a
              v-if="Profile.subs_profiles && Profile.subs_profiles.length > 1"
              class="btn btn-light btnMain"
              data-toggle="tab"
              href="#blogs"
              role="tab"
              aria-selected="false"
              @click="LoadUserSubsProfiles"
              >подписки</a
            >
            <a
              v-if="Profile.contacts"
              class="btn btn-light btnMain"
              id="v-pills-settings-tab"
              data-toggle="tab"
              href="#contacts"
              role="tab"
              aria-selected="false"
              >контакты</a
            >
          </div>
        </div>
        <div class="col-8">
          <div class="tab-content">
            <div
              class="tab-pane fade show active"
              id="description"
              role="tabpanel"
            >
              <span class="username"
                >{{ Profile.username }}
                <span class="readersCount"
                  >читают: {{ Profile.readers }}</span
                ></span
              >
              <div class="card">
                <div class="card-body">
                  <template v-if="Profile.status">
                    <span class="status">{{ Profile.status }}</span>
                    <br />
                    <br />
                  </template>
                  <template v-if="Profile.bio || Profile.school">
                    <div class="bio">
                      <span class="hint" style="text-align: left;">Обо мне</span>
                      {{ Profile.bio }}
                      <hr />
                      <span class="hint" style="text-align: left;">Школа/универ</span>
                      {{ Profile.school }}
                    </div>
                    <br />
                  </template>
                  <tag
                    v-for="(tag, i) in userInterests"
                    :key="tag + i"
                    :text="tag"
                  ></tag>
                </div>
              </div>
            </div>
            <div class="tab-pane fade" id="posts" role="tabpanel">
              <div class="infoBar">
                записи: {{ Profile.posts_count }}
                <template v-if="isLoading">
                  <div
                    class="spinner-border spinner-border-sm"
                    role="status"
                  ></div>
                </template>
              </div>
              <div class="card-columns">
                <post
                  v-for="(post, id) in UserPosts"
                  :key="id"
                  :post="post"
                  :post_index="id"
                  :topic="'profile'"
                ></post>
              </div>
            </div>
            <div
              v-if="Profile.subs_profiles && Profile.subs_profiles.length > 1"
              class="tab-pane fade"
              id="blogs"
              role="tabpanel"
            >
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
            <div class="tab-pane fade" id="contacts" role="tabpanel">
              <template v-if="Profile.contacts">
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
              </template>
            </div>
          </div>
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
      isLoading: false
    };
  },
  created() {
    this.LoadProfile();
  },
  beforeDestroy() {
    this.$store.commit("dropUserPosts");
    this.$store.commit("dropUserSubs");
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

      return user == username ? true : false;
    },
    UserPosts() {
      return this.$store.getters.getUserPosts;
    },
    UserSubs() {
      return this.$store.getters.getUserSubs;
    },
    userInterests() {
      if (this.Profile.interests) {
        let len = this.Profile.interests.length;
        return this.Profile.interests.substring(1, len - 1).split("|");
      }
    }
  },
  methods: {
    LoadUserPosts() {
      if (this.Profile.posts_count) {
        this.isLoading = true;
        let token = localStorage.getItem("token");
        let username = this.Profile.username;

        axios
          .get(
            "http://127.0.0.1:8000/api/v1/news/post/list/" + username + "/",
            {
              headers: { Authorization: "Token " + token }
            }
          )
          .then(response => {
            this.$store.commit("setUserPosts", response.data);
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
    LoadProfile() {
      if (!this.isAdmin) {
        let blog = this.$route.params.blog;

        if (blog) {
          this.$store.commit("setCurrProfile", blog);
        } else {
          let token = localStorage.getItem("token");
          let domain = this.$store.getters.getDomain;
          let username = this.$route.params.username;

          axios
            .get(`${domain}/api/v1/home/profile/${username}/`, {
              headers: {
                Authorization: "Token " + token
              }
            })
            .then(response => {
              this.$store.commit("setCurrProfile", response.data[0]);
            })
            .catch(function(e) {
              console.log(e);
            });
        }
      }
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

.nav-tabs {
  border: none;
}

.nav-link {
  color: white;
  background-color: rgba(0, 0, 0, 0.3);
  box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.8);
  text-align: center;
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
  width: 100%;
  height: auto;
  position: relative;
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
  display: block;
  margin-bottom: 2%;
  background-color: white;
  border-radius: 5px;
  color: rgba(0, 0, 0, 0.8);
  box-shadow: 0px 2px 15px rgba(0, 0, 0, 0.7);
  font-size: 18px;
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
</style>
