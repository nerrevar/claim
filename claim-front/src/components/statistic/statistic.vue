<template>
  <div class="wrapper">
    <div class="table">
      <div class="table_row bold head">
        <div class="table_cell">ФИО</div>
        <div class="table_cell">Логин</div>
        <div
          class="table_cell"
          v-for="(q, index) in question"
          :key="index"
          :q="q"
        >
          <div>{{ q.number }}</div>
          <div>{{ q.text }}</div>
        </div>
        <div class="table_cell">Итого</div>
      </div>
      <div
        class="table_block"
        v-for="(group, index) in filterGroups(group)"
        :key="index"
        :group="group"
      >
        <div class="table_row">
          <div class="table_cell bold">{{ group.name }}</div>
          <div class="table_cell bold">{{ group.summary }}</div>
          <div
            class="table_cell noborder"
            v-for="(q, q_index) in question"
            :key="q_index"
          ></div>
          <div class="table_cell noborder"></div>
        </div>
        <div
          class="table_row"
          v-for="(kv, kv_index) in filterKv(group.kv)"
          :key="kv_index"
          :kv="kv"
        >
          <div class="table_cell sticky">{{ kv.name }}</div>
          <div class="table_cell sticky">{{ kv.login }}</div>
          <div
            class="table_cell"
            v-for="(q, q_index) in question"
            :key="q_index"
            :q="q"
          >
            {{ kv.errCountArr[q.number] || 0 }}
          </div>
          <div class="table_cell">{{ kv.summary }}</div>
        </div>
        <div class="table_row bold">
          <div class="table_cell"></div>
          <div class="table_cell">Итого</div>
          <div
            class="table_cell"
            v-for="(q, index) in question"
            :key="index"
            :q="q"
          >
            <span v-text="groupCountByQuestion(group, q.number)"></span>
          </div>
          <div class="table_cell">
            <span v-text="groupCount(group)"></span>
          </div>
        </div>
      </div>
      <div
        class="table_row bold"
        v-if="!['pret_captain', 'pret_kv'].includes(getUser.role)"
      >
        <div class="table_cell"></div>
        <div class="table_cell">Итого</div>
        <div
          class="table_cell"
          v-for="(q, index) in question"
          :key="index"
          :q="q"
        >
          {{ q.summary }}
        </div>
        <div class="table_cell noborder"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Statistic',
  data() {
    return {
      question: [],
      group: [],
      captain: [],
    }
  },
  computed: mapGetters(['getUser', 'getStartDate', 'getEndDate']),
  methods: {
    fetchClaims () {
      fetch(
        `get_stat?user=${this.getUser.login}&start_date=${this.getStartDate}&end_date=${this.getEndDate}`
      ).then(
        response => response.json()
      ).then(
        response => {
          this.group = response.group
          this.question = response.question
          this.captain = response.captain
          for (let groupNum in this.group)
            for (let kvNum in this.group[groupNum].kv) {
              this.group[groupNum].kv[kvNum]['errCountArr'] = {}
              for (let q of this.question) {
                let error = response.claim.filter(
                  claim => claim.kvName == this.group[groupNum].kv[kvNum].name && claim.questionNumber == q.number
                )
                if (error)
                  this.group[groupNum].kv[kvNum]['errCountArr'][q.number] = error.length
              }
            }
        }
      )
    },
    filterGroups (groupArr) {
      switch (this.getUser.role) {
        case 'pret_view':
        case 'pret_work': return groupArr
        case 'pret_captain': {
          return groupArr.filter(
            g => g.name === this.captain.filter(
              c => c.captainName === this.getUser.name
            )[0].groupName
          )
        }
        default: {
          return groupArr.filter(
            g => g.kv.filter(kv => kv.login === this.getUser.login).length
          )
        }
      }
    },
    filterKv (kvArr) {
      switch (this.getUser.role) {
        case 'pret_captain':
        case 'pret_view':
        case 'pret_work': return kvArr
        default: {
          return kvArr.filter(kv => kv.login === this.getUser.login)
        }
      }
    },
    groupCountByQuestion (group, number) {
      let count = 0
      for (let kv of group.kv)
        count += kv.errCountArr[number]
      return count
    },
    groupCount (group) {
      let count = 0
      for (let kv of group.kv)
        for (let errCount of Object.values(kv.errCountArr))
          count += errCount
      return count
    }
  },
  mounted () { this.fetchClaims() },
  watch: {
    getStartDate: function () { this.fetchClaims() },
    getEndDate: function () { this.fetchClaims() },
  }
}
</script>


<style scoped lang="sass">
.wrapper
  display: flex
  flex-flow: row nowrap

.table
  display: flex
  flex: 1 0 auto
  flex-flow: column nowrap

.table_row
  display: flex
  flex: 1 0
  flex-flow: row nowrap
  align-self: stretch

.table_cell
  display: flex
  flex: 1 0
  flex-flow: column nowrap
  border: 1px solid grey
  padding: 3px

.noborder
  border: 0!important
  padding: 4px!important

.head
  position: sticky
  top: 0
  background: white
  z-index: 11

.sticky
  position: sticky
  left: 0
  background: white

.bold
  font-weight: 800
</style>
