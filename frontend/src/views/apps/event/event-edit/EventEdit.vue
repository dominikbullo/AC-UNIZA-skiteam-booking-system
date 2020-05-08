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
          <vs-tab label="General" icon-pack="feather" icon="icon-user">
            <div class="tab-text">
              <event-edit-tab-general class="mt-4" :data="event_data"/>
            </div>
          </vs-tab>
          <vs-tab label="Participants" icon-pack="feather" icon="icon-info">
            <div class="tab-text">
              <event-edit-tab-participants class="mt-4" :data="event_data.participants"/>
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
    EventEditTabParticipants
  },
  data () {
    return {
      event_data: null,
      event_not_found: false,
      activeTab: 0
    }
  },
  watch: {
    activeTab () {
      this.fetch_event(this.$route.params.eventId)
    }
  },
  methods: {
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
    console.log('route', this.$route.params.eventId)
    this.fetch_event(this.$route.params.eventId)
    this.$store.dispatch('calendar/fetchEventChoices')
  }
}

</script>
