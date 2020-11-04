<template>
  <div id="page-user-edit">

    <vs-alert color="danger" title="User Not Found" :active.sync="event_not_found">
      <span>User record with id: {{ $route.params.userId }} not found. </span>
      <span>
        <span>Check </span><router-link :to="{name:'page-user-list'}"
                                        class="text-inherit underline">All Users</router-link>
      </span>
    </vs-alert>

    <vx-card v-if="event_data">
      <div slot="no-body" class="tabs-container px-6 pt-6">

        <vs-tabs v-model="activeTab" class="tab-action-btn-fill-conatiner">
          <vs-tab v-if="this.$acl.check('isCoach')" label="General" href="#general" icon-pack="feather"
                  icon="icon-info">
            <div class="tab-text">
              <event-edit-tab-general class="mt-4" :data="event_data"/>
            </div>
          </vs-tab>
          <vs-tab v-if="this.$acl.check('isCoach')" label="Participants" href="#participants" icon="group">
            <div class="tab-text">
              <event-edit-tab-participants @eventname="updateparent" class="mt-4" :data="event_data"/>
            </div>
          </vs-tab>
          <vs-tab v-if="this.$acl.check('isParent')" label="Accommodation" href="#accommodation"
                  icon-pack="material-icons" icon="hotel">
            <div class="tab-text">
              <event-edit-tab-accommodation class="mt-4" :data="event_data.accommodation"/>
            </div>
          </vs-tab>
        </vs-tabs>

      </div>
    </vx-card>
  </div>
</template>

<script>

import EventEditTabGeneral from './EventEditTabGeneral'
import EventEditTabParticipants from './EvetntEditTabParticipiants'

export default {
  components: {
    EventEditTabGeneral,
    EventEditTabParticipants,
    EventEditTabAccommodation
  },
  data () {
    return {
      event_data: null,
      event_not_found: false,
      activeTab: 0,
      tabs: ['#general', '#participants', '#accommodation']
    }
  },
  watch: {
    activeTab () {
      this.fetch_event(this.$route.params.eventId)
    }
  },
  methods: {
    updateparent (variable) {
      this.event_data = variable
    },
    fetch_event (eventId) {
      this.$store.dispatch('calendar/fetchEvent', eventId)
        .then(res => {
          this.event_data = res.data
        })
        .catch(err => {
          if (err.response.status === 404) {
            this.event_not_found = true
            return
          }
          console.error(err)
        })
    }
  },
  created () {
    this.fetch_event(this.$route.params.eventId)
    this.$store.dispatch('calendar/fetchEventTypes')
  },
  mounted () {
    // RES:https://stackoverflow.com/questions/52090371/how-to-navigate-to-specific-tab-in-bootstrap-vue-tabs-in-vue-routes
    this.activeTab = this.tabs.findIndex(tab => tab === this.$route.hash)
  }
}

</script>
