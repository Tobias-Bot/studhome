<template>
  <div>
    <!-- setting picture url modal -->
    <div
      class="modal fade"
      id="PicUrlModal"
      tabindex="-1"
      role="dialog"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <input
              v-model="settings.unsplash_background"
              type="text"
              class="form-control PicUrlModal"
              placeholder="вставьте ссылку на фото c unsplash.com"
              @input="changePicFromUnsplash"
              @change="isLoading = true"
            />
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-light btnMain"
              data-dismiss="modal"
            >
              сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h4>внешний вид</h4>
      </div>
      <div class="card-body">
        <span class="SettingTitle">фоновое изображение</span>
        <button
          type="button"
          class="btn btn-light PicBtn btnOption"
          @click="$refs.file.click()"
        >
          загрузить с компьютера
        </button>
        <button
          type="button"
          class="btn btn-dark PicBtn btnOption"
          data-toggle="modal"
          data-target="#PicUrlModal"
        >
          фото с unsplash
        </button>
        <button
          type="button"
          class="btn btn-outline-secondary PicBtn btnOption"
          @click="DeleteBackPicture"
        >
          удалить фон
        </button>
        <input
          type="file"
          accept="image/jpeg, image/png, image/gif"
          ref="file"
          hidden="true"
          @change="handleFileUpload"
        />
        <template v-if="pic || unsplash_pic">
        <hr />
        <span class="SettingTitle">затемнение фона {{ range }}</span>
        <input
          v-model="settings.blackout"
          @input="changeBlackOut"
          type="range"
          class="custom-range textInput"
          min="0"
          max="1"
          step="0.05"
        />
        <hr />
        <span class="SettingTitle">размытие фона {{ blur }}</span>
        <input
          v-model="settings.blur"
          @input="changeBlackOut"
          type="range"
          class="custom-range textInput"
          min="0"
          max="5"
          step="1"
        />
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "design",
  data() {
    return {
      settings: {
        user: null,
        blackout: 0,
        blur: 0,
        background: "",
        unsplash_background: "",
      },
      isChanged: false,
      localPhotoFile: "",
    };
  },
  beforeDestroy() {
    if (this.isChanged) {
      this.updateSettings();
    }
  },
  computed: {
    range() {
      let value = this.$store.getters.getUserSettings.blackout;
      this.setRange(value);
      return value;
    },
    blur() {
      let value = this.$store.getters.getUserSettings.blur;
      this.setBlur(value);
      return value;
    },
    pic() {
      return this.$store.getters.getUserSettings.background;
    },
    unsplash_pic() {
      return this.$store.getters.getUserSettings.unsplash_background;
    },
    UserData() {
      return this.$store.getters.getUserData;
    },
  },
  methods: {
    setRange(value) {
      this.settings.blackout = value;
    },
    setBlur(value) {
      this.settings.blur = value;
    },
    updateSettings() {
      let token = localStorage.getItem("token");
      let user_id = this.$store.getters.getUserData.id;
      let domain = this.$store.getters.getDomain;
      let formData = new FormData();

      formData.append("user", user_id);
      formData.append("blackout", this.settings.blackout);
      formData.append("blur", this.settings.blur);
      formData.append("background", this.localPhotoFile);
      formData.append("unsplash_background", this.settings.unsplash_background);

      axios.put(`${domain}/api/v1/home/settings_update/${user_id}/`, formData, {
        headers: {
          Authorization: "Token " + token,
          "Content-Type": "multipart/form-data"
        }
      });
    },
    saveToDB(obj) {
      this.isChanged = true;
      obj.user = this.UserData.id;
      let openRequest = indexedDB.open("settings", 1);

      openRequest.onupgradeneeded = function() {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains("settings")) {
          DB.createObjectStore("settings");
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
        return -1;
      };

      openRequest.onsuccess = function() {
        var DB = openRequest.result;

        DB.transaction("settings", "readwrite")
          .objectStore("settings")
          .put(obj, "settings");
      };
    },
    changeBlackOut() {
      this.settings.background = this.pic;
      this.settings.unsplash_background = this.unsplash_pic;
      this.$store.commit("setUserSettings", this.settings);
      this.saveToDB(this.settings);
    },
    changePicFromUnsplash() {
      let w = screen.width;
      let h = screen.height;

      let strApi = "https://source.unsplash.com/";
      let pic = this.settings.unsplash_background;

      if (pic.indexOf("https://unsplash.com/photos") != -1) {
        this.settings.unsplash_background =
          strApi + pic.slice(28) + "/" + w + "x" + h;
        this.$store.commit("setUserSettings", this.settings);
        this.saveToDB(this.settings);
      }
    },
    DeleteBackPicture() {
      let settings = this.settings;

      if (settings.background) settings.background = "";
      if (settings.unsplash_background) settings.unsplash_background = "";
      this.$store.commit("setUserSettings", this.settings);
      this.saveToDB(this.settings);
    },
    getImagePreview(file) {
      if (/\.(jpe?g|png|gif)$/i.test(file.name)) {
        let reader = new FileReader();

        reader.addEventListener("load", () => {
          this.settings.background = reader.result;
          this.$store.commit("setUserSettings", this.settings);
          this.saveToDB(this.settings);
        });

        reader.readAsDataURL(file);
      }
    },
    handleFileUpload() {
      this.isLocalPhoto = true;
      this.localPhotoFile = this.$refs.file.files[0];

      this.getImagePreview(this.localPhotoFile);
    }
  }
};
</script>

<style scope>
.PicUrlModal {
  width: 100%;
  font-size: 20px;
  font-weight: 600;
  box-shadow: 0px 2px 2px silver;
}

.SettingTitle {
  width: auto;
  font-size: 18px;
  font-weight: 550;
  opacity: 0.9;
  display: block;
  margin-bottom: 4%;
}

.PicBtn {
  width: 100%;
  display: inline-block;
  margin: 1% 1% 1% 1%;
}
</style>
