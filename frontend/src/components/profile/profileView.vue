<template>
  <div class="card">
    <div class="card-body">
      <div class="row">
        <div class="col-4">
          <router-link
            :to="{
              name: 'profile',
              params: { username: blog.username, blog: blog }
            }"
          >
            <img class="avatar" :src="blog.avatar" />
          </router-link>
        </div>
        <div class="col">
          <div class="block">
            <router-link
              class="username"
              :to="{
                name: 'profile',
                params: { username: blog.username, blog: blog }
              }"
              >{{ blog.username }}</router-link
            >
          </div>
          <div v-if="blog.status" class="block">
            <div class="status">{{ blog.status }}</div>
          </div>
          <div v-else-if="blog.bio" class="block">
            <div class="status">{{ blog.bio.substring(0, maxLen) }}</div>
            <span v-if="blog.bio.length > maxLen">...</span>
          </div>
        </div>
        <div class="col-2">
          <div class="btn-group-vertical" role="group">
            <button class="btn btn-ligth btn-sm btnOption"></button>
            <button class="btn btn-ligth btn-sm btnOption"></button>
            <button class="btn btn-ligth btn-sm btnOption"></button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["blog"],
  name: "blog",
  data: function() {
    return {
      maxLen: 100
    };
  },
  computed: {},
  methods: {}
};
</script>

<style scoped>
.avatar {
  position: relative;
  top: 0;
  left: 0;
  width: 100%;
  border-radius: 10px;
  border: 3px solid white;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.3);
}
.avatar:hover {
  cursor: pointer;
}

.status {
  font-style: italic;
  font-weight: 400;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.8);
}

.block {
  width: 100%;
  display: block;
  border-radius: 5px;
  padding: 1% 3% 1% 3%;
  margin-bottom: 4%;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
}
</style>
