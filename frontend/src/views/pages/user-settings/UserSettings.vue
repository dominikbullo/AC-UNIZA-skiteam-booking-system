<template>
  <vs-tabs :position="isSmallerScreen ? 'top' : 'left'" class="tabs-shadow-none" id="profile-tabs"
           :key="isSmallerScreen" v-model="activeTab">

    <!-- GENERAL -->
    <vs-tab icon-pack="feather" icon="icon-user" :label="!isSmallerScreen ? $t('General') : ''">
      <div class="tab-general md:ml-4 md:mt-0 mt-4 ml-0">
        <user-settings-general/>
      </div>
    </vs-tab>
    <vs-tab icon-pack="feather" icon="icon-users" :label="!isSmallerScreen ? $t('Family') : ''">
      <div class="tab-info md:ml-4 md:mt-0 mt-4 ml-0">
        <user-settings-change-family/>
      </div>
    </vs-tab>
    <vs-tab icon-pack="feather" icon="icon-lock" :label="!isSmallerScreen ? $t('Change Password') : ''">
      <div class="tab-change-pwd md:ml-4 md:mt-0 mt-4 ml-0">
        <user-settings-change-password/>
      </div>
    </vs-tab>
    <vs-tab icon-pack="feather" icon="icon-info" :label="!isSmallerScreen ? $t('Info') : ''">
      <div class="tab-info md:ml-4 md:mt-0 mt-4 ml-0">
        <user-settings-info/>
      </div>
    </vs-tab>

    <!--    <vs-tab icon-pack="feather" icon="icon-github" :label="!isSmallerScreen ? 'Social Links' : ''">-->
    <!--      <div class="tab-social-links md:ml-4 md:mt-0 mt-4 ml-0">-->
    <!--        <user-settings-social-links/>-->
    <!--      </div>-->
    <!--    </vs-tab>-->
    <!--    <vs-tab icon-pack="feather" icon="icon-link-2" :label="!isSmallerScreen ? 'Connections' : ''">-->
    <!--      <div class="tab-text md:ml-4 md:mt-0 mt-4 ml-0">-->
    <!--        <user-settings-connections />-->
    <!--      </div>-->
    <!--    </vs-tab>-->
    <!--    <vs-tab icon-pack="feather" icon="icon-bell" :label="!isSmallerScreen ? 'Notifications' : ''">-->
    <!--      <div class="tab-text md:ml-4 md:mt-0 mt-4 ml-0">-->
    <!--        <user-settings-notifications/>-->
    <!--      </div>-->
    <!--    </vs-tab>-->
  </vs-tabs>
</template>

<script>
import UserSettingsGeneral from './UserSettingsGeneral.vue'
import UserSettingsChangePassword from './UserSettingsChangePassword.vue'
import UserSettingsChangeFamily from './UserSettingsChangeFamily.vue'
import UserSettingsInfo from './UserSettingsInfo.vue'
import UserSettingsSocialLinks from './UserSettingsSocialLinks.vue'
// import UserSettingsConnections from './UserSettingsConnections.vue'
import UserSettingsNotifications from './UserSettingsNotifications.vue'
import moduleUserManagement from '@/store/user-management/moduleUserManagement'

export default {
  components: {
    UserSettingsGeneral,
    UserSettingsChangePassword,
    UserSettingsInfo,
    UserSettingsSocialLinks,
    // UserSettingsConnections,
    UserSettingsNotifications,
    UserSettingsChangeFamily
  },
  data () {
    return {
      activeTab: 0,
      tabs: ['#general', '#family', '#password', '#info']
    }
  },
  computed: {
    isSmallerScreen () {
      return this.$store.state.windowWidth < 768
    }
  },
  created () {
    if (!moduleUserManagement.isRegistered) {
      this.$store.registerModule('userManagement', moduleUserManagement)
      moduleUserManagement.isRegistered = true
    }
    this.activeTab = this.tabs.findIndex(tab => tab === this.$route.hash)
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
