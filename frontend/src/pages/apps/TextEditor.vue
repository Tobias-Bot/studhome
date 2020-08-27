<template>
  <div class="row">
    <div class="col-11 cover">
      <div class="mainTools">
        <div class="btn-group" role="group">
          <button type="button" class="btn btn-light" @click="Render('bold')">
            <i class="fas fa-bold"></i>
          </button>
          <button type="button" class="btn btn-light" @click="Render('italic')">
            <i class="fas fa-italic"></i>
          </button>
          <button
            type="button"
            class="btn btn-light"
            @click="Render('underline')"
          >
            <i class="fas fa-underline"></i>
          </button>
          <button
            type="button"
            class="btn btn-light"
            @click="Render('strikethrough')"
          >
            <i class="fas fa-strikethrough"></i>
          </button>
        </div>
        <div class="btn-group" role="group">
          <button
            type="button"
            class="btn btn-light"
            @click="Render('justifyLeft')"
          >
            <i class="fas fa-align-left"></i>
          </button>
          <button
            type="button"
            class="btn btn-light"
            @click="Render('justifyRight')"
          >
            <i class="fas fa-align-right"></i>
          </button>
          <button
            type="button"
            class="btn btn-light"
            @click="Render('justifyCenter')"
          >
            <i class="fas fa-align-center"></i>
          </button>
          <button
            type="button"
            class="btn btn-light"
            @click="Render('justifyFull')"
          >
            <i class="fas fa-align-justify"></i>
          </button>
        </div>
        <div class="btn-group" role="group">
          <button
            type="button"
            class="btn btn-light"
            @click="Render('insertUnorderedList')"
          >
            <i class="fas fa-list-ul"></i>
          </button>
          <button
            type="button"
            class="btn btn-light"
            @click="Render('insertOrderedList')"
          >
            <i class="fas fa-list-ol"></i>
          </button>
        </div>
        <div class="btn-group" role="group">
          <button
            type="button"
            class="btn btn-light dropdown-toggle"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            <i class="fas fa-heading"></i>
          </button>
          <div class="dropdown-menu">
            <button
              class="btn btn-light subBtn"
              @click="Render('formatBlock', 'h1')"
            >
              H1
            </button>
            <button
              class="btn btn-light subBtn"
              @click="Render('formatBlock', 'h2')"
            >
              H2
            </button>
            <button
              class="btn btn-light subBtn"
              @click="Render('formatBlock', 'h3')"
            >
              H3
            </button>
          </div>
        </div>
        <div class="editorSettings">
          <i
            v-show="EditMode"
            class="fas fa-toggle-on"
            @click="EditMode = false"
          ></i>
          <i
            v-show="!EditMode"
            class="fas fa-toggle-off"
            @click="EditMode = true"
          ></i>
        </div>
      </div>
      <div class="workSpace">
        <div
          v-for="(page, i) in pages"
          :key="i"
          v-html="page.content"
          class="list"
          :contenteditable="EditMode ? true : false"
          @paste="DeleteStyles"
        >
        </div>
      </div>
    </div>
    <div class="col-1">
      <router-link class="btnSettingApp" title="закрыть приложение" to="/apps">
        <i class="fas fa-times"></i>
      </router-link>
      <hr />
      <div class="btnSettingApp" title="сохраненное">
        <i class="fas fa-archive"></i>
      </div>
      <div class="btnSettingApp" title="создать" @click="CreateNewDoc">
        <i class="far fa-plus-square"></i>
      </div>
      <hr />
      <div class="btnSettingApp" title="настройки">
        <i class="fas fa-sliders-h"></i>
      </div>
      <div class="btnSettingApp" title="о приложении">
        <i class="far fa-question-circle"></i>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  data: function() {
    return {
      EditMode: true,
    };
  },
  computed: {
    pages() {
      return this.$store.getters.getPages;
    }
  },
  methods: {
    CreateNewDoc() {
      this.$store.dispatch("InitDB", "app-TextEditor");

      this.$store.commit('setPage', { content: '' });
    },
    DeleteStyles(event) {
      event.preventDefault();
      let text = (event.originalEvent || event).clipboardData.getData(
        "text/plain"
      );
      document.execCommand("insertText", false, text);
    },
    Render(prop, option) {
      document.execCommand(prop, false, option);
    }
  }
};
</script>

<style scoped>
.editorSettings {
  position: absolute;
  right: 1%;
  top: 0;
  margin: 0 auto;
  font-size: 25px;
}
.editorSettings:hover {
  cursor: pointer;
}

.subBtn {
  font-weight: 500;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
  margin: 0 1%;
}

.workSpace {
  position: absolute;
  left: 0;
  right: 0;
  padding: 6% 0 5% 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
}

.list {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  padding: 2% 2%;
  width: 36%;
  min-height: 82%;
  border-radius: 5px;
  border: none;
  outline: none;
  background-color: white;
  box-shadow: 1px 2px 5px rgba(0, 0, 0, 0.5);
}

.mainTools {
  position: absolute;
  left: 0;
  right: 0;
  z-index: 2;
  width: 100%;
  padding: 0.4%;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.7);
}

.btn-group {
  margin-left: 0.5%;
}

.cover {
  width: 100%;
  max-height: 91vh;
  height: 91vh;
  overflow: hidden;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  border: 2px solid rgba(0, 0, 0, 0.3);
  box-shadow: 0 1px 20px rgba(0, 0, 0, 0.7);
}

.row {
  position: relative;
  top: 0;
}

.btnSettingApp {
  display: block;
  position: relative;
  margin-bottom: 5%;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  color: white;
  font-size: 40px;
  opacity: 0.5;
  transition: 0.2s all;
}
.btnSettingApp:hover {
  cursor: pointer;
  opacity: 1;
}
</style>
