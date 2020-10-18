<template>
  <table>
    <thead>
      <tr>
        <th>ФИО</th>
        <th>Логин</th>
        <th>Всего ошибок</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(line, index) of countArr"
        :key="index"
        :line="line"
      >
        <td
          v-for="(item, itemIndex) of line"
          :key="itemIndex"
          :item="item"
        >
          {{ item }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  name: 'StatisticKv',
  data: function () {
    return {
      countArr: []
    }
  },
  computed: mapGetters(['getStartDate', 'getEndDate']),
  methods: {
    fetchStat () {
      fetch(
        `stat_kv?start_date=${this.getStartDate}&end_date=${this.getEndDate}`
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
