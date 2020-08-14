<template>
  <div class="box-with-tools">
    <template v-if="!Posts[0]">
      <div class="hint-card">список закладок пуст</div>
    </template>
    <template v-else>
      <div class="card-columns">
        <post
          v-for="(post, id) in Posts"
          :key="id"
          :post="post"
          :post_index="id"
        ></post>
      </div>
    </template>
  </div>
</template>

<script>
import post from "../../components/post";

export default {
  name: "bookmarks",
  components: {
    post
  },
  data() {
    return {};
  },
  computed: {
    Posts() {
      return this.$store.getters.getUserBookmarks;
    }
  },
  methods: {}
};
</script>

<style scoped>

.hint-card {
  width: 30%;
  left: 50%;
  transform: translateX(-50%);
  position: absolute;
  top: 30%;
  margin: auto 0;
  background-color: white;
  color: rgba(0, 0, 0, 0.8);
  text-align: center;
  box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.5);
  border-radius: 5px;
  font-size: 25px;
  font-weight: 500;
  padding: 2% 4% 2% 4%;
}

</style>
