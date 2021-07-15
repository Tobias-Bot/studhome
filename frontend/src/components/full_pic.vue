<template>
  <div class="cover">
    <div class="modal-dialog modal-xl">...</div>
    <div class="row">
      <div class="col-8" style="height: 85vh;">
        <img
          :src="'http://127.0.0.1:8000' + CurrImg.image"
          :class="[isHorizontal ? HorizontalImgStyle : VerticalImgStyle]"
          alt="image"
          ref="pic"
        />
      </div>
      <div class="col-4">
        <div class="card">
          <div class="card-body">
            <h5>{{ UserName }}</h5>
          </div>
        </div>
        <div v-if="CurrImg.text" class="card">
          <div class="card-body">
            <div class="photoDescription">
              <i>{{ CurrImg.text }}</i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      isHorizontal: false,
      HorizontalImgStyle: "img_horizontal",
      VerticalImgStyle: "img_vertical",
    }
  },
  mounted() {
    let h = this.$refs.pic.naturalHeight;
    let w = this.$refs.pic.naturalWidth;

    if (h >= w) {
      this.isHorizontal = false;
    }
    else {
      this.isHorizontal = true;
    }
  },
  computed: {
    CurrImg() {
      return this.$route.params.pic;
    },
    UserName() {
      return this.$route.params.username;
    }
  },
  methods: {
  }
};
</script>

<style scoped>
img {
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0px 1px 15px black;
  border-radius: 5px;
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto 0;
}
.img_horizontal {
  width: 70%;
  height: auto;
}
.img_vertical {
  height: 85%;
  width: auto;
}

.photoDescription {
  max-height: 40vh;
  overflow-y: auto;
  overflow-x: hidden;
  width: 100%;
  padding: 3% 7% 3% 4%;
  background-color: #fafafa;
  color: #3c3c3c;
  box-shadow: 0px 1px 10px silver;
  border-radius: 3px;
  text-align: justify;
}

.card {
  margin-left: 3%;
  margin-bottom: 3%;
}

.cover {
  width: 100%;
  height: 100vh;
  padding: 3% 150px 2.5% 150px;
  background-color: rgba(0, 0, 0, 0.7);
  position: relative;
  z-index: 1;
}
</style>
