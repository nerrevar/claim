<template>
  <div
    class="menu_button"
    v-if="checkPrivacy(item.privacy)"
  >
    <div
      class="project_text"
      v-if="item.type === 'single'"
      @click="setCurrentPageLocal(item)"
    >
      {{ item.name }}
    </div>
    <div
      class="project_text"
      v-if="item.type === 'multiple'"
      @click="menuToggle"
    >
      {{ item.name }}
    </div>
    <div
      class="menu"
      v-if="item.type === 'multiple'"
      :class="{closed: !opened}"
    >
      <div
        class="menu_item"
        v-for="(subitem, subindex) in filter(item.submenu)"
        :key="subindex"
        :item="subitem"
        @click="setCurrentPageLocal(subitem)"
      >
        <span class="item_text">{{ subitem.name }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'Menu',
  props: ['item'],
  data: function () {
    return {
      opened: false,
    }
  },
  computed: mapGetters(['getUser']),
  methods: {
    ...mapActions(['setCurrentPage']),
    menuToggle () {
      this.opened = !this.opened
    },
    setCurrentPageLocal (page) {
      this.opened = false
      this.setCurrentPage(page)
    },
    checkPrivacy (privacyLevel) {
      let userLevel = 0
      switch (this.getUser.role) {
        case 'pret_work': {
          userLevel = 3
          break
        }
        case 'pret_view': {
          userLevel = 2
          break
        }
        case 'pret_captain': {
          userLevel = 1
          break
        }
        default:
          break
      }
      return userLevel >= privacyLevel
    },
    filter (menuArr) {
      return menuArr.filter(m => this.checkPrivacy(m.privacy))
    }
  }
}
</script>

<style scoped lang="sass">
.menu_button
  padding: 10px
  border: 1px solid blue
  margin: 2px

.menu
  position: absolute
  background: pink
  z-index: 15

.menu_item
  font-size: 15px
  padding: 5px
  margin: 2px
  border: 1px solid red
</style>
