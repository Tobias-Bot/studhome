<template>
  <div class="card">
    <div class="card-body">
      <router-link
        :to="{
          name: 'room',
          params: { room_id: room.id, room }
        }"
      >
        <div id="wrapper">
          <div class="roomName">{{ room.name }}</div>
          <img :src="room.image" id="cover" />
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  props: ["room"],
  data: function() {
    return {};
  },
  methods: {}
};
</script>

<style scoped>
#wrapper {
  width: 100%;
  height: auto;
  position: relative;
  bottom: 0vh;
  transition: 0.2s all;
}
#wrapper:hover {
  cursor: pointer;
  bottom: 1vh;
}

#cover {
  max-height: 35vh;
  width: 100%;
  height: auto;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.8);
  position: relative;
  z-index: 1;
  border-radius: 5px;
}

.roomName {
  width: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  color: white;
  font-size: 20px;
  font-weight: bold;
  padding: 1% 0% 2% 2%;
  border-radius: 5px 5px 0px 0px;
  position: absolute;
  z-index: 2;
  top: 0px;
  left: 0px;
}

.roomDesc {
  font-size: 14px;
  margin: 5% 0% 0% 7%;
}

.btn-light {
  width: 100%;
  box-shadow: 0px 2px 5px silver;
}
</style>
