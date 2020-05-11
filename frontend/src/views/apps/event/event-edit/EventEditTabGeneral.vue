<template>
  <div id="user-edit-tab-info">
    <p>{{data}}</p>
    <br>
    <p>{{data_local}}</p>
    <br>

    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2">
        <!-- Col Content -->
        <div>
          <!-- DOB -->

          <div class="mt-4">
            <label class="text-sm">Start</label>
            <flat-pickr v-model="data_local.start"
                        :config="datePickerConfig"
                        class="w-full"
                        v-validate="'required'" name="start"/>
            <span class="text-danger text-sm" v-show="errors.has('start')">{{ errors.first('start') }}</span>
          </div>

          <div class="mt-4">
            <label class="text-sm">End</label>
            <flat-pickr v-model="data_local.end"
                        :config="datePickerConfig" class="w-full"
                        v-validate="'required'" name="dob"/>
            <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
          </div>

          <div class="mt-4">
            <label class="text-sm">Categories</label>
            <!-- RES: https://vue-select.org/ -->
            <v-select multiple
                      :closeOnSelect="false"
                      label="displayName"
                      :reduce="category => category.id"
                      v-model="data_local.category"
                      :options="getCategories"/>
          </div>

          <div v-if="data_local.skis_type" class="mt-4">
            <span slot="off">Skis type</span>
            <div class="mt-2">
              <vs-radio v-model="data_local.skis_type" vs-value="ALL" class="mr-4">All</vs-radio>
              <vs-radio v-model="data_local.skis_type" vs-value="SG" class="mr-4">SG</vs-radio>
              <vs-radio v-model="data_local.skis_type" vs-value="SL">SL</vs-radio>
            </div>
          </div>

          <!-- Gender -->
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
    getCategories () {
      return this.$store.state.calendar.eventConfig.categories
    }
  },
  created () {
    this.$store.dispatch('calendar/fetchCategories')
  },
  methods: {
    save_changes () {
      /* eslint-disable */
      if (!this.validateForm) return
      console.log('Save changes with data', this.data_local)

      // FIXME
      const event = Object.assign({}, this.data_local)
      delete event['season']
      delete event['category']
      delete event['location']

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
    reset_data () {
      this.data_local = Object.assign({}, this.data)
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
