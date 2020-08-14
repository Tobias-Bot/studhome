<template>
  <span
    class="dropdown-item"
    :class="isSelected ? markSelected : mark"
    @click="updatePostMark(name); $emit('addMark')"
    >{{ name }}</span
  >
</template>

<script>
export default {
  props: ["name"],
  data: function() {
    return {

      markSelected: "markSelected",
      mark: "mark"
    };
  },
  computed: {
    isSelected() {
      let marks = this.$store.getters.getCreatedPostMarks.join("|");
      if (~marks.indexOf(this.name)) return true
      else return false;
    }
  },
  methods: {
    updatePostMark(name) {
      if (!this.isSelected) {
        this.$store.commit("addCreatedPostMarks", name);
      } else {
        this.$store.commit("deleteCreatedPostMarks", name);
      }
    }
  }
};
</script>

<style scoped>
.mark {
  width: 80%;
  position: relative;
  left: 50%;
  margin: 3.5% 0 3.5% 0;
  transform: translateX(-50%);
  border-radius: 50px;
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.3);
  font-size: 18px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.8);
  text-align: center;
  transition: 0.1s all;
}
.mark:hover {
  cursor: pointer;
  color: white;
  background-color: rgba(0, 0, 0, 0.8);
}

.markSelected {
  width: 80%;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  margin: 3.5% 0 3.5% 0;
  box-shadow: 0px 3px 3px rgba(0, 0, 0, 0.4);
  border-radius: 50px;
  font-size: 18px;
  font-weight: 500;
  text-align: center;
  color: white;
  background-color: rgba(0, 0, 0, 0.9);
}
.markSelected:hover {
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.8);
}
</style>
