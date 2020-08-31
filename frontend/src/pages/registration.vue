<template>
  <div class="box">
    <div class="card">
      <div class="card-header">
        <h5>Регистрация</h5>
      </div>
      <div class="card-body">
        <h6>Имя пользователя</h6>
        <input
          v-model="UserData.username"
          type="name"
          class="form-control textInput"
          required
        />
        <br />
        <h6>Email</h6>
        <input
          v-model="email"
          type="email"
          class="form-control textInput"
          :class="{
            'is-invalid':
              $v.email.$dirty && (!$v.email.required || !$v.email.email),
          }"
        />
        <br />
        <h6>Пароль</h6>
        <input
          v-model="password"
          type="password"
          class="form-control textInput"
          :class="{
            'is-invalid':
              ($v.password.$dirty && !$v.password.minLength) ||
              ($v.password.$dirty && !$v.password.required),
          }"
        />
        <br />
        <h6>Повторите пароль</h6>
        <input
          v-model="UserData.pass2"
          type="password"
          class="form-control textInput"
          required
        />
      </div>
      <div class="card-footer">
        <router-link to="/home">
          <button class="btn btn-dark btnMain" @click="RegisterFunc">
            начать
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped></style>
