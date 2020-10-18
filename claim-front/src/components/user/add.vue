<template>
  <form>
    <label for="name">ФИО</label>
    <input type="text" id="name" name="name" />
    <label for="username">Имя пользователя</label>
    <input type="text" id="username" name="username" />
    <label for="group">Группа</label>
    <select name="group" id="group">
      <option
        v-for="(group, index) in groups"
        :key="index"
        :value="group"
        :group="group"
      >
        {{ group }}
      </option>
    </select>
    <label for="role">Роль</label>
    <select name="role" id="role" value="pret_kv">
      <option
        v-for="(role, index) in roles"
        :key="index"
        :value="role"
        :role="role"
      >
        {{ role }}
      </option>
    </select>
    <button
      @click="addUser($event)"
    >
      Добавить
    </button>
    <div
      class="response_status"
      v-if="response !== ''"
    >
      <span
        class="green"
        v-show="response === 'True'"
      >
        Пользователь успешно добавлен
      </span>
      <span
        class="red"
        v-show="response === 'False'"
      >
        Пользователь не добавлен
      </span>
      <span
        class="red"
        v-show="response === 'User exist'"
      >
        Пользователь существует
      </span>
    </div>
  </form>
</template>

<script>
export default {
  name: 'UserAdd',
  data () {
    return {
      groups: [],
      roles: ['pret_kv', 'pret_captain', 'pret_view', 'pret_work'],
      response: ''
    }
  },
  methods: {
    addUser (e) {
      e.preventDefault()
      fetch(
        'user_add',
        {
          method: 'POST',
          mode: 'same-origin',
          body: new FormData(document.querySelector("form")),
          credentials: 'include',
        }
      ).then(
        response => response.text()
      ).then(
        response => {
          this.response = response
          setTimeout((_=this) => {
              _.response = ''
            },
            10000
          )
        }
      )
    },
  },
  created () {
    fetch(
      'get_groups'
    ).then(
      response => response.json()
    ).then(
      response => this.groups = response
    )
  }
}
</script>

<style lang="sass" scoped>
form
  display: flex
  flex: 1 0
  flex-flow: column nowrap
  padding: 10px

input, select, button
  width: 50%
  margin: 10px 0
</style>
