<template>
  <!-- TODO: Add some extra data about event -->
  <div id="event-calendar-view-event-tab-general">
    <div class="vx-row">
      <div class="vx-col flex-1">
        <table>
          <tr>
            <td class="font-bold">{{ $t('Logged in') }}</td>
            <td>{{ event.participants.length }}</td>
          </tr>
          <tr>
            <td class="font-bold">{{ $t('Location') }}</td>
            <td>{{ event.location.displayName }}</td>
          </tr>
          <tr>
            <td class="font-bold">{{ $t('Category') }}</td>
            <td>{{ displayObject(event.category) }}</td>
          </tr>
          <tr v-if="event.type.need_skis">
            <td class="font-bold">{{ $t('Skis') }}</td>
            <td>{{ displayObject(event.skis_type) }}</td>
          </tr>
          <tr v-if="event.additional_info">
            <td class="font-bold">{{ $t('Additional Information') }}</td>
            <td>{{ event.additional_info }}</td>
          </tr>
        </table>
      </div>
    </div>

    <!-- TODO: Child on event list -->

    <!--    <div v-if="!(Array.isArray(event.accommodation) && event.accommodation.length > 0)"-->
    <!--         class="flex flex-wrap items-center justify-end mt-5">-->
    <!--      <vs-button icon-pack="material-icons" icon="hotel" type="border" color="warning" class="mt-4"-->
    <!--                 :to="{name: 'app-event-edit', hash:'#accommodation', params: { eventId: this.event.id }}">-->
    <!--        Accommodation-->
    <!--      </vs-button>-->
    <!--    </div>-->

  </div>
</template>

<script>
export default {
  props: {
    data: {
      type: Object,
      default: () => {}
    }
  },
  computed: {
    event () {
      return this.$store.getters['calendar/getEvent'](this.data.id)
    }
  },
  methods: {
    displayObject (object, displayKey = 'displayName') {
      return Object.values(object).map(item => item[displayKey]).toString()
    }
  }
}
</script>
