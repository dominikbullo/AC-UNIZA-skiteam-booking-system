<template>
  <div id="event-calendar-add-event">
    <vs-prompt
        buttons-hidden
        :active.sync="isPromptActiveLocal"
        :accept-text="$t('Ok')"
        class="my-prompt"
        :title="$t('Event detail')">
      <vs-tabs style="overflow: auto">
        <vs-tab label="General">
          <view-event-tab-general @closeDeleted="isPromptActiveLocal=false" :data="data"/>
        </vs-tab>
        <vs-tab label="Detail">
          <view-event-tab-detail :data="data"/>
        </vs-tab>
        <vs-tab label="Accommodation" v-if="Array.isArray(data.accommodation) && data.accommodation.length > 0">
          <view-event-tab-accommodation :data="data"/>
        </vs-tab>
      </vs-tabs>
    </vs-prompt>
  </div>
</template>

<script>
import ViewEventTabGeneral from './ViewEventTabGeneral'
import ViewEventTabDetail from './ViewEventTabDetail'
import ViewEventTabAccommodation from './ViewEventTabAccommodation'

export default {
  props: {
    isPromptActive: {
      type: Boolean,
      required: true
    },
    data: {
      type: Object,
      default: () => {}
    }
  },
  components: {
    ViewEventTabGeneral,
    ViewEventTabDetail,
    ViewEventTabAccommodation
  },
  data () {
    return {
      tmpParticipants: []
    }
  },
  watch: {
    isPromptActive (val) {
      if (!val) return
      this.initValues()
    }
  },
  computed: {
    isPromptActiveLocal: {
      get () {
        return this.isPromptActive
      },
      set (val) {
        if (!val) {
          this.$emit('closePrompt')
          this.$validator.reset()
          this.initValues()
        }
      }
    },
    needSkis () {
      if (this.eventType.length <= 0) {
        return false
      }
      return this.$store.getters['calendar/needSkis'](this.eventType)
    },
    isSkiRace () {
      if (this.eventType.length <= 0) {
        return false
      }
      return this.$store.getters['calendar/isSkiRace'](this.eventType)
    }
  },
  methods: {
    initValues (force = false) {
      if (!force || this.category.length > 0) return
      this.category = this.$store.state.calendar.eventConfig.categories.map(x => x.id)
      this.eventType = this.$store.state.calendar.eventConfig.types[0].id
      this.location = this.$store.state.calendar.eventConfig.locations[0].id
      this.skisType = this.$store.state.calendar.eventConfig.skis.map(x => x.id)
      this.organizer = this.$store.state.calendar.eventConfig.organizers[0].id
    }
  }
}
</script>
