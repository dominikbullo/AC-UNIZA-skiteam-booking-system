<template>
  <div id="user-edit-tab-info">
    <!--    <pre>{{data_local}}</pre>-->
    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2">
        <!-- Col Content -->
        <div>
          <!-- DOB -->
          <vs-input class="w-full mt-4" label="Event Title" v-model="data_local.title"
                    v-validate="{regex: '^\\+?([0-9]+)$' }" name="mobile"/>
          <span class="text-danger text-sm" v-show="errors.has('mobile')">{{ errors.first('mobile') }}</span>

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

          <!-- Gender -->
          <!-- TODO: fetch types from server-->
          <div class="mt-4">
            <span slot="off">Skis type</span>

            <!--            <div class="flex items-center mb-4 mt-2">-->
            <!--              <vs-switch color="danger" vs-value="SG" v-model="data_local.skis_type"/>-->
            <!--              <span class="ml-4">Cancel this event</span>-->
            <!--            </div>-->

            <!--            <div class="flex items-center mb-4 mt-2">-->
            <!--              <vs-switch color="danger" vs-value="SL" v-model="data_local.skis_type"/>-->
            <!--              <span class="ml-4">Cancel this event</span>-->
            <!--            </div>-->


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
                           @click="delete_event">Delete event
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
            <vs-textarea class="w-full" height="110px" v-model="data_local.additional_info"
                         placeholder="Additional information about event..."/>
          </div>

          <!--          <div class="centerx">-->
          <!--            <vs-input-number v-model="data_local.temperature" min="-50" label="passengers:"/>-->
          <!--            <vs-input-number v-model="data_local.gates" label="passengers:"/>-->
          <!--            <vs-input-number v-model="data_local.number_of_runs" label="passengers:"/>-->
          <!--          </div>-->
          <!-- TODO: Fetch categories -->
          <vs-input class="w-full mt-4" label="Category" v-model="data_local.location.add_line_1"
                    v-validate="'required'" name="addd_line_1"/>
          <span class="text-danger text-sm"
                v-show="errors.has('addd_line_1')">{{ errors.first('addd_line_1') }}</span>

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
        altFormat: 'd.m.Y H:i',
        maxDate: new Date()
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
    }
  },
  methods: {
    save_changes () {
      /* eslint-disable */
      if (!this.validateForm) return
      console.log('Save changes with data', this.data_local)

    },
    reset_data () {
      this.data_local = Object.assign({}, this.data)
    },
    delete_event () {
      console.log('id', this.data.id)
      this.$http.delete(`/event/${this.data.id}/`)
        .then(response => {
          console.log('response', response)
          this.$vs.notify({
            color: 'success',
            title: 'Event Deleted',
            text: 'Event has been deleted successfully'
          })
          this.$router.push({ name: 'app-event-calendar' }).catch(() => {
          })
        })
    }
  }
}
</script>
