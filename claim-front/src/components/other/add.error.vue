<template>
  <form class="wrapper">
    <label for="kv_select">ФИО кв: </label>
    <input type="text" id="kv_select" list="kv" name="kv_name" />
    <datalist id="kv">
      <option
        v-for="(kv, index) of kvList"
        :key="index"
        :value="kv.name"
      />
    </datalist>
    <label for="q_select">Вопрос: </label>
    <input type="text" id="q_select" list="q" name="question" />
    <datalist id="q">
        <option
          v-for="(q, index) of question"
          :key="index"
          :value="`${q.number}. ${q.text}`"
        />
    </datalist>
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
  name: 'AddError',
  data() {
    return {
      question: [],
      kvList: [],
      response: ''
    }
  },
  methods: {
    addError(e) {
      e.preventDefault()
      fetch(
        'write_error',
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
          document.getElementById('q_select').value = ''
          setTimeout((_=this) => {
              _.response = ''
            },
            10000
          )
        }
      )
    }
  },
  created() {
    fetch(
      'get_error_fill_data'
    ).then(
      response => response.json()
    ).then(
      response => {
        this.question = response.question
        this.kvList = response.kvList
      }
    )
  }
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
