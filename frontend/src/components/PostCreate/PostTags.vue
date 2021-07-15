<template>
  <div class="card">
    <div class="card-header">
      <h5>Облако тегов</h5>
    </div>
    <div class="card-body">
      <input
        v-model="PostTag"
        class="form-control textInput"
        type="text"
        placeholder="введите тег и нажмите enter"
        style="margin-bottom: 5%;"
        @keyup.enter="addPostTag(); $emit('changed');"
        @keyup.space="PostTag = PostTag.replace('  ', ' ')"
      />
      <span v-show="!tags.length" class="hint"
        >вы не добавили ни одного тега</span
      >
      <span v-for="(tag, index) in tags" class="tag">
        {{ tag }}
        <i
          class="fas fa-times-circle"
          style="opacity: 0.9;"
          @click="tags.splice(index, 1)"
        ></i>
      </span>
    </div>
  </div>
</template>

<script>
export default {
  props: ["tags"],
  components: {},
  data: function() {
    return {
      PostTag: "",
      spaces: 0,
    };
  },
  computed: {},
  methods: {
    addPostTag() {
      let tag = this.PostTag;
      var vm = this;
      
      if (tag && tag !== " ") {

        if (tag.indexOf(" ") == 0) tag = tag.substring(1, tag.length);
        if (tag.indexOf(" ") == tag.length - 1) tag = tag.substring(0, tag.length - 1);
        this.tags.push(tag);
      }

      this.PostTag = "";
    }
  }
};
</script>

<style scoped>

.tag {
  float: left;
  width: auto;
  padding: 0.5% 1% 0.5% 1%;
  background-color: rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  text-align: center;
  font-size: 16px;
  font-weight: 550;
  box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.4);
  margin: 0.8% 0.8% 0.8% 0.8%;
  color: rgba(0, 0, 0, 0.8);
  transition: 0.2s all;
}
.tag:hover {
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
}
</style>
