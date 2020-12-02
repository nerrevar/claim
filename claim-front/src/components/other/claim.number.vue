<template>
  <div class="wrapper">
    <div
      v-if="zero === true"
    >
      Нет записей
    </div>
    <table
      cellspacing=0
      v-if="zero !== true"
    >
      <thead>
        <tr>
          <th>Номер Анкеты</th>
          <th>Вопрос</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(item, index) of number"
          :item="item"
          :key="index"
        >
          <td>{{ item.number }}</td>
          <td>{{ item.question }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  name: 'ClaimNumber',
  data () {
    return {
      zero: false,
      number: {},
    }
  },
  computed: mapGetters(['getCurrentPage', 'getUser', 'getStartDate', 'getEndDate']),
  methods: {
    fetchNumbers () {
      console.log('fetching')
      let login = this.getCurrentPage.login ? this.getCurrentPage.login : this.getUser.login
      fetch(
        `get_numbers?login=${login}&start_date=${this.getStartDate}&end_date=${this.getEndDate}`,
      ).then(
        response => response.json()
      ).then(
        response => {
          if (response.status === 'zero')
            this.zero = true
          else
            this.number = response
        }
      )
    }
  },
  mounted () {
    this.fetchNumbers()
  },
  watch: {
    getStartDate: function () { this.fetchNumbers() },
    getEndDate: function () { this.fetchNumbers() },
  }
}
</script>

<style lang="sass" scoped>
td, th
  border: 1px solid black
  padding: 5px
</style>
