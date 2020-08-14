<template>
<div>
  <div class="progressbar"></div>
  <div class="scrollPath"></div>
</div>
</template>

<script>
export default {
  props: ["colors"],
  data: function() {
    return {};
  },
  methods: {}
};
</script>

<style scoped>

.scrollPath {
    position: absolute;
    top: 7.5%;
    right: 0;
    width: 2%;
    height: 100%;
    background: blue;
}

</style>
