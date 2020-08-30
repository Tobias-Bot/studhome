<template>
  <div class="tool_bar">
    <div class="btn-group-vertical" role="group">
      <button class="btn btn-outline-dark" @click="StyleText('bold')">
        <i class="fas fa-bold"></i>
      </button>
      <button class="btn btn-outline-dark" @click="StyleText('italic')">
        <i class="fas fa-italic"></i>
      </button>
      <button class="btn btn-outline-dark" @click="StyleText('underline')">
        <i class="fas fa-underline"></i>
      </button>
      <button class="btn btn-outline-dark" @click="StyleText('strikethrough')">
        <i class="fas fa-strikethrough"></i>
      </button>
      <button
        class="btn btn-outline-dark"
        @click="StyleText('insertUnorderedList')"
      >
        <i class="fas fa-list-ul"></i>
      </button>
      <button
        class="btn btn-outline-dark"
        @click="StyleText('insertOrderedList')"
      >
        <i class="fas fa-list-ol"></i>
      </button>
      <button
        class="btn btn-outline-dark"
        @click="setTextBG('hiliteColor')"
      >
        <i class="fas fa-highlighter">
          <div class="btnLED" :style="'background-color:' + ColorBase"></div>
        </i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: ["HighLighterColor", "NoteColor"],
  data: function() {
    return {
      Color: this.HighLighterColor,
      isColored: false
    };
  },
  computed: {
    ColorBase() {
      return this.HighLighterColor;
    }
  },
  methods: {
    StyleText(style) {
      if (style == "hiliteColor") {
        document.execCommand("styleWithCSS", false, true);
        document.execCommand(style, false, this.Color);
        document.execCommand("styleWithCSS", false, false);
      } else document.execCommand(style, false, null);
    },
    setTextBG(style) {
      if (!this.isColored) {
        this.Color = this.ColorBase;
        this.isColored = true;
      } else {
        this.Color = this.NoteColor;
        this.isColored = false;
      }

      this.StyleText(style, this.Color);
    },
    setTextColor() {
      let color = this.$refs.TextColorInput.value;
      this.TextColor = color;
    }
  }
};
</script>

<style scoped>
.tool_bar {
  width: auto;
  height: auto;
  padding: 0.4% 0.4% 0.4% 0.4%;
  border-radius: 5px;
  background-color: white;
  left: 20%;
  position: fixed;
}

.btnLED {
  display: inline-block;
  width: 7px;
  height: 7px;
  border: 1px solid black;
  border-radius: 100px;
}

.btn-group-vertical {
  border-radius: 5px;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.7);
}
</style>
