<template>
  <router-link
    :to="{
      name: 'post',
      params: { post_id: post.id, post: post, post_index: index }
    }"
    style="text-decoration: none;"
  >
    <template v-if="post.text">
      <div
        class="text"
        :style="
          'background: linear-gradient(to left bottom, transparent 50%, rgba(0,0,0,0.3) 0) no-repeat 100% 0 / 15px 15px, linear-gradient(-135deg, transparent 11px,' +
            post.note_color +
            ' 0);'
        "
        @click="addUserView(post.id, index)"
      >
        <template
          v-if="
            (post.text.includes('</b>') ||
              post.text.includes('</i>') ||
              post.text.includes('</u>') ||
              post.text.includes('<br>') ||
              post.text.includes('</strike>') ||
              post.text.includes('</ul>') ||
              post.text.includes('</ol>') ||
              post.text.includes('</span>')) &&
              !post.text.includes('</script>')
          "
        >
          <span
            v-html="post.text.substring(0, NoteHeight)"
            :style="'color:' + post.text_color + ';'"
          ></span>
          <span
            v-if="post.text.length > NoteHeight"
            :style="'color:' + post.text_color + ';'"
            >. . .</span
          >
        </template>
        <template v-else>
          <span :style="'color:' + post.text_color + ';'">
            {{ post.text.substring(0, NoteHeight) }}
          </span>
          <span
            v-if="post.text.length > NoteHeight"
            :style="'color:' + post.text_color + ';'"
            >. . .</span
          >
        </template>
      </div>
    </template>
  </router-link>
</template>

<script>
export default {
  props: ["post", "index"],
  data: function() {
    return {
      MinLen: 350
    };
  },
  computed: {
    NoteHeight() {
      let H;

      if (this.post.text.length < this.MinLen)
        H = Math.round(this.post.text.length + this.MinLen);
      else H = Math.round((this.post.text.length + this.MinLen) * 0.1);

      return H;
    },
  },
  methods: {
    addUserView(post_id, post_index) {
      let data = {
        post_id,
        post_index
      }

      console.log(data);

      this.$store.dispatch('addUserView', data);
    },
  }
};
</script>

<style scoped>
.text {
  width: 100%;
  height: auto;
  color: black;
  display: inline-block;
  position: relative;
  left: 0;
  top: 0;
  padding: 4% 6% 4% 3.5%;
  background: white;
  border-radius: 3px;
  transition: 0.1s all;
  filter: drop-shadow(2px 3px 5px rgba(0, 0, 0, 0.4));
}
.text:before {
  content: " ";
  position: absolute;
  top: 0px;
  right: 0px;
  background: linear-gradient(
      to left bottom,
      transparent 50%,
      rgba(0, 0, 0, 0) 0
    )
    100% 0 no-repeat;
  width: 15px;
  height: 15px;
  transform: rotate(180deg);
}
</style>
