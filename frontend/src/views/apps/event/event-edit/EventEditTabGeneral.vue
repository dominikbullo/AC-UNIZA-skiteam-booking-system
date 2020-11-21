<template>
  <div id="event-edit-tab-general">
    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2">
        <!-- Datepicker all day / with time -->
        <div class="vx-col w-full">
          <vs-checkbox
              color="success"
              @change="changeAllDay"
              v-model="data_local.all_day">
            {{ $t('All day') }}
          </vs-checkbox>
        </div>
      </div>
    </div>
    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2">
        <div class="vx-row mt-4" v-if="render">
          <div class="vx-col w-1/2">
            <label class="text-sm">Start</label>
            <flat-pickr v-model="data_local.start"
                        :config="datePickerConfig"
                        class="w-full"
                        v-validate="'required'" name="start"/>
            <span class="text-danger text-sm" v-show="errors.has('start')">{{ errors.first('start') }}</span>
          </div>
          <div class="vx-col w-1/2">
            <label class="text-sm">End</label>
            <flat-pickr v-model="data_local.end"
                        :config="datePickerConfig" class="w-full"
                        v-validate="'required'" name="dob"/>
            <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
          </div>
        </div>

        <div class="mt-4">
          <label class="text-sm">Categories</label>
          <!-- RES: https://vue-select.org/ -->
          <v-select multiple
                    :closeOnSelect="false"
                    label="displayName"
                    v-model="data_local.category"
                    :options="categories"/>
        </div>

        <div class="vx-row mt-4">
          <div class="vx-col w-1/2">
            <label class="text-sm">Location</label>
            <v-select :clearable="false"
                      label="displayName"
                      v-model="data_local.location"
                      :options="locations"/>
            <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
          </div>


          <div v-if="data_local.skis_type" class="vx-col w-1/2">
            <label class="text-sm">Skis type</label>
            <ul class="centerx">
              <v-select multiple
                        :closeOnSelect="false"
                        :clearable="false"
                        label="displayName"
                        v-model="data_local.skis_type"
                        :options="skis"/>
            </ul>
          </div>

          <div v-if="this.isSkiRace" class="vx-col w-1/2 mt-2">
            <label class="text-sm">Race Organizer</label>
            <v-select :clearable="false"
                      label="displayName"
                      v-model="data_local.organizer"
                      :options="organizers"/>
            <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
          </div>
        </div>


        <div class="mt-4">
          <div class="vx-col w-full">
            <div class="mt-8 flex flex-wrap items-center">
              <vs-button class="mt-2" icon-pack="feather" icon="icon-trash-2" type="border" color="danger"
                         @click="deleteEvent">Delete event
              </vs-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 2nd Col -->
      <div class="vx-col w-full md:w-1/2">
        <div>

          <!-- Bio -->
          <div class="mt-4">
            <label class="text-sm">Additional information</label>
            <vs-textarea id="text-area-edit-event" class="w-full" v-model="data_local.additional_info"
                         placeholder="Additional information about event..."/>
          </div>


          <div class="mt-6">
            <label>Options</label>

            <div class="flex items-center mb-4 mt-2">
              <vs-switch color="danger" v-model="data_local.canceled">
                <span slot="on">Canceled</span>
                <span slot="off">Cancel</span>
              </vs-switch>
              <span class="ml-4">Cancel this event</span>
            </div>

            <div class="flex items-center mb-4">
              <vs-switch v-model="data_local.send_email"/>
              <span class="ml-4">Send email to all users about this event</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Save & Reset Button -->
    <div class="vx-row">
      <div class="vx-col w-full">
        <div class="mt-8 flex flex-wrap items-center justify-end">
          <vs-button class="ml-auto mt-2" @click="save_changes" :disabled="!validateForm">Save Changes</vs-button>
          <vs-button class="ml-4 mt-2" type="border" color="warning" @click="reset_data">Reset</vs-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { Slovak } from 'flatpickr/dist/l10n/sk.js'

import vSelect from 'vue-select'

