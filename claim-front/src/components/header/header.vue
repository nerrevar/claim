<template>
  <div class="header">
    <Project
      class="project"
      :class="{
        red: getCurrentProject.code == 'mm',
        pink: getCurrentProject.code == 'mk',
      }"
      :project="project"
    ></Project>
    <div class="nav_wrapper">
      <Menu
        class="nav_menu"
        v-for="(item, index) in getCurrentProject.menu"
        :key="index"
        :item="item"
      ></Menu>
      <div
        class="authorization nav_menu menu_button"
        @click="setCurrentPage({ name: 'Настройки пользователя', code: 'user_settings' })"
      >
        {{ getUser.name || getUser.login }}
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import Project from './project'
import Menu from './menu'

export default {
  name: 'Header',
  props: ['project', 'menu'],
  components: {Project, Menu},
  computed: mapGetters(['getCurrentProject', 'getUser']),
  methods: mapActions(['setCurrentPage'])
}
</script>

<style scoped lang="sass">
.header
  width: 100vw

.project
  width: 100vw

.red
  background: red

.pink
  background: pink

.nav_wrapper
  display: flex
  flex: 1 0
  flex-flow: row wrap

.nav_menu
  background: lightblue
  font-size: 20px

.menu_button
  padding: 10px
  border: 1px solid blue
  margin: 2px
  align-self: center

.authorization
  margin: 2px 2px 2px auto
</style>
