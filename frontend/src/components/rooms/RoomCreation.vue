<template>
  <div>
    <!-- Room Creation Modal -->
    <div
      class="modal fade"
      id="RoomCreationModal"
      tabindex="-1"
      role="dialog"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="RoomCreationModal">Создание комнаты</h5>
            <button type="button" class="close" data-dismiss="modal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <input
              v-model="RoomName"
              class="form-control textInput"
              placeholder="название комнаты"
            />
            <br />
            <textarea
              v-model="RoomDesc"
              class="form-control textInput"
              row="5"
              placeholder="добавьте описание, если хотите"
            ></textarea>
            <br />
            <template v-if="PicUrl">
              <img :src="PicUrl" />
              <button
                type="button"
                class="btn btn-light btn-sm DeleteCoverBtn btnOption"
                @click="PicUrl = ''"
              >
                удалить обложку
              </button>
            </template>
            <template v-else>
              <button
                type="button"
                class="btn btn-light btn-sm btnOption"
                @click="$refs.file.click()"
              >
                загрузить обложку
              </button>
            </template>
            <input
              type="file"
              accept="image/jpeg, image/gif, image/png"
              ref="file"
              hidden="true"
              @change="handleFileUpload"
            />
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-light btnMain"
              data-dismiss="modal"
              @click="submitRoom"
            >
              создать комнату
            </button>
          </div>
        </div>
      </div>
    </div>

    <div
      class="card"
      type="button"
      data-toggle="modal"
      data-target="#RoomCreationModal"
    >
      <i class="fas fa-plus"></i>
      <br />
      <span class="text">создать комнату</span>
    </div>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      RoomName: "",
      RoomDesc: "",

      PicUrl: "",
      ImgCover: ""
    };
  },
  computed: {
    UserData() {
      return this.$store.getters.getUserData;
    }
  },
  methods: {
    getImagePreviews(file) {
      if (/\.(jpe?g|png|gif)$/i.test(file.name)) {
        let reader = new FileReader();

        reader.addEventListener(
          "load",
          function() {
            this.PicUrl = reader.result;
          }.bind(this),
          false
        );

        reader.readAsDataURL(file);
      }
    },
    handleFileUpload() {
      this.ImgCover = this.$refs.file.files[0];
      this.getImagePreviews(this.ImgCover);
    },
    submitRoom() {
      let formData = new FormData();
      let token = localStorage.getItem("token");
      formData.append("name", this.RoomName);
      formData.append("description", this.RoomDesc);
      formData.append("image", this.ImgCover);
      formData.append("adminname", this.UserData.username);
      formData.append("user", this.UserData.id);

      axios.post(
        "http://127.0.0.1:8000/api/v1/room/create/" + this.UserData.username + "/",
        formData,
        {
          headers: {
            Authorization: "Token " + token,
            "Content-Type": "multipart/form-data"
          }
        }
      );
    }
  }
};
</script>

<style scoped>
.card {
  width: 100%;
  max-height: 40vh;
  background-color: rgba(0, 0, 0, 0.3);
  text-align: center;
  border-radius: 5px;
  border: 3px dashed rgba(0, 0, 0, 0.2);
  color: silver;
  font-size: 30px;
  font-weight: 600;
  padding: 10% 0 10% 0;
  transition: 0.2s all;
}
.card:hover {
  border: 3px dashed rgba(0, 0, 0, 0.4);
  background-color: rgba(0, 0, 0, 0.4);
  cursor: pointer;
  font-size: 35px;
  color: white;
}

img {
  width: 100%;
  height: auto;
  position: relative;
  border-radius: 5px;
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.8);
  z-index: inherit;
}

.DeleteCoverBtn {
  width: auto;
  position: relative;
  border-radius: 5px 5px 5px 5px;
  margin-top: 3%;
}
</style>
