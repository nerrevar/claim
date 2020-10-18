<template>
  <div class="main">
    <div
      class="result_wrapper"
      v-if="result !== {}"
    >
      <div
        class="red unneeded"
        v-if="result.unneeded !== undefined"
      >
        <div>Неиспользуемые логины:</div>
        <div
          class="black"
          v-for="(item, index) in result.unneeded"
          :key="index"
          :item="item"
        >
          {{ item }}
        </div>
      </div>
      <div
        class="green needed"
        v-if="result.needed !== undefined"
      >
        <div>Отсутствующие логины:</div>
        <div
          class="black"
          v-for="(item, index) in result.needed"
          :key="index"
          :item="item"
        >
          {{ item }}
        </div>
      </div>
    </div>
    <button
      @click="check"
    >
      Проверить
    </button>
    <div class="input_wrapper">
      <label for="list">Список логинов:</label>
      <textarea name="list" id="list"></textarea>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserCheck',
  data () {
    return {
      result: {},
      login: []
    }
  },
  created () {
    fetch(
      'get_login'
    ).then(
      response => response.json()
    ).then(
      response => this.login = response
    )
  },
  methods: {
    check () {
      let input = document.getElementById('list').value.split('\n')
      for (let login of input)
        if (!this.login.includes(login)) {
          if (this.result.needed === undefined)
            this.result.needed = []
          this.result.needed.push(login)
        }
      for (let login of this.login)
        if (!input.includes(login)) {
          if (this.result.unneeded === undefined)
            this.result.unneeded = []
          this.result.unneeded.push(login)
        }
      this.$forceUpdate()
    }
  }
}
</script>

<style lang="sass" scoped>
.main
  padding: 10px

.result_wrapper
  display: flex
  flex: 1 0
  flex-flow: row nowrap

.needed, .unneeded, .input_wrapper
  display: flex
  flex: 1 0
  flex-flow: column nowrap

textarea
  min-height: 400px

button
  margin: 10px 0

label
  margin-bottom: 10px
</style>
