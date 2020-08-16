<template>
  <div>
    <div class="box">
      <div class="row">
        <div class="col-3">
          <WritingToolBar
            v-show="isText"
            :HighLighterColor="LighterColor"
            :NoteColor="NoteColor"
          ></WritingToolBar>
        </div>
        <div class="col-5" style="padding-right: 3%;">
          <div class="row">
            <PostToolBar
              :files.sync="files"
              :youtubeUrl.sync="youtubeUrl"
              @switch-note-mode="isText = !isText"
              @changed="saveDraftToMemory"
            ></PostToolBar>
          </div>
          <div class="row">
            <div class="bgnote">
              <textarea
                class="NoteTitle"
                rows="3"
                placeholder="Заголовок"
                ref="NoteTitle"
                @change="saveDraftToMemory"
              ></textarea>
              <div style="width: 100%; height: 5px;"></div>
              <span
                v-show="isText"
                class="NotePalette"
                title="выбрать цвета"
                @click="ChangeColors = !ChangeColors"
              >
                <i class="fas fa-palette"></i>
              </span>
              <div v-show="ChangeColors && isText">
                <span
                  class="NoteListTool"
                  title="цвет заметки"
                  @click="$refs.inputNoteColor.click()"
                >
                  заметка
                  <br />
                  <div
                    class="ColorLED"
                    :style="'background-color:' + NoteColor"
                  ></div>
                </span>
                <span
                  class="NoteListTool"
                  title="цвет текста"
                  @click="$refs.inputTextColor.click()"
                >
                  текст
                  <br />
                  <div
                    class="ColorLED"
                    :style="'background-color:' + TextColor"
                  ></div>
                </span>
                <span
                  class="NoteListTool"
                  title="цвет выделителя"
                  @click="$refs.inputLighterColor.click()"
                >
                  выделитель
                  <br />
                  <div
                    class="ColorLED"
                    :style="'background-color:' + LighterColor"
                  ></div>
                </span>
                <input
                  type="color"
                  ref="inputNoteColor"
                  v-model="NoteColor"
                  style="display: none;"
                  @change="saveDraftToMemory"
                />
                <input
                  type="color"
                  ref="inputTextColor"
                  v-model="TextColor"
                  style="display: none;"
                  @change="saveDraftToMemory"
                />
                <input
                  type="color"
                  ref="inputLighterColor"
                  v-model="LighterColor"
                  style="display: none;"
                />
              </div>
              <div
                v-show="isText"
                class="note"
                :style="
                  'background-color:' +
                    NoteColor +
                    ';' +
                    ' color:' +
                    TextColor +
                    ';'
                "
                ref="editor"
                contenteditable="true"
                placeholder="что новенького?"
                @input="saveDraftToMemory"
                @paste="DeleteStyles"
                @change="saveDraftToMemory"
              ></div>
              <div :class="{ 'card-columns': ManyImages }">
                <createPic
                  v-for="(file, key) in files"
                  :key="key"
                  :files.sync="files"
                  :index="key"
                  :editMode="EditMode"
                ></createPic>
              </div>
              <br />
              <hr />
              <button
                type="button"
                class="btn btn-dark btnMain"
                :disabled="isPublishing"
                style="float: right;"
                @click="createPost"
              >
                <template v-if="!isPublishing">
                  <span v-if="!EditMode">опубликовать</span>
                  <span v-else>сохранить изменения</span>
                </template>
                <template v-else="isPublishing">
                  <div class="spinner-border spinner-border-sm" role="status">
                    <span class="sr-only">Loading...</span>
                  </div>
                  публикация...
                </template>
              </button>
            </div>
          </div>
        </div>
        <div class="col-4">
          <div v-if="youtubeUrl" class="card">
            <div class="card-header">
              <h5 style="float: left;">Видео</h5>
              <button
                type="button"
                class="btn btn-light btn-sm btnOption"
                style="float: right; margin-left: 2%;"
                title="удалить видео"
                @click="
                  youtubeUrl = '';
                  saveDraftToMemory();
                "
              >
                <i class="fas fa-times"></i>
              </button>
              <button
                type="button"
                class="btn btn-light btn-sm btnOption"
                style="float: right;"
                data-toggle="modal"
                data-target="#youtubeModal"
              >
                заменить
              </button>
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
          <PostTags :tags.sync="tags" @changed="saveDraftToMemory"></PostTags>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import createPic from "../components/createPic";
import PostToolBar from "../components/PostCreate/PostToolBar";
import WritingToolBar from "../components/PostCreate/WritingToolBar";
import PostTags from "../components/PostCreate/PostTags";

