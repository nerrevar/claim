<template>
  <div class="wrapper">
    <label for="start_date">Начальная дата</label>
    <input
      type="date"
      id="start_date"
      @change="setStartDate($event.target.value)"
      :value="getStartDate"
    />
    <label for="end_date">Конечная дата</label>
    <input
      type="date"
      id="end_date"
      @change="setEndDate($event.target.value)"
      :value="getEndDate"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'DatePicker',
  computed: mapGetters(['getStartDate', 'getEndDate']),
  methods: mapActions(['setStartDate', 'setEndDate'])
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
