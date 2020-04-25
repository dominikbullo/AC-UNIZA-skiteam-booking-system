<template>
  <div id="page-family-edit">
    <vs-alert :active.sync="family_not_found" color="danger" title="User Not Found">
      <span>Family record with id: {{ $route.params.familyID }} not found. </span>
      <span>
        <span>Check </span><router-link :to="{name:'page-user-list'}"
                                        class="text-inherit underline">All Users</router-link>
      </span>
    </vs-alert>

    <p>{{family_data}}</p>
    <vx-card v-if="family_data">
      <div class="tabs-container px-6 pt-6" slot="no-body">

        <vs-tabs class="tab-action-btn-fill-conatiner" v-model="activeTab">
          <vs-tab icon="icon-info" icon-pack="feather" label="Information">
            <div class="tab-text">
              <family-edit-tab-information class="mt-4" :data="family_data"/>
            </div>
          </vs-tab>
          <!--          <vs-tab icon="icon-users" icon-pack="feather" label="Members">-->
          <!--            <div class="tab-text">-->
          <!--              <family-edit-tab-social class="mt-4" :data="family_data"/>-->
          <!--            </div>-->
          <!--          </vs-tab>-->
          <!--          <vs-tab icon="icon-user" icon-pack="feather" label="Profile">-->
          <!--            <div class="tab-text">-->
          <!--              <family-edit-tab-account class="mt-4" :data="family_data"/>-->
          <!--            </div>-->
          <!--          </vs-tab>-->
        </vs-tabs>

      </div>

    </vx-card>
  </div>
</template>

<script>
import FamilyEditTabInformation from './FamilyEditTabInformation.vue'

export default {
  components: {
    FamilyEditTabInformation
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
      this.fetchFamilyData(this.$route.params.familyId)
    }
  },
  methods: {
    fetchFamilyData (familyId) {
      this.$store.dispatch('family/fetchFamily', familyId)
        .then(res => {
          this.family_data = res.data
        })
        .catch(err => {
          if (err.response.status === 404) {
            this.family_not_found = true
            return
          }
          console.error(err)
        })
    }
  },
  created () {
    this.fetchFamilyData(this.$route.params.familyId)
  }
}

</script>
