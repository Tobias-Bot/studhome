<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-1" style="max-width: 3%;">
        <div class="btn-group-vertical btn-group-sm" role="group">
          <router-link
            active-class="btn btn-active"
            class="btn btn-light"
            to="/apps/text"
          >
            <span>
              <i class="fas fa-pen-alt"></i>
            </span>
          </router-link>
          <router-link
            active-class="btn btn-active"
            class="btn btn-light"
            to="/somewhere"
          >
            <span>
              <i class="fas fa-sticky-note fa-lg"></i>
            </span>
          </router-link>
          <router-link
            active-class="btn btn-active"
            class="btn btn-light"
            to="/somewhere"
          >
            <span>
              <i class="fas fa-tasks fa-lg"></i>
            </span>
          </router-link>
          <router-link
            active-class="btn btn-active"
            class="btn btn-light"
            to="/somewhere"
          >
            <span>
              <i class="fas fa-table fa-lg"></i>
            </span>
          </router-link>
        </div>
      </div>
      <div class="col">
        <iframe src="http://192.168.1.57:8081" align="center">
          Ваш браузер не поддерживает плавающие фреймы :(
        </iframe>
      </div>
      <div class="col-1" style="max-width: 3%;"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "apps",
};
</script>

<style scoped>
iframe {
  width: 100%;
  height: 91vh;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  border: 2px solid rgba(0, 0, 0, 0.3);
  box-shadow: 0 1px 20px rgba(0, 0, 0, 0.7);
}

.row {
  position: relative;
  top: 70px;
}

.btn-group-vertical {
  left: 50%;
  transform: translateX(-50%);
  box-shadow: 0px 0px 15px black;
}

.btn-light {
  font-size: 20px;
  text-align: center;
}
.btn-light:hover {
  box-shadow: 4px 0px white;
}

.btn-active {
  position: relative;
  z-index: 2;
  box-shadow: 5px 1px 12px black;
  background-color: black;
  color: white;
}
</style>
