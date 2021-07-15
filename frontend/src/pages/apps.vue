<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-0">
        <div class="btn-group-vertical btn-group-sm" role="group">
          <router-link active-class="btn btn-active" class="btn btn-dark" to="/apps/settings">
            <span>
              <i class="fas fa-ellipsis-h"></i>
            </span>
          </router-link>
          <router-link active-class="btn btn-active" class="btn btn-light" to="/apps/text">
            <span>
              <i class="fas fa-pen-alt"></i>
            </span>
          </router-link>
          <router-link active-class="btn btn-active" class="btn btn-light" to="/apps/notes">
            <span>
              <i class="fas fa-sticky-note fa-lg"></i>
            </span>
          </router-link>
          <router-link active-class="btn btn-active" class="btn btn-light" to="/apps/tasks">
            <span>
              <i class="fas fa-tasks fa-lg"></i>
            </span>
          </router-link>
          <router-link active-class="btn btn-active" class="btn btn-light" to="/apps/timetable">
            <span>
              <i class="fas fa-table fa-lg"></i>
            </span>
          </router-link>
        </div>
      </div>
      <div class="col-11">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "apps"
};
</script>

<style scoped>

.btn-group-vertical {
  box-shadow: 0px 0px 15px black;
}

.btn-light {
  height: auto;
  font-size: 16px;
  text-align: center;
}
.btn-light:hover {
  box-shadow: 3px 0px white;
}

.btn-active {
  box-shadow: 5px 1px 12px black;
  background-color: black;
  color: white;
  position: relative;
  z-index: 2;
}

</style>
