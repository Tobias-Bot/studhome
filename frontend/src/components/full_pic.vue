<template>
  <div class="cover">
    <div class="modal-dialog modal-xl">...</div>
    <div class="row">
      <div class="col-8" style="height: 85vh;">
        <img
          :src="ImgUrl"
          :class="[isHorizontal ? HorizontalImgStyle : VerticalImgStyle]"
          alt="image"
          ref="pic"
        />
      </div>
      <div class="col-4">
        <div class="card" style="background-color: rgba(0, 0, 0, 0.8);">
          <div v-if="CurrImg.username" class="card-body">
            <router-link
              style="text-decoration: none;"
              :to="{ name: 'profile', params: { username: CurrImg.username } }"
            >
              <span class="username" @click="LoadProfile(CurrImg.username)">{{
                CurrImg.username
              }}</span>
            </router-link>
            <template v-if="CurrImg.username !== UserData.username">
              <span
                v-if="!inUserSubs"
                class="btnSubscribe"
                style="color: white;"
                @click="Subscribe(CurrImg.username, UserData.username)"
                ><i class="fas fa-plus-circle"></i
              ></span>
              <span
                v-else
                class="btnSubscribe"
                @click="unSubscribe(CurrImg.username, UserData.username)"
                ><i class="far fa-times-circle"></i
              ></span>
            </template>
          </div>
        </div>
        <div v-if="CurrImg.text" class="card">
          <div class="card-body">
            <div class="photoDescription">
              <i>{{ CurrImg.text }}</i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      isHorizontal: false,
      HorizontalImgStyle: "img_horizontal",
      VerticalImgStyle: "img_vertical"
    };
  },
  created() {
    let posts = this.$store.getters.getPosts;
    let myNewsPosts = this.$store.getters.getMyNewsPosts;
    let userPosts = this.$store.getters.getUserPosts;
    let searchPosts = this.$store.getters.getSearchPost;
    let image_id = this.$route.params.pic_id;
    let image = this.$route.params.pic;

    if (
      image &&
      (posts.length ||
        userPosts.length ||
        myNewsPosts.length ||
        searchPosts.length)
    ) {
      this.$store.commit("setCurrImage", image);
    } else {
      if (!image && !this.CurrImg.id) {
        let domain = this.$store.getters.getDomain;
        let token = localStorage.getItem("token");

        axios
          .get(`${domain}/api/v1/news/post/image/${image_id}/`, {
            headers: { Authorization: "Token " + token }
          })
          .then(response => {
            let image = response.data[0];
            this.$store.commit("setCurrImage", image);
          })
          .catch(function(e) {
            console.log(e);
          });
      }
    }
  },
  mounted() {
    let timerId = setInterval(() => {
      let h = this.$refs.pic.naturalHeight;
      let w = this.$refs.pic.naturalWidth;

      if (h && w) {
        if (h >= w) {
          this.isHorizontal = false;
        } else {
          this.isHorizontal = true;
        }

        clearInterval(timerId);
      }
    }, 200);
  },
  computed: {
    CurrImg() {
      let img = this.$store.getters.getCurrImage;

      return img;
    },
    inUserSubs() {
      let names = this.$store.getters.getUserProfile.subs_profiles;
      if (names && names.indexOf(this.CurrImg.username) == -1) return false;
      else return true;
    },
    UserData() {
      return this.$store.getters.getUserData;
    },
    ImgUrl() {
      if (this.CurrImg.image)
        return ~this.CurrImg.image.indexOf("http://127.0.0.1:8000")
          ? this.CurrImg.image
          : "http://127.0.0.1:8000" + this.CurrImg.image;
    }
  },
  methods: {
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
    },
    LoadProfile(username) {
      let isAdmin = username === this.UserData.username;

      this.$store.commit("dropUserPosts");
      this.$store.commit("dropUserSubs");
      this.$store.commit("setProfileTab", "description");

      this.$store.dispatch("LoadProfile", { blog: "", isAdmin, username });
    }
  }
};
</script>

<style scoped>
img {
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0px 1px 15px black;
  border-radius: 5px;
  position: absolute;
  top: 0;
  bottom: 10%;
  margin: auto 0;
}
.img_horizontal {
  width: 70%;
  height: auto;
}
.img_vertical {
  height: 85%;
  width: auto;
}

.photoDescription {
  max-height: 40vh;
  overflow-y: auto;
  overflow-x: hidden;
  width: 100%;
  padding: 3% 7% 3% 4%;
  background-color: #fafafa;
  color: #3c3c3c;
  box-shadow: 0px 1px 10px silver;
  border-radius: 5px;
}

.card {
  margin-left: 3%;
  margin-bottom: 3%;
}

.cover {
  position: fixed;
  z-index: 1;
  width: 100%;
  height: 100vh;
  padding: 2% 150px 2.5% 150px;
  background-color: rgba(0, 0, 0, 0.8);
}

.username {
  font-size: 20px;
  color: white;
  opacity: 0.8;
}
.username:hover {
  opacity: 1;
}

.btnSubscribe {
  font-size: 20px;
  color: white;
  opacity: 0.8;
}
.btnSubscribe:hover {
  opacity: 1;
}
</style>
