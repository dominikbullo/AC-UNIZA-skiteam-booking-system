<template>
  <vs-tabs :position="isSmallerScreen ? 'top' : 'left'" class="tabs-shadow-none" id="profile-tabs"
           :key="isSmallerScreen">

    <!-- GENERAL -->
    <vs-tab icon-pack="feather" icon="icon-user" :label="!isSmallerScreen ? 'General' : ''">
      <div class="tab-general md:ml-4 md:mt-0 mt-4 ml-0">
        <family-settings-general></family-settings-general>
      </div>
    </vs-tab>

  </vs-tabs>
</template>

<script>
import FamilySettingsGeneral from '../FamilyGeneral.vue'

export default {
  components: {
    FamilySettingsGeneral
  },
  data () {
    return {}
  },
  computed: {
    isSmallerScreen () {
      return this.$store.state.windowWidth < 768
    }
  }
}
</script>

<style lang="scss">
  #profile-tabs {
    .vs-tabs--content {
      padding: 0;
    }
  }
</style>
