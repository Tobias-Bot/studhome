<template>
  <div class="ImgBG">
    <img
      class="image"
      :src="files[index].url"
      @mouseover="
        ImgSettings = true;
        ShowImgDesc = true;
      "
      @mouseout="
        ImgSettings = false;
        ShowImgDesc = false;
      "
    />
    <div
      v-show="ImgSettings"
      class="ImgSettings"
      @mouseover="ImgSettings = true"
      @mouseout="ImgSettings = false"
    >
      <button
        class="btn btn-outline-light btn-sm"
        @click="DeletePreviewPhoto(index)"
      >
        <i class="fas fa-times"></i>
      </button>
    </div>
    <textarea
      v-show="ShowImgDesc"
      v-model="files[index].text"
      class="imgDescription"
      rows="3"
      placeholder="добавьте описание к фото, если хотите"
      @mouseover="ShowImgDesc = true"
      @mouseout="ShowImgDesc = false"
      @change.once="files[index].modified = true"
    ></textarea>
  </div>
</template>

<script>
export default {
  props: ["source", "files", "index", "editMode"],
  components: {},
  data: function() {
    return {
      ImgSettings: false,
      ShowImgDesc: false,

      Modified: false,
    };
  },
  methods: {
    DeletePreviewPhoto(i) {
      this.DeletePhotoFromServer(i);

      this.files.splice(i, 1);
    },
    DeletePhotoFromServer(i) {
      let img_id = this.files[i].image_id;
      let domain = this.$store.getters.getDomain;
      let token = localStorage.getItem("token");

      if (img_id && token) {
        axios
        .delete(
          `${domain}/api/v1/news/post/image_delete/${img_id}/`,
          {
            headers: {
              Authorization: "Token " + token
            }
          }
        )
        .catch(e => {
          console.log(e);
        });
      }
    },
  }
};
</script>

<style scoped>
.image {
  width: 100%;
  height: auto;
  position: sticky;
  border-radius: 5px;
  z-index: inherit;
}

.ImgBG {
  width: 100%;
  height: auto;
  position: relative;
  z-index: inherit;
  display: block;
  border-radius: 5px;
  box-shadow: 3px 1px 5px rgba(0, 0, 0, 0.6);
  margin-bottom: 7%;
}

.ImgSettings {
  width: auto;
  position: absolute;
  margin: 1% 1% 0% 0%;
  border-radius: 5px 5px 5px 5px;
  right: 0px;
  top: 0px;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 2;
}

.imgDescription {
  position: absolute;
  left: 0px;
  bottom: 0px;
  z-index: 2;
  width: 100%;
  height: auto;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  resize: none;
  border-radius: 0px 0px 5px 5px;
  padding: 1% 3% 2% 2%;
}
</style>
