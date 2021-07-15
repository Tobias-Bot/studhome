<template>
  <div :class="[ data.username == this.username ? MyMessage : OtherMessage ]">
    <span class="username">
      {{ data.username }}
    </span>
    <br />
    <span class="text">
      {{ data.message }}
    </span>
  </div>
</template>

<script>
export default {
  name: "message",
  props: ["data"],
  data: function() {
    return {
      MyMessage: 'MyMessage',
      OtherMessage: 'OtherMessage',
    };
  },
  computed: {
    username() {
      return this.$store.getters.getUserData.username;
    },
  },
  methods: {}
};
</script>

<style scoped>
.MyMessage {
  max-width: 50%;
  width: auto;
  padding: 0.5% 3% 1.5% 3%;
  box-shadow: 2px 4px 2px rgba(0, 0, 0, 0.6);
  background-color: rgba(255, 255, 255, 0.8);
  display: table;
  border-radius: 1px 15px 1px 20px;
  margin: 3% 5% 0 auto;
}

.OtherMessage {
  max-width: 50%;
  width: auto;
  padding: 1% 3% 1.5% 3%;
  box-shadow: 2px 4px 2px rgba(0, 0, 0, 0.6);
  background-color: white;
  display: table;
  margin: 5% auto 0 2%;
  border-radius: 15px 1px 20px 1px;
}

.text {
  font-size: 16px;
  font-weight: 550;
  word-break: break-word;
}

.username {
  opacity: 0.7;
  color: black;
  font-size: 12px;
}
</style>
