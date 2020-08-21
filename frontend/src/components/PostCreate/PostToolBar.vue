<template>
  <div style="width: 100%;">
    <!-- youtube modal -->
    <div
      class="modal fade"
      id="youtubeModal"
      tabindex="-1"
      role="dialog"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h4>Добавить видео</h4>
            <button type="button" class="close" data-dismiss="modal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body" style="text-align: center;">
            <span style="opacity: 0.6; font-size: 14px;"
              >вставьте ссылку на видео с youtube.com в поле ниже</span
            >
            <br />
            <br />
            <div
              class="input-group"
              style="box-shadow: 0px 2px 7px silver; font-size: 17px;"
            >
              <input
                class="form-control textInput"
                v-model="YoutubeUrl"
                type="text"
                placeholder="https://www.youtube.com/..."
                @input="setYoutubeUrl"
              />
              <div v-if="youtubeUrl" class="input-group-append">
                <button
                  class="btn btn-secondary"
                  type="button"
                  title="удалить"
                  @click="destroyYoutubeUrl"
                >
                  x
                </button>
              </div>
            </div>
            <br />
            <br />
            <button
              type="button"
              class="btn btn-dark"
              data-dismiss="modal"
              style="box-shadow: 0px 4px 10px black; float: right;"
              @click="$emit('changed')"
            >
              добавить
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="post-toolbar">
      <div class="dropdown">
        <button
          class="btn btn-light dropdown-toggle PostTool btnMain"
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
          title="добавить метку"
        >
          <i class="fas fa-tags"></i>
          метки
        </button>
        <div class="dropdown-menu">
          <PostMarks
            v-for="(mark, i) in marks"
            :key="'mark' + i"
            :name="mark"
            @addMark="$emit('changed')"
          ></PostMarks>
        </div>
      </div>
      <button
        class="btn btn-light PostTool btnMain"
        data-toggle="modal"
        data-target="#youtubeModal"
        title="добавить видео с youtube"
      >
        <i class="fab fa-youtube"></i>
        видео
      </button>
      <button
        class="btn btn-light PostTool btnMain"
        @click="$refs.files.click()"
        title="загрузить фотографии"
      >
        <i class="fas fa-camera"></i>
        фото
      </button>
      <button
        class="btn btn-light PostTool btnMain"
        title="добавить текст"
        @click="$emit('switch-note-mode')"
      >
        <i class="fas fa-envelope-open-text"></i>
        текст
      </button>
      <input
        type="file"
        accept="image/jpeg, image/gif, image/png"
        ref="files"
        multiple
        hidden="true"
        @change="handleFileUpload"
      />
    </div>
  </div>
</template>

<script>
import PostMarks from "./PostMarks";

export default {
  props: ["files", "youtubeUrl"],
  components: {
    PostMarks
  },
  data: function() {
    return {
      YoutubeUrl: "",
      marks: ["вопрос", "книга"]
    };
  },
  computed: {},
  methods: {
    getImagePreviews(old_len) {
      for (let i = old_len; i < this.files.length; i++) {
        if (/\.(jpe?g|png|gif)$/i.test(this.files[i].file.name)) {
          let reader = new FileReader();

          reader.addEventListener(
            "load",
            function() {
              this.files[i].url = reader.result;
              this.$emit('changed');
            }.bind(this),
            false
          );

          reader.readAsDataURL(this.files[i].file);
        }
      }
    },
    handleFileUpload() {
      let uploadedFiles = this.$refs.files.files;
      let len = this.files.length;

      for (var i = 0; i < uploadedFiles.length; i++) {
        this.files.push({ file: uploadedFiles[i], url: "", text: "" });
      }

      this.getImagePreviews(len);
    },
    setYoutubeUrl() {
      this.$emit("update:youtubeUrl", this.YoutubeUrl);
    },
    destroyYoutubeUrl() {
      this.YoutubeUrl = "";
      this.$emit("update:youtubeUrl", this.YoutubeUrl);
      this.$emit('changed');
    }
  }
};
</script>

<style scoped>
.post-toolbar {
  width: 100%;
  height: auto;
  padding: 1% 0% 1% 1%;
}

.PostTool {
  width: auto;
  float: right;
}
</style>