export default {
  components: {
    createPic,
    PostToolBar,
    WritingToolBar,
    PostTags
  },
  data: function() {
    return {
      files: [],
      isText: false,

      ChangeColors: false,

      NoteColor: "white",
      TextColor: "#212121",
      LighterColor: "yellow",

      youtubeUrl: "",

      tags: [],

      isPublishing: false
    };
  },
  mounted() {
    let post = this.$route.params.post;
    let domain = this.$store.getters.getDomain;

    if (post) {
      if (post.images.length) {
        for (let i of post.images) {
          let img = {
            file: "",
            url: domain + i.image,
            text: i.text,
            image_id: i.id
          };

          this.files.push(img);
        }
      }

      if (post.title) {
        this.$refs.NoteTitle.value = post.title;
      }

      if (post.text) {
        this.isText = true;

        this.$refs.editor.innerHTML = post.text;
      }

      this.NoteColor = post.note_color;
      this.TextColor = post.text_color;

      if (post.video_url) {
        this.youtubeUrl = post.video_url;
      }

      if (post.tags.length > 2) {
        let tags = post.tags.split("|");
        tags.splice(0, 1);
        tags.splice(tags.length - 1, 1);
        this.tags = tags;
      }

      if (post.marks.length > 2) {
        let data = post.marks.substring(1, post.marks.length - 1).split("|");
        this.$store.commit("setPostMarks", data);
      }
    } else {
      this.loadDraftFromMemory({ store: "post-drafts", key: "draft" });
    }
  },
  computed: {
    UserData() {
      return this.$store.getters.getUserData;
    },
    video_url() {
      return (
        "https://www.youtube-nocookie.com/embed/" + this.youtubeUrl.slice(32)
      );
    },
    ManyImages() {
      if (this.files) return this.files.length > 2;
    },
    EditMode() {
      return this.$route.params.editMode;
    }
  },
  methods: {
    loadDraftFromMemory(obj) {
      var openRequest = indexedDB.open(obj.store, 1);

      openRequest.onupgradeneeded = () => {
        var DB = openRequest.result;
        if (!DB.objectStoreNames.contains(obj.store)) {
          DB.createObjectStore(obj.store);
        }
      };

      openRequest.onerror = function() {
        console.error("Can't create DB", openRequest.error);
      };

      openRequest.onsuccess = () => {
        var DB = openRequest.result;

        let tx = DB.transaction(obj.store, "readonly");
        let store = tx.objectStore(obj.store);
        let data = store.get(obj.key);

        let result = (tx.oncomplete = () => {
          if (data.result) this.setSavedPost(data.result);
        });
      };
    },
    saveDraftToMemory() {
      let text = $(".note").html();
      let title = this.$refs.NoteTitle.value;
      let tags = "|" + this.tags.join("|") + "|";
      let video_url = this.youtubeUrl;
      let marks = this.$store.getters.getCreatedPostMarks;
      let files = this.files;
      let note_color = this.NoteColor;
      let text_color = this.TextColor;

      let data = {
        title,
        video_url,
        tags,
        text,
        note_color,
        text_color,
        marks,
        files
      };

      this.$store.dispatch("saveToDB", {
        store: "post-drafts",
        key: "draft",
        data
      });
    },
    setSavedPost(data) {
      this.$refs.editor.innerHTML = data.text;
      this.$refs.NoteTitle.value = data.title;

      if (data.tags.length > 2)
        this.tags = data.tags.substring(1, data.tags.length - 1).split("|");

      if (data.youtubeUrl) this.youtubeUrl = data.youtubeUrl;
      else this.youtubeUrl = "";

      this.$store.commit("setPostMarks", data.marks);
      this.NoteColor = data.note_color;
      this.TextColor = data.text_color;
      this.files = data.files;
    },
    dropPostInDB(objstore) {
      this.$store.dispatch("DropStorage", objstore);
    },
    clearPostData() {
      this.$refs.NoteTitle.value = "";
      this.$refs.editor.innerHTML = "";
      this.tags.splice(0, this.tags.length);
      this.youtubeUrl = "";
      this.NoteColor = "white";
      this.TextColor = "#212121";
      this.LighterColor = "yellow";
      this.files.splice(0, this.files.length);
      this.$store.commit("dropCreatedPostMarks", 0);

      this.dropPostInDB("post-drafts");
    },
    createPost() {
      this.isPublishing = true;

      let text = "";
      let note_color = "";
      let text_color = "";
      let token = localStorage.getItem("token");
      let title = this.$refs.NoteTitle.value;
      let tags = "|" + this.tags.join("|") + "|";
      let user_id = this.UserData.id;
      let username = this.UserData.username;
      let video_url = this.youtubeUrl;
      let type = "|";
      let marks = this.$store.getters.getCreatedPostMarks;

      if (this.isText) {
        text = $(".note").html();
        note_color = this.NoteColor;
        text_color = this.TextColor;
      }

      if (marks) {
        marks = "|" + marks.join("|") + "|";
      }

      let post = {
        user: user_id,
        username,
        title,
        video_url,
        tags,
        type,
        text,
        note_color,
        text_color,
        marks
      };

      if (text.length && this.isText) {
        post.type += "note|";
      }

      if (this.files.length > 0 && !text.length && !video_url.length)
        post.type += "photo|";
      // if () type + "document|";

      if (this.EditMode) {
        let post_id = this.$route.params.post.id;
        this.submitEditedPost(post_id, post, token);
      } else {
        this.submitPost(username, post, token);
      }
    },
    submitEditedPost(post_id, post, token) {
      axios
        .put(
          "http://127.0.0.1:8000/api/v1/news/post_update/" + post_id + "/",
          post,
          {
            headers: {
              Authorization: "Token " + token
            }
          }
        )
        .then(response => {
          let post_id = response.data.id;
          let domen = this.$store.getters.getDomen;

          if (this.files.length > 0) {
            for (var i = 0; i < this.files.length; i++) {
              if (!this.files[i].image_id) this.submitPhotos(token, post_id, i);
            }

            this.clearPostData();
          }
          this.isPublishing = false;
        })
        .catch(e => {
          console.log(e);
        });
    },
    submitPost(username, post, token) {
      let profile = this.$store.getters.getUserProfile;

      axios
        .post(
          "http://127.0.0.1:8000/api/v1/news/post_create/" + username + "/",
          post,
          {
            headers: {
              Authorization: "Token " + token
            }
          }
        )
        .then(response => {
          let post_id = response.data.id;

          if (this.files.length > 0) {
            for (var i = 0; i < this.files.length; i++) {
              this.submitPhotos(token, post_id, i);
            }

            this.clearPostData();
          }

          profile.posts_count = profile.posts_count + 1;

          this.$store.dispatch("saveToDB", {
            store: "profile",
            key: "userprofile",
            data: profile
          });

          this.isPublishing = false;
        })
        .catch(e => {
          console.log(e);
        });
    },
    submitPhotos(token, post_id, img_index) {
      let formData = new FormData();
      formData.append("post", post_id);
      formData.append("text", this.files[img_index].text);
      formData.append("image", this.files[img_index].file);

      axios.post(
        "http://127.0.0.1:8000/api/v1/news/post/" + post_id + "/image/",
        formData,
        {
          headers: {
            Authorization: "Token " + token,
            "Content-Type": "multipart/form-data"
          }
        }
      );
    },
    DeleteStyles(event) {
      event.preventDefault();
      var text = (event.originalEvent || event).clipboardData.getData(
        "text/plain"
      );
      document.execCommand("insertText", false, text);
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

.bgnote {
  width: 100%;
  height: auto;
  padding: 4% 3% 2% 3%;
  margin-top: 2%;
  border-radius: 5px;
  background-color: white;
}

.NoteTitle {
  width: 100%;
  margin-bottom: 1%;
  height: auto;
  outline: none;
  resize: none;
  border: none;
  line-height: 1.3;
  font-weight: 600;
  font-size: 30px;
  color: #323232;
}

.NoteListTool {
  float: right;
  padding: 0% 2% 2% 0%;
  margin: 0% 1% 0% 1%;
  opacity: 0.8;
  font-size: 15px;
}
.NoteListTool:hover {
  cursor: pointer;
  opacity: 1;
}

.note {
  width: 100%;
  height: auto;
  display: inline-block;
  padding: 3% 3% 5% 3%;
  margin-bottom: 3%;
  border-radius: 5px;
  outline: none;
  font-size: 20px;
  color: rgba(0, 0, 0, 0.9);
  box-shadow: 0px 3px 10px silver;
}
.note[placeholder]:empty:before {
  content: attr(placeholder);
  color: #555;
}
.note[placeholder]:empty:focus:before {
  content: "";
}

.video {
  width: 100%;
  height: 25vh;
  box-shadow: 0px 1px 12px black;
  border-radius: 8px;
}

.card {
  margin-left: 10%;
  margin-bottom: 5%;
}

.ColorLED {
  width: 100%;
  height: 5px;
  border: 1px solid silver;
  border-radius: 5px;
}

.NotePalette {
  float: right;
  padding: 0% 2% 2% 0%;
  margin: 0% 1% 0% 1%;
  opacity: 0.7;
  font-size: 18px;
}
.NotePalette:hover {
  cursor: pointer;
  opacity: 1;
}
</style>
