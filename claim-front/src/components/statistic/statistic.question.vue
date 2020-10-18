<template>
  <table>
    <thead>
      <tr>
        <th>Вопрос</th>
        <th>Всего ошибок</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(itemNum, index) in countArr"
        :key="index"
        :item="itemNum"
        :index="index"
      >
        <td>{{ index }}</td>
        <td>{{ itemNum }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'StatisticQuestion',
  data() {
    return {
      countArr: {}
    }
  },
  computed: mapGetters(['getUser', 'getStartDate', 'getEndDate']),
  methods: {
    fetchStat () {
      fetch(
        `stat_question?user=${this.getUser.login}&start_date=${this.getStartDate}&end_date=${this.getEndDate}`
      ).then(
        response => response.json()
      ).then(
        response => this.countArr = response
      )
    }
  },
  mounted () { this.fetchStat() },
  watch: {
    getStartDate: function () { this.fetchStat() },
    getEndDate: function () { this.fetchStat() },
  }
}
</script>
