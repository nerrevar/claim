<template>
  <form class="wrapper">
    <label for="kv_select">Список ошибок: </label>
    <input type="text" id="error_list" name="error_list" />
    <input type="checkbox" id="prev" name="prev" />
    <label for="prev">Отнести к прошлому месяцу</label>
    <div>
      <button @click="addError($event)">Добавить</button>
      <div
        class="response_status"
        v-if="response !== ''"
      >
        <span
          class="green"
          v-show="response === 'True'"
        >
          Ошибка успешно добавлена
        </span>
        <span
          class="red"
          v-show="response !== 'True'"
        >
          Ошибка не добавлена
        </span>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  name: 'AddErrorMultiple',
  data() {
    return {
      response: ''
    }
  },
  methods: {
    addError(e) {
      e.preventDefault()
      fetch(
        'write_error_multiple',
        {
          method: 'POST',
          mode: 'same-origin',
          body: new FormData(document.querySelector("form")), // TODO: Convert to JSON
          credentials: 'include',
        }
      ).then(
        response => response.text()
      ).then(
        response => {
          this.response = response
          setTimeout(() => {
              this.response = ''
            },
            10000
          )
        }
      )
    }
  },
}
</script>

<style lang="sass" scoped>
.wrapper
  display: flex
  flex: 1 0
  flex-flow: row wrap

label
  width: 90%

input
  width: 100%

#prev
  width: 16px
  margin: 5px

button
  width: 200px
  height: 30px
</style>
