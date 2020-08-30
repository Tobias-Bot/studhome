<template>
  <div>
    <!-- edit profile modal -->
    <div
      class="modal fade"
      id="profileModal"
      tabindex="-1"
      role="dialog"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h4>Редактирование профиля</h4>
            <button type="button" class="close" data-dismiss="modal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <button
              type="button"
              class="btn btn-light btnOption"
              @click="$refs.file.click()"
            >
              изменить аватарку
            </button>
            <input
              type="file"
              accept="image/jpeg, image/png, image/gif"
              ref="file"
              hidden="true"
              @change="handleFileUpload"
            />
            <br />
            <br />
            <div class="profileSettingCard">
              <h5>статус</h5>
              <textarea
                class="textInput"
                v-model="profile.status"
                placeholder="Статус профиля"
              ></textarea>
            </div>
            <div class="profileSettingCard">
              <h5>описание профиля</h5>
              <textarea
                class="textInput"
                v-model="profile.bio"
                placeholder="Описание"
              ></textarea>
            </div>
            <div class="profileSettingCard">
              <h5>школа/университет</h5>
              <input
                v-model="profile.school"
                class="form-control textInput"
                type="text"
                placeholder="добавьте свое образовательное учреждение"
              />
            </div>
            <div class="profileSettingCard">
              <h5>интересы</h5>
              <input
                v-model="ProfileTag"
                class="form-control textInput"
                type="text"
                placeholder="введите тему и нажмите enter"
                style="margin-bottom: 3%;"
                @keyup.enter="addProfileTag"
                @keyup.space="ProfileTag = ProfileTag.replace('  ', ' ')"
              />
              <div class="tag" v-for="(tag, i) in tags" :key="tag + i">
                {{ tag }}
                <span @click="deleteProfileTag(i)">x</span>
              </div>
            </div>
            <div class="profileSettingCard">
              <h5>контакты</h5>
              <input class="textInput" />
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-dark btnMain"
              data-dismiss="modal"
              @click="saveProfile"
            >
              сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-body">
        <template v-if="profile.username == username">
          <div
            class="btnProfileTools"
            title="редактировать профиль"
            data-toggle="modal"
            data-target="#profileModal"
            @click="loadUserInterests"
          >
            <i class="far fa-edit"></i>
          </div>
        </template>
        <template v-else>
          <div
            v-if="!inUserSubs"
            class="btnProfileTools"
            title="подписаться"
            @click="Subscribe(profile.username, username)"
          >
            <i class="fas fa-plus-circle"></i>
          </div>
          <div
            v-else
            class="btnProfileTools"
            title="отписаться"
            @click="unSubscribe(profile.username, username)"
          >
            <i class="far fa-times-circle"></i>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "profileTools",
  props: ["profile", "userInterests"],
  data: function() {
    return {
      avatarHasBeenUpdated: false,
      ProfileTag: "",
      spaces: 0,
      tags: []
    };
  },
  computed: {
    username() {
      return this.$store.getters.getUserData.username;
    },
    inUserSubs() {
      let names = this.$store.getters.getUserProfile.subs_profiles;
      if (names && names.indexOf(this.profile.username) == -1) return false;
      else return true;
    },
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
    getImagePreview(file) {
      if (/\.(jpe?g|png|gif)$/i.test(file.name)) {
        let reader = new FileReader();

        reader.addEventListener("load", () => {
          this.profile.avatar = reader.result;
          this.avatarHasBeenUpdated = true;
        });

        reader.readAsDataURL(file);
      }
    },
    handleFileUpload() {
      let ava = this.$refs.file.files[0];

      this.getImagePreview(ava);
    },
    saveProfile() {
      if (this.tags.length) this.profile.interests = `|${this.tags.join("|")}|`;

      this.$store.commit("setUserProfile", this.profile);
      this.saveToDB(this.profile);
      this.saveProfileToServer(this.profile);
    },
    saveProfileToServer(profile) {
      let token = localStorage.getItem("token");
      let domain = this.$store.getters.getDomain;
      let data = new FormData();
      let ava = this.$refs.file.files[0];

      if (this.avatarHasBeenUpdated) data.append("avatar", ava);
      data.append("bio", profile.bio);
      data.append("status", profile.status);
      data.append("interests", profile.interests);
      data.append("school", profile.school);
      data.append("user", profile.user);
      data.append("username", profile.username);

      axios.put(`${domain}/api/v1/home/profile_update/${profile.user}/`, data, {
        headers: {
          Authorization: "Token " + token,
          "Content-Type": "multipart/form-data"
        }
      });
    },
    saveToDB(obj) {
      let openRequest = indexedDB.open("profile", 1);

      openRequest.onupgradeneeded = function() {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains("profile")) {
          DB.createObjectStore("profile");
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
        return -1;
      };

      openRequest.onsuccess = function() {
        var DB = openRequest.result;

        DB.transaction("profile", "readwrite")
          .objectStore("profile")
          .put(obj, "userprofile");
      };
    },
    addProfileTag() {
      let tag = this.ProfileTag;
      let vm = this;

      if (tag && tag !== " ") {
        if (tag.indexOf(" ") == 0) tag = tag.substring(1, tag.length);
        if (tag.indexOf(" ") == tag.length - 1)
          tag = tag.substring(0, tag.length - 1);
        vm.tags.push(tag);
      }

      this.ProfileTag = "";
    },
    deleteProfileTag(i) {
      this.tags.splice(i, 1);
    },
    loadUserInterests() {
      if (this.userInterests) this.tags = this.userInterests;
    }
  }
};
</script>

<style scoped>
.btnProfileTools {
  width: 100%;
  position: relative;
  display: block;
  margin: 5% 0 5% 0;
  padding: 1% 1% 5% 1%;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  text-shadow: 0 2px 3px rgba(0, 0, 0, 0.5);
  font-size: 40px;
  font-weight: 500;
  border-radius: 5px;
  transition: 0.1s all;
}
.btnProfileTools:hover {
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.9);
  color: white;
}

.profileSettingCard {
  width: 100%;
  padding: 1% 1% 3% 1%;
  margin-bottom: 5%;
  border-radius: 5px;
  background-color: white;
  box-shadow: 0px 2px 7px rgba(0, 0, 0, 0.3);
}

.textInput {
  box-shadow: inset 0 1px 5px rgba(0, 0, 0, 0.3);
  padding: 2% 2% 2% 2%;
}

.modal-dialog {
  position: absolute;
  width: 40%;
  right: 2%;
  top: 5%;
}
</style>
