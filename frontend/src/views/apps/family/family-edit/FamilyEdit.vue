<!-- =========================================================================================
  File Name: UserEdit.vue
  Description: User Edit Page
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div id="page-family-edit">

    <vs-alert :active.sync="family_not_found" color="danger" title="User Not Found">
      <span>Family record with id: {{ $route.params.familyID }} not found. </span>
      <span>
        <span>Check </span><router-link :to="{name:'page-user-list'}"
                                        class="text-inherit underline">All Users</router-link>
      </span>
    </vs-alert>

    <!--    <vx-card v-if="family_data">-->
    <vx-card>

      <div class="tabs-container px-6 pt-6" slot="no-body">

        <vs-tabs class="tab-action-btn-fill-conatiner" v-model="activeTab">
          <vs-tab icon="icon-info" icon-pack="feather" label="Information">
            <div class="tab-text">
              <!--              <family-edit-tab-information class="mt-4" :data="family_data"/>-->
            </div>
          </vs-tab>
          <vs-tab icon="icon-users" icon-pack="feather" label="Members">
            <div class="tab-text">
              <!--              <family-edit-tab-social class="mt-4" :data="family_data"/>-->
            </div>
          </vs-tab>
          <vs-tab icon="icon-user" icon-pack="feather" label="Profile">
            <div class="tab-text">
              <!--              <family-edit-tab-account class="mt-4" :data="family_data"/>-->
            </div>
          </vs-tab>
        </vs-tabs>

      </div>

    </vx-card>
  </div>
</template>

<script>
import FamilyEditTabAccount from './FamilyEditTabAccount.vue'
import FamilyEditTabInformation from './FamilyEditTabInformation.vue'
import FamilyEditTabSocial from './FamilyEditTabSocial.vue'

// // Store Module
// import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'

export default {
  components: {
    FamilyEditTabAccount,
    FamilyEditTabInformation,
    FamilyEditTabSocial
  },
  data () {
    return {
      family_data: null,
      family_not_found: false,

      /*
        This property is created for fetching latest data from API when tab is changed

        Please check it's watcher
      */
      activeTab: 0
    }
  },
  watch: {
    activeTab () {
      this.fetch_family_data(this.$route.params.familyID)
    }
  },
  methods: {
    fetch_family_data (familyID) {
      console.log('Need to fetch family', familyID)
      // this.$store.dispatch('userManagement/fetchDefaultUser', userId)
      //   .then(res => {
      //     this.family_data = res.data
      //   })
      //   .catch(err => {
      //     if (err.response.status === 404) {
      //       this.user_not_found = true
      //       return
      //     }
      //     console.error(err)
      //   })
    }
  },
  created () {
    console.log('created')
    // // Register Module UserManagement Module
    // if (!moduleUserManagement.isRegistered) {
    //   this.$store.registerModule('userManagement', moduleUserManagement)
    //   moduleUserManagement.isRegistered = true
    // }
    // this.fetch_family_data(this.$route.params.userId)
  }
}

</script>
