<template>
  <div id="event-edit-tab-general">
    <!--    <p>{{data}}</p>-->
    <!--    <br>-->
    <!--    <p>{{data_local}}</p>-->
    <!--    <br>-->

    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2">

        <div class="vx-row mt-4">
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
                    :reduce="item => item.id"
                    v-model="data_local.category"
                    :options="categories"/>
        </div>

        <div class="vx-row mt-4">
          <!--          TODO: Cannot change type, because of aplication logic, but maybe they will want to-->
          <!--          <div class="vx-col w-1/2">-->
          <!--            <label class="text-sm">Event type</label>-->
          <!--            <v-select :clearable="false"-->
          <!--                      label="displayName"-->
          <!--                      :reduce="item => item.id"-->
          <!--                      v-model="data_local.type"-->
          <!--                      :options="choices.EventTypeChoices"/>-->
          <!--            <span class="text-danger text-sm" v-show="errors.has('start')">{{ errors.first('start') }}</span>-->
          <!--          </div>-->

          <div class="vx-col w-1/2">
            <label class="text-sm">Location</label>
            <v-select :clearable="false"
                      label="displayName"
                      :reduce="item => item.id"
                      v-model="data_local.location"
                      :options="locations"/>
            <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
          </div>


          <div v-if="data_local.skis_type" class="vx-col w-1/2 mt-4">
            <span slot="off">Skis type</span>

            <div class="mt-2">
              <vs-radio :key="item.key" v-for="item in this.choices.SkiTypeChoices"
                        v-model="data_local.skis_type"
                        :vs-value="item.key"
                        vs-w="6"
                        class="mr-4">
                <span class="sm:inline hidden">{{item.displayName}}</span>
              </vs-radio>
            </div>
          </div>
          <div v-if="data_local.type === 'SKI_RACE'" class="vx-col w-1/2">
            <label class="text-sm">Race Organizer</label>
            <v-select :clearable="false"
                      label="displayName"
                      :reduce="item => item.id"
                      v-model="data_local.organizer"
                      :options="organizers"/>
            <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
          </div>
        </div>


        <div class="mt-4">
          <div class="vx-col w-full">
            <div class="mt-8 flex flex-wrap items-center">
              <!--                <vs-button class="mt-2" icon-pack="feather" icon="icon-x" type="border" color="warning"-->
              <!--                           @click="reset_data">Cancel event-->
              <!--                </vs-button>-->
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

      data_local: JSON.parse(JSON.stringify(this.data)),

      datePickerConfig: {
        locale: Slovak,
        enableTime: true,
        altInput: true,
        altFormat: 'd.m.Y H:i'
      },
      email: this.data.canceled,

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
    locations () {
      return this.$store.state.calendar.eventConfig.locations
    },
    organizers () {
      return this.$store.state.calendar.eventConfig.organizers
    },
    choices () {
      return this.$store.state.calendar.eventConfig.choices
    }

  },
  created () {
    this.$store.dispatch('calendar/fetchCategories')
    this.$store.dispatch('calendar/fetchLocations')
    this.$store.dispatch('calendar/fetchRaceOrganizers')
    this.$store.dispatch('calendar/fetchEventChoices')
    this.reset_data()
  },
  methods: {
    save_changes () {
      /* eslint-disable */
      if (!this.validateForm) return
      console.log('Save changes with data', this.data_local)

      // FIXME
      const event = Object.assign({}, this.data_local)
      delete event['season']

      this.$store.dispatch('calendar/editEvent', event)
        .then(res => {
          this.$vs.notify({
            color: 'success',
            title: 'Event Deleted',
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
    cleanData (data, key = 'id') {
      const cleanData = []
      Object.values(data).forEach((element) => {
        cleanData.unshift(element[key])
      })
      return cleanData
    },
    reset_data () {
      // TODO: Maybe not neet to include some stuf -> later cleanup
      this.data_local = Object.assign({}, this.data)


      this.data_local.category = this.cleanData(this.data.category)
      this.data_local.location = this.data_local.location.id

      if (this.data.hasOwnProperty('organizer')) {
        this.data_local.organizer = this.data_local.organizer.id
      }
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
