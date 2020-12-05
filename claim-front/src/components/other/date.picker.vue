<template>
  <div class="wrapper">
    <span>Обязательно выберите месяц: </span>
    <select
      id="month"
      @click="setDate($event.target.value)"
    >
      <option
        v-for="(item, index) in month"
        :item="item"
        :value="index"
        :key="index"
      >
        {{ item }}
      </option>
    </select>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'DatePicker',
  data () {
    return {
      month: {
        0: 'Январь',
        1: 'Февраль',
        2: 'Март',
        3: 'Апрель',
        4: 'Май',
        5: 'Июнь',
        6: 'Июль',
        7: 'Август',
        8: 'Сентябрь',
        9: 'Октябрь',
        10: 'Ноябрь',
        11: 'Декабрь',
      }
    }
  },
  computed: mapGetters(['getStartDate', 'getEndDate']),
  methods: {
    ...mapActions(['setStartDate', 'setEndDate']),
    setDate (month) {
      month = parseInt(month) + 1
      let startDate = `${(new Date()).getFullYear()}-${month < 10 ? '0' + month : month}-01`
      this.setStartDate(startDate)
      let endDate = `${(new Date()).getFullYear()}-${month < 10 ? '0' + month : month}-`
      if (month === 12)
        month = 0
      endDate += `${new Date((new Date()).getFullYear(), month, 0).getDate()}`
      this.setEndDate(endDate)
    },
  },
}
</script>

<style scoped lang="sass">
.wrapper
  display: flex
  flex: 0 0
  flex-flow: row nowrap
  margin: 5px 0 20px 0
  align-items: center

input
  margin: 0 10px 0 5px
</style>
