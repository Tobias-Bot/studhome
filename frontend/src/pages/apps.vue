<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-1 appsOptions">
        <div class="btn-group-vertical btn-group-sm" role="group">
          <span
            class="btn btn-light"
            @click="setCurrentApp('http://192.168.1.57:8081')"
          >
            <i class="fas fa-pen-alt"></i>
          </span>
          <span class="btn btn-light" @click="setCurrentApp('')">
            <i class="fas fa-sticky-note fa-lg"></i>
          </span>
          <span class="btn btn-light" @click="setCurrentApp('')">
            <i class="fas fa-tasks fa-lg"></i>
          </span>
          <span class="btn btn-light" @click="setCurrentApp('')">
            <i class="fas fa-table fa-lg"></i>
          </span>
        </div>
      </div>
      <template v-if="currentApp.length">
        <div class="col">
          <iframe :src="currentApp" align="center">
            Ваш браузер не поддерживает плавающие фреймы :(
          </iframe>
        </div>
        <div class="col-1 appsOptions">
          <div class="btnApp" title="закрыть приложение" @click="closeApp">
            <i class="fas fa-times"></i>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
export default {
  name: "apps",
  data: function() {
    return {
      currentApp: "",
    };
  },
  methods: {
    setCurrentApp(url) {
      this.currentApp = url;
    },
    closeApp() {
      this.currentApp = "";
    },
  },
};
</script>

<style scoped>
iframe {
  width: 100%;
  height: 91vh;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  border: 2px solid rgba(0, 0, 0, 0.4);
  box-shadow: 0 1px 20px rgba(0, 0, 0, 0.8);
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
  transition: 0.1s all;
}
.btn-light:hover {
  box-shadow: 4px 0px white;
  background-color: rgba(0, 0, 0, 0.9);
  color: white;
}

.btnApp {
  font-size: 25px;
  padding: 4px;
  background-color: white;
  color: rgba(0, 0, 0, 0.9);
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.5);
  border-radius: 2px;
  transition: 0.1s all;
}
.btnApp:hover {
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.9);
  color: white;
}

.appsOptions {
  max-width: 3%;
}
</style>
