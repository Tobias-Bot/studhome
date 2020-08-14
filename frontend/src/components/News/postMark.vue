<template>
  <div
    :class="[selected ? postMarkSelected : postMark]"
    @click="updatePostMarks(); PostMarksLoader();"
  >
    {{ name }}
  </div>
</template>

<script>
export default {
  props: ["name", "index"],
  name: "postMark",
  data: function() {
    return {
      selected: false,

      postMark: "postMark",
      postMarkSelected: "postMarkSelected"
    };
  },
  methods: {
    updatePostMarks() {
      let vm = this;

      if (!this.selected) {
        this.$store.commit("addPostMark", vm.name);
      } else {
        this.$store.commit("deletePostMark", vm.index);
      }

      this.selected = !this.selected;
    },
    PostMarksLoader() {
      let marks = this.$store.getters.getPostMarks;

      if (marks.length) {
        let token = this.$store.getters.getToken;

        axios
          .get(
            "http://127.0.0.1:8000/api/v1/news/post/marks/?q=|" +
              marks.join("|") +
              "|",
            {
              headers: { Authorization: "Token " + token }
            }
          )
          .then(response => {
            this.$store.commit("setPost", response.data);
          })
          .catch(function(e) {
            console.log(e);
          });
      }
    }
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
