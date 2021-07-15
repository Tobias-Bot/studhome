<template>
  <div>
    <div class="BlackoutGlobal" :style="Style"></div>
    <img
      :src="picLocalUrl ? picLocalUrl : picUnsplashUrl"
      id="image"
      :style="'filter: blur(' + ImgBlur + 'px);'"
    />
    <nav
      id="main_header"
      class="navbar navbar-expand-lg navbar-light"
      :style="BGColor"
    >
      <img src="./static/logo.png" id="logo" />
      <span class="navbar-brand" :style="TextColor">studhome</span>
      <template v-if="IsAuthorized">
        <div class="btn-group" role="group">
          <router-link
            active-class="btn btn-active"
            class="btn btn-dark"
            to="/home"
          >
            <span class="MainTabs">
              <i class="fas fa-home"></i>
              <span style="color: white;">домой</span>
            </span>
          </router-link>
          <router-link
            active-class="btn btn-active"
            class="btn btn-dark"
            to="/news"
          >
            <span class="MainTabs">
              <i class="far fa-newspaper"></i>
              <span style="color: white;">публикации</span>
            </span>
          </router-link>
          <router-link
            active-class="btn btn-active"
            class="btn btn-dark"
            to="/search"
          >
            <span class="MainTabs">
              <i class="far fa-compass"></i>
              <span style="color: white;">поиск</span>
            </span>
          </router-link>
        </div>
        <ul class="navbar-nav ml-auto">
          <!-- <li class="nav-item" style="margin-right: 1vw; opacity: 0.95;">
            <h4><i class="fas fa-at"></i></h4>
          </li>
          <li class="nav-item" style="margin-right: 1vw;">
            <h4 v-if="msgOpen" @click="msgOpen = !msgOpen">
              <i class="far fa-envelope-open"></i>
            </h4>
            <h4 v-else @click="msgOpen = !msgOpen">
              <i class="far fa-envelope"></i>
            </h4>
          </li> -->
          <li class="nav-item">
            <div
              class="WriteBtn"
              @mouseover="isWritingSection = true"
              @mouseout="isWritingSection = false"
            >
              <i class="fas fa-pencil-alt"></i>
              <b>пост</b>
              <div v-show="isWritingSection" class="writeSlider">
                <router-link
                  tag="div"
                  class="btnInWritingSection"
                  style="text-decoration: none;"
                  :to="{ name: 'CreatePost', params: { editMode: false } }"
                >
                  <i class="far fa-file-alt"></i>
                  1
                </router-link>
                <div class="btnInWritingSection">
                  <i class="fas fa-list"></i>
                  2
                </div>
                <div class="btnInWritingSection">
                  <i class="far fa-sticky-note"></i>
                  3
                </div>
                <div class="btnInWritingSection">
                  <i class="far fa-bell"></i>
                  4
                </div>
              </div>
            </div>
          </li>
        </ul>
      </template>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
let Cookies = localStorage;

export default {
  name: "App",
  data() {
    return {
      msgOpen: false,

      isWritingSection: false
    };
  },
  methods: {},
  created() {
    let token = Cookies.getItem("token");

    if (token) {
      this.$store.commit("setAuth", true);
      this.$store.commit("setToken", token);
      this.$store.dispatch("addUserData", token);
    }
  },
  computed: {
    Style() {
      return {
        width: "100%",
        height: "100vh",
        position: "absolute",
        background:
          "rgba(0, 0, 0, " + this.$store.getters.getUserSettings.blackout + ")",
        "z-index": -1
      };
    },
    ImgBlur() {
      return this.$store.getters.getUserSettings.blur;
    },
    BGColor() {
      return {
        "background-color": this.ProfileColors[0]
      };
    },
    TextColor() {
      return {
        color: this.ProfileColors[1]
      };
    },
    ProfileColors() {
      let str = this.$store.getters.getUserSettings.colors;
      let colors = "|#FFFFFF|#323232|";

      if (str) {
        colors = str.substring(1, str.length - 1).split("|");
      }

      return colors;
    },
    picLocalUrl() {
      return this.$store.getters.getUserSettings.background;
    },
    picUnsplashUrl() {
      return this.$store.getters.getUserSettings.unsplash_background;
    },
    IsAuthorized() {
      return this.$store.getters.getAuth;
    }
  }
};
</script>

<style>
.btn-group {
  margin-left: 50px;
}

.btn-active {
  background-color: rgba(0, 0, 0, 0.4);
}

.navbar-brand {
  text-shadow: 1px 1px 5px white;
}

.writeSlider {
  width: inherit;
  position: absolute;
  z-index: 5;
  padding-top: 1%;
}

.btnInWritingSection {
  width: 60%;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  margin: 20% 0 20% 0;
  display: block;
  border-radius: 100px;
  background-color: white;
  color: rgba(0, 0, 0, 0.8);
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.8);
  font-size: 25px;
  font-weight: 500;
  text-align: center;
  text-decoration: none;
  transition: 0.1s all;
}
.btnInWritingSection:hover {
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.9);
  color: white;
}
</style>
