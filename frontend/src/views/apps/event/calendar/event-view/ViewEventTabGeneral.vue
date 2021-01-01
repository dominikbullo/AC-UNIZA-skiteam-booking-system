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
      <!-- TODO: Coach going to event checkbox -->
      <div class="vx-col w-full flex flex-wrap items-center justify-center">

        <div class="mb-5 vx-row switch-toggle switch-3 switch-candy">
          <input id="on" name="state-d" class="toggle-on" type="radio" checked=""/>
          <label for="on" onclick="">
            <feather-icon icon="CheckIcon" svgClasses="w-6 h-6 text-white"></feather-icon>
          </label>
          <input id="na" name="state-d" class="toggle-unset" type="radio" disabled checked="checked"/>
          <label for="na" class="disabled" onclick="">&nbsp;</label>
          <input id="off" name="state-d" class="toggle-off" type="radio"/>
          <label for="off" onclick="">
            <feather-icon icon="XIcon" svgClasses="w-6 h-6 text-white"></feather-icon>
          </label>
        </div>

        <div class="vx-row w-full flex flex-wrap items-center justify-center">
          <vs-button icon-pack="feather" icon="icon-edit" class="mr-4"
                     :to="{name: 'app-event-edit', params: { eventId: this.data.id}}">
            Edit event
          </vs-button>
          <vs-button type="border" icon="group" class="mr-4"
                     :to="{name: 'app-event-edit', hash:'#participants', params: { eventId: this.data.id }}">
            Edit participants
          </vs-button>
          <vs-button type="border" color="danger" icon-pack="feather" icon="icon-trash"
                     @click="deletePopup=true">
            Delete
          </vs-button>
        </div>
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

    <!-- TODO: v-for from store not from responses-->
    <div class="mb-2 vx-row mx-auto self-center" :key="item.user_to_event.id" v-for="item in this.mergedResponses">

      <!-- RES: https://stackoverflow.com/questions/23661970/3-state-css-toggle-switch -->
      <div class="switch-toggle switch-3 switch-candy mr-2">
        <input class="toggle-yes" type="radio" :name="'cs-' + item.user_to_event.id"
               :id="'children-radio-on-' + item.user_to_event.id" :checked="item.going"
               @change="changeValue(true, item.user_to_event.id)">
        <label :for="'children-radio-on-' + item.user_to_event.id">
          <feather-icon icon="CheckIcon" svgClasses="w-6 h-6 text-white"></feather-icon>
        </label>
        <input class="toggle-unset" type="radio" :name="'cs-' + item.user_to_event.id"
               :id="'children-radio-na-' + item.user_to_event.id" disabled :checked="item.going==null">
        <label :for="'children-radio-na-' + item.user_to_event.id">&nbsp;</label>
        <input class="toggle-no" type="radio" :name="'cs-' + item.user_to_event.id"
               :id="'children-radio-off-' + item.user_to_event.id"
               @change="changeValue(false, item.user_to_event.id)" :checked="item.going===false">
        <label :for="'children-radio-off-' + item.user_to_event.id">
          <feather-icon icon="XIcon" svgClasses="w-6 h-6 text-white"></feather-icon>
        </label>
      </div>

      <p class="self-center">{{ item.user_to_event.displayName }}</p>
    </div>
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
      merged: [],
      deletePopup: false,
      selectedChildren: []
    }
  },
  computed: {
    event () {
      return this.$store.getters['calendar/getEvent'](this.data.id)
    },
    mergedResponses () {
      // console.log(' this.$store.getters[\'family/familyChildren\']', this.$store.getters['family/familyChildren'])
      const familyChildren = this.$store.getters['family/familyChildren'].map(x => x.user.profile.id)
      const mergedStore = this.$store.getters['calendar/getEventMergedResponses'](this.data.id)
      if (mergedStore) {
        return mergedStore.filter(x => familyChildren.includes(x.user_to_event.id))
      }
      return []
    }
  },
  methods: {
    changeValue (going, id) {
      const payload = {
        'eventID': this.event.id,
        'data': {
          going,
          'user_to_event': id
        }
      }
      // TODO: vs.notify
      this.$store.dispatch('calendar/addEventResponse', payload)
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
  }
}
</script>
<style>
.switch-toggle {
  float: left;
  background: #10163a;
}

.switch-toggle input {
  position: absolute;
  opacity: 0;
}

.switch-toggle input + label {
  padding: 5px;
  min-width: 3em;
  text-align: center;
  float: left;
  color: #fff;
  cursor: pointer;
}

.switch-toggle input:checked.toggle-no + label {
  background-color: red;
  height: 100%;
}

.switch-toggle input:checked.toggle-yes + label {
  background-color: green;
  height: 100%;
}

.switch-toggle input:checked.toggle-unset + label {
  background-color: orange;
}

.switch-toggle input.toggle-unset + label {
  cursor: not-allowed;
  height: 100%;
}
</style>