export default {
  components: {
    vSelect,
    flatPickr
  },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      render: true,
      data_local: Object.assign({}, this.data),

      datePickerConfig: {
        locale: Slovak,
        enableTime: true,
        allowInput: true,
        altInput: true,
        altFormat: 'd.m.Y H:i'
      },

      langOptions: [
        {
          label: 'English',
          value: 'english'
        },
        {
          label: 'Slovak',
          value: 'slovak'
        }
      ]
    }
  },
  computed: {
    validateForm () {
      return !this.errors.any()
    },
    categories () {
      return this.$store.state.calendar.eventConfig.categories
    },
    skis () {
      return this.$store.state.calendar.eventConfig.skis
    },
    locations () {
      return this.$store.state.calendar.eventConfig.locations
    },
    organizers () {
      return this.$store.state.calendar.eventConfig.organizers
    },
    choices () {
      return this.$store.state.calendar.eventConfig.choices
    },
    isSkiRace () {
      // FIXME: via store
      return this.data.type.type === 'RACE' && this.data.type.need_skis === true
    }
  },
  created () {
    this.$store.dispatch('calendar/fetchEventTypes')
    this.$store.dispatch('calendar/fetchSkisTypes')
    this.$store.dispatch('calendar/fetchCategories')
    this.$store.dispatch('calendar/fetchLocations')
    this.$store.dispatch('calendar/fetchRaceOrganizers')
    this.changeAllDay()
  },
  methods: {
    // RES: https://medium.com/javascript-in-plain-english/many-ways-to-rerender-a-vue-component-660376d94cc1
    // RES: https://github.com/logaretm/vee-validate/issues/2109#issuecomment-589514549
    reloadDatepicker () {
      this.$validator.pause()
      this.render = false
      this.$nextTick(() => {
        this.$validator.errors.clear()
        this.$validator.fields.items.forEach(field => field.reset())
        this.$validator.fields.items.forEach(field => this.errors.remove(field))
        this.$validator.resume()
        this.render = true
      })
    },
    changeAllDay () {
      if (this.data_local.all_day) {
        this.data_local.end = this.moment(this.data_local.end).add(-1, 'second').toDate()
        console.log('this.data.end format****', this.data.end)
      }
      if (!this.datePickerConfig.enableTime && !this.data_local.all_day) {
        this.data_local.end = this.moment(this.data_local.end).add(1, 'second').toDate()
        console.log('this.data.end format****', this.data.end)
      }
      this.datePickerConfig.enableTime = !this.data_local.all_day
      this.datePickerConfig.altFormat = this.data_local.all_day ? 'd.m.Y' : 'd.m.Y H:i'

      this.reloadDatepicker()
    },
    save_changes () {
      /* eslint-disable */
      if (!this.validateForm) return

      const tmp = Object.assign({}, this.data_local)
      delete tmp.accommodation
      tmp.participants = this.data_local.participants.map(x => x.id)
      tmp.category = this.data_local.category.map(x => x.id)
      tmp.location = this.data_local.location.id
      tmp.type = this.data_local.type.id

      if (this.data_local.skis_type) {
        tmp.skis_type = this.data_local.skis_type.map(x => x.id)
      }
      if (this.data_local.organizer) {
        tmp.organizer = this.data_local.organizer.id
      }
      if (tmp.all_day) {
        tmp.end = this.moment(this.data.end).add(1, 'day')
      }

      this.$store.dispatch('calendar/editEvent', tmp)
          .then(res => {
            this.$vs.notify({
              color: 'success',
              title: 'Event Edited',
              text: 'The selected event was successfully edited'
            })
          })
          .catch(err => {
            this.$vs.notify({
              color: 'danger',
              title: 'Event Not Changed',
              text: err.message
            })
            console.error(err)
          })
    },
    reset_data () {
      this.data_local = Object.assign({}, this.data)
      this.changeAllDay()
    },
    deleteEvent () {
      this.$store.dispatch('calendar/deleteEvent', this.data)
          .then(res => {
            this.$router.push({ name: 'app-event-calendar' }).catch(() => {
            })
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
              text: 'The selected user wasn\'t  deleted'
            })
            console.error(err)
          })
    }
  }
}
</script>

<style>
#text-area-edit-event {
  min-height: 110px
}
</style>
