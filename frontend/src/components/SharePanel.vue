<template>
  <div class="share_panel">
    <!-- Share modal -->
    <div
      class="modal fade"
      id="ShareModal"
      tabindex="-1"
      role="dialog"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-body">
            <span class="hint">Скопируй эту ссылку и поделись со своими друзьями в других социальных сетях</span>
            <hr />
            <input :value="post_url" readonly class="form-control textInput" />
          </div>
        </div>
      </div>
    </div>

    <!-- Comment modal -->
    <div
      class="modal fade"
      id="CommentModal"
      tabindex="-1"
      role="dialog"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="CommentModal">
              Комментарий к записи
            </h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-10">
                <textarea
                  v-model="CommentText"
                  class="form-control textInput"
                  rows="5"
                  placeholder="ваш комментарий"
                ></textarea>
              </div>
              <div class="col-2">
                <button
                  type="button"
                  class="btn btn-light btnMain"
                  data-dismiss="modal"
                  @click="SendComment(post_index, post_id)"
                >
                  <i class="fas fa-paper-plane"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="btn-group" role="group">
      <button
        type="button"
        class="btn btn-light"
        data-toggle="modal"
        data-target="#CommentModal"
      >
        <i class="far fa-comment"></i>
        <span v-if="text" class="textOnBtns">комментировать</span>
      </button>
      <button
        type="button"
        class="btn btn-light"
        data-toggle="modal"
        data-target="#ShareModal"
      >
        <i class="fas fa-share-alt"></i>
        <span v-if="text" class="textOnBtns">поделиться</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: ["post_index", "post_id", "text"],
  data: function() {
    return {
      CommentText: "",
      CommentSettings: false
    };
  },
  computed: {
    domain() {
      return this.$store.getters.getDomain;
    },
    post_url() {
      return `http://localhost:8080/post_${this.post_id}`;
    }
  },
  methods: {
    SendComment(post_index, post_id) {
      if (this.CommentText) {
        var CommentText = this.CommentText;
        let UserData = this.$store.getters.getUserData;
        let comment = {
          text: CommentText,
          post: post_id,
          user: UserData.id,
          username: UserData.username,
          children: [],
          likes: "|",
          parent: null
        };

        this.$store.dispatch("SendComment", comment);

        this.CommentText = "";
        this.CommentArea = false;
      } else {
        console.log("this field is empty!");
      }
    }
  }
};
</script>

<style scoped>
.share_panel {
  position: relative;
  right: 0;
  bottom: 0;
  border-radius: 10px;
  width: 100%;
  height: auto;
  text-align: right;
  display: inline-block;
}

.input {
  border: none;
  width: 100%;
  padding-left: 3%;
  padding-right: 3%;
  border-radius: 0px 5px 5px 0px;
}

.textOnBtns {
  font-size: 15px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.9);
}
</style>
