<template>
  <div class="note">
    <div class="row">
      <div class="col-10">
        <template v-if="!editMode">
          <h4>{{ note.title }}</h4>
          <i>{{ note.text }}</i>
        </template>
        <template v-else>
          <input type="text" v-model="inputTitle" class="form-control" placeholder="заголовок"/>
          <br>
          <textarea v-model="inputText" class="form-control" rows="5" placeholder="текст заметки"></textarea>
        </template>
      </div>
      <div class="col-2">
        <template v-if="!editMode">
          <i
            class="far fa-times-circle"
            style="opacity: 0.4; float: right; margin-bottom: 30%;"
            @click="deleteNote(index)"
          ></i><br>
          <i
            class="far fa-edit"
            style="opacity: 0.4; float: right;"
            @click="editMode = !editMode"
          ></i>
        </template>
        <button
          v-else
          class="btn btn-light"
          type="button"
          style="float: left;"
          @click="saveNote(index)"
        >
          <i class="far fa-check-circle"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["index", "note"],
  data: function() {
    return {
      editMode: true,
      inputTitle: '',
      inputText: '',
    };
  },
  computed: {
  },
  methods: {
    deleteNote(i) {
      this.$store.commit("deleteNote", i);
    },
    saveNote(i) {
        let title = this.inputTitle;
        let text = this.inputText;
        let note = {
            title: title,
            text: text
        }
        
        this.$store.commit('setNote', { index: i, data: note });

        this.editMode = !this.editMode
    },
  }
};
</script>

<style scoped>
.note {
  width: 30%;
  height: auto;
  padding: 2% 2% 2% 2.5%;
  margin: 1% 1% 1% 1%;
  background-color: white;
  color: black;
  box-shadow: 0px 5px 10px silver;
  border-radius: 7px;
  float: left;
  transition: 0.2s all;
  position: relative;
  z-index: 1;
}
.note:hover {
  background-color: #f8f8ff;
  box-shadow: 0px 10px 12px silver;
}
</style>
