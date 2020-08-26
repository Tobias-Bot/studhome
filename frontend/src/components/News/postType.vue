<template>
  <router-link
    :to="{
      name: 'AllPosts',
      params: { topic: 'type' }
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
      postMark: "postMark",
      postMarkSelected: "postMarkSelected",
    };
  },
  computed: {
    selected() {
      let tags = this.$store.getters.getPostTypes;
      let response = false;

      for (let tag of tags) {
        if (~tag.name.indexOf(this.name)) response = true;
      }

      return response;
    }
  },
  methods: {
    updatePostMarks() {
      let vm = this;

      if (!this.selected) {
        this.$store.commit("addPostType", { name: vm.name, id: vm.index });
      } else {
        this.$store.commit("deletePostType", vm.index);
      }

      this.$emit('loadPostsByTypes');
    },
  }
};
</script>

<style scoped>
.postMark {
  position: relative;
  display: block;
  padding: 0 5% 1% 5%;
  border-radius: 15px 3px 15px 3px;
  border: 1px solid rgba(0, 0, 0, 0.8);
  margin-bottom: 5%;
  background: white;
  font-size: 20px;
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
  border-radius: 3px 15px 3px 15px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  margin-bottom: 5%;
  font-size: 20px;
  background: rgba(0, 0, 0, 0.92);
  box-shadow: 0 2px 1.5px rgba(0, 0, 0, 0.6);
  color: white;
}
</style>
