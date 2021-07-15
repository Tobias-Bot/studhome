<template>
  <div class="section">
  </div>
</template>

<script>
export default {
  props: ["title", "text"],
  data: function() {
    return {};
  },
  computed: {
      note() {
        return
      },
  },
  methods: {}
};
</script>

<style scoped>
.section {
  width: auto;
  height: auto;
  padding: 1% 2% 1% 1%;
  color: black;
  background-color: rgba(0, 0, 0, 0.4);
  box-shadow: 0px 10px 15px black;
  border-radius: 10px;
}
</style>
