<template>
  <div class="box">
    <div class="row">
      <div class="col-8">
        <h1>{{ "room " + this.$route.params.room_id }}</h1>
      </div>
      <div class="col">
          <chat></chat>
      </div>
    </div>
  </div>
</template>

<script>
import chat from "./chat";

export default {
  name: "room",
  components: {
    chat
  },
  props: [],
  data: function() {
    return {};
  },
  methods: {},
  created() {
    var room = this.$route.params.room;
  }
};
</script>

<style scoped>
</style>
