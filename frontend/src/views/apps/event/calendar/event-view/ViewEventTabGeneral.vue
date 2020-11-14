<template>
  <div id="event-calendar-view-event-tab-general">
    <div class="vx-row">
      <div class="vx-col flex-1" id="event-general-col-1">
        <table>
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

    <div v-if="$acl.check('isCoach')">
      <vs-divider>{{ $t('Coach zone') }}</vs-divider>
      <div class="vx-col w-full flex flex-wrap items-center justify-center">

        <vs-button icon-pack="feather" icon="icon-edit" class="mr-4"
                   :to="{name: 'app-event-edit', params: { eventId: this.data.id}}">
          Edit event
        </vs-button>

        <vs-button type="border" icon="group" class="mr-4"
                   :to="{name: 'app-event-edit', hash:'#participants', params: { eventId: this.data.id }}">
          Edit participants
        </vs-button>

        <vs-button type="border" color="danger" icon-pack="feather" icon="icon-trash"
                   @click="deletePopup=true">Delete
        </vs-button>
      </div>

      <vs-popup title="Delete event" :active.sync="deletePopup">
        <p>You are about to delete event. Do you really want to ?</p>
        <!-- TODO: Send notification options -->
        <!-- Delete & Cancel Button -->
        <div class="flex flex-wrap items-center justify-end mt-5">
          <vs-button class="ml-auto mt-2" color="danger" @click="deleteEvent">Delete</vs-button>
          <vs-button class="ml-4 mt-2" type="border" @click="deletePopup=false">Cancel</vs-button>
        </div>
      </vs-popup>

    </div>

    <vs-divider>{{ $t('Your children') }}</vs-divider>
    <ul class="centerx">
      <li class="mb-2" :key="child.user.profile.id" v-for="child in this.$store.getters['family/familyChildren']">
        <vs-checkbox
            :vs-value="child.user.profile.id"
            color="success"
            v-model="selectedChildren"
            @change="changeParticipants">
          {{ child.user.profile.displayName }}
        </vs-checkbox>
      </li>
    </ul>

  </div>
</template>

<script>
import vSelect from 'vue-select'

import flatPickr from 'vue-flatpickr-component'
import { Slovak } from 'flatpickr/dist/l10n/sk.js'

export default {
  props: {
    data: {
      type: Object,
      default: () => {
      }
    },
    savedParticipants: {
      type: Array,
      default: () => []
    }
  },
  components: {
    flatPickr,
    'v-select': vSelect
  },
  data () {
    return {
      deletePopup: false,
      selectedChildren: []
    }
  },
  computed: {
    event () {
      return this.$store.getters['calendar/getEvent'](this.data.id)
    }
  },
  methods: {
    changeParticipants () {
      const payload = {
        'id': this.data.id,
        'data': this.selectedChildren
      }
      this.$store.dispatch('calendar/changeEventMembers', payload)
    },
    displayObject (object, displayKey = 'displayName') {
      return Object.values(object).map(item => item[displayKey]).toString()
    },
    deleteEvent () {
      this.deletePopup = false
      this.$store.dispatch('calendar/deleteEvent', this.data)
        .then(res => {
          this.$emit('closeDeleted')
          this.$vs.notify({
            color: 'success',
            title: 'Event Deleted',
            text: 'The selected event was successfully deleted'
          })
        })
        .catch(err => {
          this.$vs.notify({
            color: 'danger',
            title: 'Event Not Deleted',
            text: 'The selected user was successfully deleted'
          })
          console.error(err)
        })
    }
  },
  created () {
    this.$store.dispatch('family/fetchFamily', this.$store.getters['familyID']).then(() => {

      console.log(this.$store.getters['family/familyChildren'])
      const childrenUsersID = this.$store.getters['family/familyChildren'].map(e => e.user.profile.id)
      console.log('childrenUsersID', childrenUsersID)

      const eventChildren = Object.values(this.event.participants).map(e => e.id)
      console.log('eventChildren', eventChildren)

      const userChildrenOnEvent = childrenUsersID.filter(x => eventChildren.includes(x))
      console.log('userChildrenOnEvent', userChildrenOnEvent)

      this.selectedChildren = userChildrenOnEvent
    })
  }
}
</script>
