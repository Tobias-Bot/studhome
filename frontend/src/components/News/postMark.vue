<template>
  <router-link
    :to="{
      name: 'AllPosts',
      params: { topic: 'marks' }
    }"
    style="text-decoration: none;"
  >
    <div
      :class="[selected ? postMarkSelected : postMark]"
      @click="updatePostMarks()"
    >
      {{ name }}
    </div>
  </router-link>
</template>

<script>
export default {
  props: ["name", "index"],
  name: "postMark",
  data: function() {
    return {
      selected: false,

      postMark: "postMark",
      postMarkSelected: "postMarkSelected",
    };
  },
  methods: {
    updatePostMarks() {
      let vm = this;

      if (!this.selected) {
        this.$store.commit("addPostMark", { name: vm.name, id: vm.index });
      } else {
        this.$store.commit("deletePostMark", vm.index);
      }

      this.selected = !this.selected;

      this.$emit('loadPostsByMarks');
    },
  }
};
</script>

<style scoped>
.postMark {
  position: relative;
  display: block;
  padding: 0 5% 1% 5%;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.8);
  margin-bottom: 7%;
  background: white;
  color: rgba(0, 0, 0, 0.9);
  box-shadow: 0 2px 1.5px rgba(0, 0, 0, 0.6);
  transition: 0.1s all;
}
.postMark:hover {
  background-color: rgba(0, 0, 0, 0.9);
  color: white;
}

.postMarkSelected {
  position: relative;
  display: block;
  padding: 0 5% 1% 5%;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  margin-bottom: 7%;
  background: rgba(0, 0, 0, 0.92);
  box-shadow: 0 2px 1.5px rgba(0, 0, 0, 0.6);
  color: white;
}
</style>
