<template>
  <div class="box">
    <div class="row">
      <div class="col-10">
        <div class="notes_block">
          <template v-if="Notes[0]">
            <note
              v-for="(note, index) in Notes"
              :key="index"
              :index="index"
              :note="note"
            ></note>
          </template>
          <template v-else>
            <span style="opacity: 0.7;">нет ни одной заметки</span>
          </template>
        </div>
      </div>
      <div class="col-2">
        <button class="btn" type="button" @click="createNote">
          <i class="fas fa-plus" style="margin: 0% 4% 0% 0%"></i>
          добавить заметку</button
        ><br />
        <!-- <button class="btn" type="button">
          <i class="far fa-square" style="margin: 0% 4% 0% 0%"></i>
          новый раздел</button
        ><br /> -->
      </div>
    </div>
  </div>
</template>

<script>
import note from "../../components/apps/notes/note";

export default {
  components: {
    note
  },
  data: function() {
    return {};
  },
  computed: {
    Notes() {
      return this.$store.getters.getNotes;
    }
  },
  methods: {
    createNote() {
      let note = {
        title: "",
        text: ""
      };

      this.$store.commit("addNote", note);
    }
  }
};
</script>

<style scoped>
.box {
  width: 100vw;
  height: auto;
  overflow: hidden;
  padding: 3% 10% 5% 6%;
}
.notes_block {
  width: 100%;
  height: 85vh;
  overflow-x: hidden;
  overflow-y: auto;
  background-color: #f1f1f1;
  padding: 2% 3% 2% 2%;
  border-radius: 10px 0px 0px 10px;
  box-shadow: 0px 2px 15px black;
}
.btn {
  width: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  margin-bottom: 5%;
  color: white;
  text-align: left;
}
.btn:hover {
  background-color: rgba(0, 0, 0, 0.4);
}
</style>
