<template>
  <form class="wrapper">
    <label>Список ошибок: </label>
    <textarea type="text" id="error_list"></textarea>
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
          Ошибки успешно добавлены
        </span>
        <span
          class="red"
          v-show="response !== 'True'"
        >
          Ошибки не добавлены
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
      let data = {
        error_list: document.getElementById('error_list').value.split('\n').map(
          el => {
            let arr = el.split(',')
            return {
              login: arr[0].trim(),
              question_text: arr[1].trim(),
              form_id: arr[2].trim(),
            }
          }
        ),
        prev: document.getElementById('prev').checked,
      }
      console.log(data)
      fetch(
        'write_error_multiple',
        {
          method: 'POST',
          mode: 'same-origin',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data),
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

textarea
  width: 100%
  height: 300px

#prev
  width: 16px
  margin: 5px

button
  width: 200px
  height: 30px
</style>
