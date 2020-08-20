<template>
  <div class="box-with-tools">
    <div class="card-columns">
      <design></design>
      <account></account>
    </div>
  </div>
</template>

<script>
import design from "../../components/MainSettings/design"
import account from "../../components/MainSettings/account"

var Cookies = localStorage;

export default {
  name: "settings",
  components: {
    design,
    account
  },
  data() {
    return {
      settingsState: {
        BlackOutRange: {
          id: "BlackOutRange",
          value: 0
        },
        BackgroundPicture: {
          id: "BackgroundPicture",
          url: ""
        }
      }
    };
  },
  computed: {
    range() {
      let value = this.$store.getters.getRange;
      this.settingsState.BlackOutRange.value = value;
      return value;
    },
    UserData() {
      return this.$store.getters.getUserData;
    }
  },
  methods: {
    saveToDB(obj) {
      let openRequest = indexedDB.open("settings", 1);

      openRequest.onupgradeneeded = function() {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains("settings")) {
          DB.createObjectStore("settings", { keyPath: "id" });
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
        return -1;
      };

      openRequest.onsuccess = function() {
        var DB = openRequest.result;

        let ob = DB.transaction("settings", "readwrite")
          .objectStore("settings")
          .put(obj);
      };
    },
    LogoutFunc() {
      let token = Cookies.getItem("token");

      axios
        .options("/api/v1/auth_token/token/logout", {
          headers: { Authorization: "Token " + token }
        })
        .then(response => {
          this.$store.commit("setToken", "");
          this.$store.commit("setAuth", false);
          Cookies.removeItem("token");
        });
    },
    changeBlackOut() {
      var obj = this.settingsState.BlackOutRange;
      this.$store.commit("setRange", obj.value);
      this.saveToDB(obj);
    },
    changeBackPicture() {
      let w = screen.width;
      let h = screen.height;

      let strApi = "https://source.unsplash.com/";
      let pic = this.settingsState.BackgroundPicture;

      if (pic.url.indexOf("https://unsplash.com/photos") != -1) {
        let url = strApi + pic.url.slice(28) + "/" + w + "x" + h;
        pic.url = url;
        this.$store.commit("setBackPicture", pic.url);
        this.saveToDB(pic);
      }
    },
    changeBackPictureRand() {
      let w = screen.width;
      let h = screen.height;

      let url = "https://source.unsplash.com/" + w + "x" + h + "/?cozy";
      let pic = this.settingsState.BackgroundPicture;
      pic.url = url;
      this.$store.commit("setBackPicture", pic.url);
      this.saveToDB(pic);
    },
    DeleteBackPicture() {
      let pic = this.settingsState.BackgroundPicture;

      pic.url = "";
      this.$store.commit("setBackPicture", pic.url);
      this.saveToDB(pic);
    },
  }
};
</script>

<style scoped>

</style>
