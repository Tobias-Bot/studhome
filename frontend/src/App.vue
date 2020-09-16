<template>
  <div>
    <div class="BlackoutGlobal" :style="Style"></div>
    <img
      :src="picLocalUrl ? picLocalUrl : picUnsplashUrl"
      id="image"
      :style="'filter: blur(' + ImgBlur + 'px);'"
    />
    <nav id="main_header" class="navbar navbar-expand-lg navbar-light">
      <div :class="!IsAuthorized ? 'logoBlock' : ''">
        <img src="@/static/logo.png" id="logo" />
        <span class="navbar-brand">studhome</span>
      </div>
      <template v-if="IsAuthorized">
        <div class="btn-group" role="group">
          <router-link
            active-class="btn btn-active"
            class="btn btn-light"
            to="/search"
          >
            <span class="MainTabs">
              <i class="fas fa-compass"></i>
              <span style="margin-left: 3px;">поиск</span>
            </span>
          </router-link>
          <router-link
            active-class="btn btn-active"
            class="btn btn-light"
            to="/news"
          >
            <span class="MainTabs">
              <i class="fas fa-newspaper"></i>
              <span style="margin-left: 3px;">публикации</span>
            </span>
          </router-link>
          <router-link
            active-class="btn btn-active"
            class="btn btn-light"
            to="/apps"
          >
            <span class="MainTabs">
              <i class="fas fa-shapes"></i>
              <span style="margin-left: 3px;">приложения</span>
            </span>
          </router-link>
          <router-link
            active-class="btn btn-active"
            class="btn btn-light"
            to="/rooms"
          >
            <span class="MainTabs">
              <i class="fas fa-home"></i>
              <span style="margin-left: 3px;">моя комната</span>
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
            <div class="OptionalMainBtns">
              <router-link tag="div" class="smallBtn" to="/bookmarks">
                <i class="far fa-bookmark"></i>
              </router-link>
              <div
                class="smallBtn"
                @mouseover="isProfileSection = true"
                @mouseout="isProfileSection = false"
              >
                <i class="far fa-user-circle"></i>
                <div v-show="isProfileSection" class="slider">
                  <router-link
                    tag="span"
                    :to="{
                      name: 'profile',
                      params: { username },
                    }"
                  >
                    <span class="btnInSlider">
                      <i class="fas fa-user"></i>
                      профиль
                    </span>
                  </router-link>
                  <router-link tag="span" to="/settings">
                    <span class="btnInSlider">
                      <i class="fas fa-sliders-h"></i>
                      настройки
                    </span>
                  </router-link>
                </div>
              </div>
            </div>
            <div
              class="WriteBtn"
              @mouseover="isWritingSection = true"
              @mouseout="isWritingSection = false"
            >
              <i class="fas fa-pencil-alt"></i>
              <div v-show="isWritingSection" class="writeSlider">
                <router-link
                  tag="div"
                  class="btnInWritingSection"
                  style="text-decoration: none;"
                  :to="{ name: 'CreatePost', params: { editMode: false } }"
                >
                  <i class="fas fa-file-signature"></i>
                </router-link>
                <div class="btnInWritingSection">
                  <i class="fas fa-check-square"></i>
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
      isWritingSection: false,
      isProfileSection: false,
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
        background:
          "rgba(0, 0, 0, " + this.$store.getters.getUserSettings.blackout + ")",
        "z-index": -1,
      };
    },
    ImgBlur() {
      return this.$store.getters.getUserSettings.blur;
    },
    picLocalUrl() {
      return this.$store.getters.getUserSettings.background;
    },
    picUnsplashUrl() {
      return this.$store.getters.getUserSettings.unsplash_background;
    },
    IsAuthorized() {
      return this.$store.getters.getAuth;
    },
    username() {
      return this.$store.getters.getUserData.username;
    },
  },
};
</script>

<style>
.logoBlock {
  width: 100%;
  text-align: center;
}

.btn-group {
  margin-left: 50px;
}

.btn-active {
  background-color: rgba(0, 0, 0, 0.1);
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
  width: 50px;
  height: 50px;
  display: block;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  margin: 20% 0 20% 0;
  padding-top: 10%;
  border-radius: 100px;
  border: 2px solid white;
  background-color: white;
  color: rgba(0, 0, 0, 0.9);
  box-shadow: 2px 5px 20px black;
  font-size: 23px;
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
