<template>
  <form class="wrapper">
    <label for="username">Имя пользователя</label>
    <input type="text" name="username" id="username" />
    <label for="password">Пароль</label>
    <input type="password" name="password" id="password" />
    <div
      class="button"
      @click="login"
    >
      Вход
    </div>
    <div
      class="error red"
      v-if="error !== ''"
    >
      {{ error }}
    </div>
  </form>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'Login',
  data () {
    return {
      error: ''
    }
  },
  methods: {
    ...mapActions(['setUser', 'setCurrentProject', 'setCurrentPage']),
    login () {
      fetch(
        'login',
        {
          method: 'POST',
          mode: 'same-origin',
          body: new FormData(document.querySelector('form'))
        }
      ).then(
        response => response.json()
      ).then(
        response => {
          switch(response.status) {
            case 'True': {
              this.setUser({
                name: response.name,
                login: response.login,
                project: response.project,
                role: response.role,
                group_name: response.group_name,
              })
              // setCurrentProject({ code: response.project_code })
              this.setCurrentPage({ code: 'stat' })
              break
            }
            case 'Error': {
              this.error = 'Ошибка: ' + response.error
              break
            }
            default:
              this.error = 'Неизвестная ошибка'
          }
        }
      )
    }
  },
}
</script>

<style lang="sass" scoped>
.wrapper
  position: absolute
  z-index: 11000
  display: flex
  align-self: center
  width: 300px
  margin: 15% auto auto auto
  padding: 20px

input, label, div
  margin: 5px

.button
  background: #13aa13
  padding: 10px
  text-align: center
</style>
