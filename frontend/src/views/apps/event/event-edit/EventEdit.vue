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
      {{event_data}}
    </vx-card>
  </div>
</template>

<script>

export default {
  data () {
    return {
      event_data: null,
      event_not_found: false
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
  }
}

</script>
