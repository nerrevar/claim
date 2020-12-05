<template>
  <div class="wrapper">
    <Login
      v-if="this.getUser.login === undefined"
    ></Login>
    <Header
      :class="{ hidden: this.getUser.login === undefined }"
      :project="project"
    ></Header>
    <DatePicker
      :class="{ hidden: this.getUser.login === undefined }"
      v-show="['stat', 'stat_kv', 'stat_question'].includes(getCurrentPage.code)"
    ></DatePicker>
    <component
      class="content"
      :class="{ hidden: this.getUser.login === undefined }"
      :is="getCurrentPageLocal"
    ></component>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import Login from './login'
import Header from './header/header'
import DatePicker from './other/date.picker'
import Statistic from './statistic/statistic'
import StatisticKv from './statistic/statistic.kv'
import StatisticQuestion from './statistic/statistic.question'
import ClaimNumber from './other/claim.number'
import AddError from './other/add.error'
import AddErrorMultiple from './other/add.error.multiple'
import UserAdd from './user/add'
import UserCheck from './user/check'
import UserSettings from './auth/settings'

export default {
  name: 'App',
  data () {
    return {
      project: [
        {
          code: 'mk',
          name: 'Магнит Косметик',
          menu: [
            {
              name: 'Статистика',
              type: 'multiple',
              privacy: 0,
              submenu: [
                {
                  code: 'stat',
                  name: 'Общая',
                  privacy: 0
                },
                {
                  code: 'stat_kv',
                  name: 'Статистика по КВ',
                  privacy: 2
                },
                {
                  code: 'stat_question',
                  name: 'Статистика по вопросам',
                  privacy: 2
                }
              ]
            },
            {
              name: 'Номера анкет',
              type: 'single',
              code: 'claim_number',
              privacy: 0,
            },
            {
              name: 'Добавить ошибку',
              type: 'single',
              code: 'add_error',
              privacy: 2
            },
            {
              name: 'Добавить ошибки списком',
              type: 'single',
              code: 'add_error_multiple',
              privacy: 2
            },
            {
              name: 'Пользователь',
              type: 'multiple',
              privacy: 3,
              submenu: [
                {
                  name: 'Добавить пользователя',
                  code: 'user_add',
                  privacy: 3
                },
                {
                  name: 'Сверка',
                  code: 'user_check',
                  privacy: 3
                }
              ]
            }
          ]
        },
      ],
    }
  },
  components: {
    Login,
    Header,
    DatePicker,
    Statistic,
    StatisticKv,
    StatisticQuestion,
    ClaimNumber,
    AddError,
    AddErrorMultiple,
    UserAdd,
    UserCheck,
    UserSettings,
  },
  computed: {
    ...mapGetters(['getCurrentPage', 'getUser']),
    getCurrentPageLocal: function () {
      switch (this.getCurrentPage.code){
        case 'start':
        case 'stat': return 'Statistic'
        case 'stat_kv': return 'StatisticKv'
        case 'stat_question': return 'StatisticQuestion'
        case 'claim_number': return 'ClaimNumber'
        case 'add_error': return 'AddError'
        case 'add_error_multiple': return 'AddErrorMultiple'
        case 'user_add': return 'UserAdd'
        case 'user_check': return 'UserCheck'
        case 'user_settings': return 'UserSettings'
        default: return 'Statistic'
      }
    }
  },
  methods: mapActions(['setCurrentProject', 'setUser', 'setCurrentPage']),
  created () {
  },
  mounted () {
    fetch(
      'login',
      {
        method: 'POST',
        mode: 'same-origin',
        credentials: 'include'
      }
    ).then(
      response => response.json()
    ).then(
      response => {
        if (response.status === 'True') {
          this.setUser({
            name: response.name,
            login: response.login,
            project: response.project,
            role: response.role,
            group_name: response.group_name,
          })
          this.setCurrentPage({ code: 'stat' })
        }
      }
    )
    this.setCurrentProject(this.project[0])
  }
}
</script>

<style lang="sass">
*
  margin: 0
  padding: 0
  box-sizing: border-box

.hidden
  visibility: hidden

.wrapper
  display: flex
  flex-flow: column nowrap

.content
  padding: 10px

#app
  font-family: Avenir, Helvetica, Arial, sans-serif
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  text-align: center
  color: #2c3e50
  margin-top: 60px

.closed
  display: none

.black
  color: black

.green
  color: green

.red
  color: red
</style>
