<template>
  <div id="chat">
    <span class="status">{{ this.status }}</span>
    <div id="dialogArea">
      <template v-if="!this.dialogs.length">
        <h3 style="opacity: 0.6; color: white;">новых сообщений нет</h3>
      </template>
      <template v-else>
        <message v-for="(dialog, i) in dialogs" :key="i" :data="dialog"></message>
      </template>
    </div>
    <div id="inputMesArea">
      <div class="row">
        <div class="col-9">
          <textarea
            class="form-control"
            placeholder="введите сообщение"
            v-model="mes"
            @keyup.enter="sendMessage"
          ></textarea>
        </div>
        <div class="col">
          <div class="btn-group-vertical" role="group">
            <button type="button" class="btn btn-dark" @click="sendMessage">
              <i class="fas fa-paper-plane"></i>
            </button>
            <button type="button" class="btn btn-outline-light">
              <i class="fas fa-paperclip"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import message from "./message";

export default {
  name: "chat",
  components: {
    message
  },
  props: [],
  data: function() {
    return {
      mes: "",
      dialogs: [],
      status: "disconnected",
      chatSocket: ""
    };
  },
  created() {
    this.connect();
  },
  methods: {
    connect() {
      this.chatSocket = new WebSocket(
        "ws://127.0.0.1:8000/ws/chat/" + this.$route.params.room_id + "/"
      );

      this.chatSocket.onopen = () => {
        this.status = "connected";

        this.chatSocket.onmessage = ({ data }) => {
          this.dialogs.push(JSON.parse(data));
        };
      };
    },
    disconnect() {
      this.chatSocket.close();
      this.status = "disconnected";
      this.dialogs.splice(0, this.dialogs.length);
    },
    sendMessage() {
      let message = this.mes;
      let username = this.$store.getters.getUserData.username;

      this.chatSocket.send(
        JSON.stringify({
          message,
          username,
        })
      );

      this.mes = "";
    }
  }
};
</script>

<style scoped>
#chat {
  width: 100%;
  height: 82vh;
  border-radius: 7px;
  padding: 2% 0% 0% 3%;
  box-shadow: 0px 3px 50px rgba(0, 0, 0, 0.9);
  background-color: rgba(0, 0, 0, 0.3);
}

.status {
  color: white;
  font-size: 18px;
}

#inputMesArea {
  width: 100%;
  height: auto;
  position: absolute;
  bottom: 2%;
}

textarea {
  height: 10vh;
  color: white;
  font-size: 20px;
  font-weight: 500;
  resize: none;
  border: none;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 6px;
  padding: 1% 3% 2% 2%;
  transition: 0.2s all;
}

#dialogArea {
  overflow-y: auto;
  overflow-x: hidden;
  width: 100%;
  height: 78%;
}
</style>
