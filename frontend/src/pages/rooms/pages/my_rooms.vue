<template>
  <div class="box-with-tools">
    <div class="card-columns">
      <roomView v-for="(room, i) in rooms" :key="i" :room="room"></roomView>
      <RoomCreation></RoomCreation>
    </div>
  </div>
</template>

<script>
import roomView from "../../../components/rooms/roomView";
import RoomCreation from "../../../components/rooms/RoomCreation";

export default {
  components: {
    roomView,
    RoomCreation,
  },
  data: function() {
    return {
      rooms: []
    };
  },
  computed: {},
  methods: {},
  created() {
    let username = this.$store.getters.getUserData.username;
    let token = localStorage.getItem("token");

    axios
      .get("http://127.0.0.1:8000/api/v1/room/" + username + "/", {
        headers: { Authorization: "Token " + token }
      })
      .then(response => {
        this.rooms = response.data;
      });
  }
};
</script>

<style scoped>
.card {
  margin-bottom: 4%;
}
</style>
