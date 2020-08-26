<template>
  <div>
    <!-- update comment modal -->
    <div
      class="modal fade"
      :id="'UpdateCommentModal' + args.id"
      tabindex="-1"
      role="dialog"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h4>Редактирование комментария</h4>
            <button type="button" class="close" data-dismiss="modal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-10">
                <textarea
                  class="form-control textInput"
                  rows="4"
                  v-model="EditCommText"
                  placeholder="ваш комментарий"
                ></textarea>
              </div>
              <div class="col-2">
                <button
                  type="button"
                  class="btn btn-light btnMain"
                  data-dismiss="modal"
                  @click="EditCommentText"
                >
                  <i class="fas fa-paper-plane"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="comment">
      <div class="row">
        <div class="col-10">
          <router-link
            :to="{ name: 'profile', params: { username: args.username } }"
          >
            <span class="username" @click="LoadProfile">{{
              args.username
            }}</span>
          </router-link>
          <br />
          <span class="commentText">{{ args.text }}</span>
        </div>
        <div class="col-2">
          <div
            class="btn-group-vertical"
            role="group"
            style="float: right; opacity: 0.7;"
          >
            <template v-if="args.user === UserData.id">
              <button
                data-toggle="tooltip"
                data-placement="right"
                title="удалить"
                type="button"
                class="btn btn-light btn-sm"
                @click="DeleteComment(post_id, args.id, index)"
              >
                <i class="fas fa-times-circle"></i>
              </button>
              <button
                type="button"
                title="редактировать"
                data-toggle="modal"
                :data-target="'#UpdateCommentModal' + args.id"
                class="btn btn-light btn-sm"
              >
                <i class="fas fa-pen"></i>
              </button>
            </template>
            <template v-else>
              <button
                type="button"
                data-toggle="tooltip"
                data-placement="right"
                title="ответить"
                class="btn btn-light btn-sm"
                @click="CommentArea = !CommentArea"
              >
                <span v-if="args.children.length" class="optionCounts">{{
                  args.children.length
                }}</span>
                <i class="far fa-comment-dots"></i>
              </button>
              <button
                type="button"
                data-toggle="tooltip"
                data-placement="right"
                title="нравится"
                class="btn btn-light btn-sm"
                @click="LikeComment(args)"
              >
                <span v-if="CommentLikesCount" class="optionCounts">{{
                  CommentLikesCount
                }}</span>
                <i v-if="!isLiked" class="far fa-heart"></i>
                <i v-else class="fas fa-heart"></i>
              </button>
            </template>
          </div>
        </div>
      </div>
      <template v-if="CommentArea">
        <div class="row" style="padding-top: 1%;">
          <div class="col-10">
            <textarea
              class="form-control textInput"
              rows="4"
              placeholder="комментарий"
              v-model="ReplyCommText"
            ></textarea>
          </div>
          <div class="col">
            <button
              type="button"
              class="btn btn-light btnOption"
              style="font-size: 14px; opacity: 0.6;"
              @click="CommentArea = !CommentArea"
            >
              <i class="fas fa-times-circle"></i>
            </button>
            <br />
            <button
              type="button"
              class="btn btn-light btnOption"
              data-dismiss="modal"
              @click="ReplyComment(post_id, args.id)"
            >
              <i class="fas fa-paper-plane"></i>
            </button>
          </div>
        </div>
      </template>
      <template v-if="args.children">
        <comment
          v-for="(child, id) in args.children"
          :key="'child' + child.id"
          :index="id"
          :post_id="post_id"
          :args="child"
          :mates="args.children"
        ></comment>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: "comment",
  props: ["index", "post_id", "args", "mates"],
  data: function() {
    return {
      CommentArea: false,
      ReplyCommText: "",
      EditCommText: ""
    };
  },
  mounted() {
    this.EditCommText = this.args.text;
  },
  computed: {
    UserData() {
      return this.$store.getters.getUserData;
    },
    Comments() {
      return this.$store.getters.getCurrentComms;
    },
    CommentLikesCount() {
      if (this.args.likes && this.args.likes.length > 1) {
        let len = this.args.likes.length;
        return this.args.likes.substring(1, len - 1).split("|").length;
      } else {
        return 0;
      }
    },
    isLiked() {
      if (
        this.args.likes &&
        this.args.likes.indexOf(this.UserData.username) !== -1
      )
        return true;
      else {
        return false;
      }
    }
  },
  methods: {
    DeleteComment(post_id, comm_id, comm_index) {
      let token = this.$store.getters.getToken;
      let domain = this.$store.getters.getDomain;

      axios
        .delete(`${domain}/api/v1/news/post/${post_id}/comment/${comm_id}/`, {
          headers: { Authorization: "Token " + token }
        })
        .catch(function(e) {
          console.log(e);
        });

      this.$store.commit("deleteCurrentComm", null);
      this.mates.splice(comm_index, 1);
    },
    ReplyComment(post_id, parent_id) {
      if (this.ReplyCommText) {
        let text = this.ReplyCommText;
        let UserData = this.$store.getters.getUserData;

        let comment = {
          text,
          post: post_id,
          user: UserData.id,
          username: UserData.username,
          children: [],
          likes: "|",
          parent: parent_id
        };

        this.$store.dispatch("SendComment", comment).then(data => {
          this.args.children.push(data);
        });

        this.ReplyCommText = "";
        this.CommentArea = false;
      } else {
        console.log("this field is empty!");
      }
    },
    LikeComment(comm) {
      let username = this.UserData.username;
      console.log(comm.id);

      if (!this.isLiked) {
        comm.likes += `${username}|`;
      } else {
        comm.likes = comm.likes.replace(`|${username}|`, "|");
      }

      this.UpdateComment(comm);
    },
    EditCommentText() {
      if (this.EditCommText) {
        console.log(this.args);
        this.args.text = this.EditCommText;

        this.UpdateComment(this.args);

        this.EditCommText = "";
      }
    },
    UpdateComment(comm) {
      let token = this.$store.getters.getToken;
      let domain = this.$store.getters.getDomain;

      axios
        .put(`${domain}/api/v1/news/comment_update/${comm.id}/`, comm, {
          headers: { Authorization: "Token " + token }
        })
        .catch(function(e) {
          console.log(e);
        });
    },
    LoadProfile() {
      this.$store.commit("dropUserPosts");
      this.$store.commit("dropUserSubs");
      this.$store.commit("setProfileTab", 'description');
      this.$store.commit("setHash", '');
    }
  }
};
</script>

<style scoped>
.comment {
  margin: 2% 0% 0.5% 0%;
  padding-left: 1.5%;
  padding-bottom: 3%;
  margin-right: 2%;
  border-left: 3px solid rgba(0, 0, 0, 0.5);
  border-radius: 5px 3px 15px 0px;
  background-color: #fafafa;
  text-align: left;
  box-shadow: -1px 3px 15px rgba(0, 0, 0, 0.2);
}

.username {
  opacity: 0.8;
  font-size: 14px;
  font-weight: 400;
  text-decoration: none;
  transition: 0.1s all;
}
.username:hover {
  opacity: 1;
}

.optionCounts {
  display: inline-block;
  font-size: 11px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.7);
}

.commentText {
  width: auto;
  font-size: 16px;
  color: rgba(0, 0, 0, 0.8);
}
</style>
