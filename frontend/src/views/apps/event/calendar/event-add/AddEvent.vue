<template>
  <div id="event-calendar-add-event">
    <vs-popup
        :active.sync="isPopupActiveLocal"
        class="my-prompt"
        :title="$t('Event detail')">

      <div class="vx-row">
        <div class="vx-col sm:w-1/2 w-full">
          <div class="mt-4">
            <label class="text-sm">{{ $t('Event type') }} </label>
            <!-- RES: https://vue-select.org/ -->
            <v-select :clearable="false"
                      label="displayName"
                      :reduce="item => item.id"
                      v-model="eventType"
                      :options="this.$store.state.calendar.eventConfig.types"/>
          </div>
        </div>
        <div class="vx-col sm:w-1/2 w-full">
          <div class="mt-4">
            <label class="text-sm">{{ $t('Location') }}</label>
            <v-select :clearable="false"
                      label="displayName"
                      :reduce="item => item.id"
                      v-model="location"
                      :options="this.$store.state.calendar.eventConfig.locations"/>
          </div>
        </div>
      </div>

      <div class="vx-row">
        <div v-if="this.needSkis" class="vx-col w-1/2">
          <div class="mt-4">
            <label class="text-sm">{{ $t('Skis') }}</label>
            <ul class="demo-alignment my-checkbox-alignment">
              <li :key="item.id" v-for="item in this.$store.state.calendar.eventConfig.skis">
                <vs-checkbox
                    :vs-value="item.id"
                    color="success"
                    v-model="skisType">
                  {{ item.displayName }}
                </vs-checkbox>
              </li>
            </ul>
          </div>
        </div>

        <div v-if="this.isSkiRace" class="vx-col w-1/2">
          <div class="mt-4">
            <label class="text-sm">{{ $t('Organizer') }}</label>
            <v-select :clearable="false"
                      label="displayName"
                      :reduce="item => item.id"
                      v-model="raceOrganizer"
                      :options="this.$store.state.calendar.eventConfig.organizers"/>
          </div>
        </div>
      </div>

      <div class="mt-4">
        <label class="text-sm">{{ $t('Category') }}</label>
        <v-select multiple
                  :closeOnSelect="false"
                  label="displayName"
                  :reduce="item => item.id"
                  v-model="category"
                  :options="this.$store.state.calendar.eventConfig.categories"/>
      </div>

      <!-- Datepicker all day / with time -->
      <div class="mt-4">

        <div class="vx-row">
          <div class="vx-col w-full">
            <vs-checkbox
                color="success"
                @change="changeAllDay"
                v-model="data.allDay">
              {{ $t('All day') }}
            </vs-checkbox>
          </div>
        </div>

        <div class="vx-row" v-if="render">
          <div class="vx-col sm:w-1/2 w-full">
            <div class="mt-4">
              <label class="text-sm">{{ $t('Start') }}</label>
              <flat-pickr v-model="data.start"
                          :config="datePickerConfig"
                          class="w-full"
                          v-validate="'required'"
                          name="start"/>
              <span class="text-danger text-sm" v-show="errors.has('start')">{{ errors.first('start') }}</span>
            </div>
          </div>
          <div class="vx-col sm:w-1/2 w-full">
            <div class="mt-4">
              <label class="text-sm">{{ $t('End') }}</label>
              <flat-pickr v-model="data.end"
                          :config="datePickerConfig"
                          class="w-full"
                          name="end"/>
              <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Save & Reset Button -->
      <div class="vx-row">
        <div class="vx-col w-full">
          <div class="mt-8 flex flex-wrap items-center justify-end">
            <vs-button class="ml-auto mt-2" @click="submitData">{{ $t('Create') }}</vs-button>
            <vs-button class="ml-4 mt-2" type="border" @click="close"
                       color="warning">Cancel
            </vs-button>
          </div>
        </div>
      </div>
    </vs-popup>
  </div>
</template>

<script>
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css'

import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { Slovak } from 'flatpickr/dist/l10n/sk.js'

export default {
  props: {
    isPopupActive: {
      type: Boolean,
      required: true
    },
    data: {
      type: Object,
      default: () => {}
    }
  },
  components: {
    flatPickr,
    'v-select': vSelect
  },
  data () {
    return {
      render: true,

      category: [],
      location: [],
      skisType: [],
      raceOrganizer: [],
      eventType: [],

      datePickerConfig: {
        locale: Slovak,
        enableTime: true,
        altInput: true,
        allowInput: true,
        altFormat: 'd.m.Y H:i'
      }
    }
  },
  watch: {
    isPopupActive (val) {
      if (!val) return
      this.initValues()
    }
  },
  computed: {
    start () {
      return this.data.start
    },
    isPopupActiveLocal: {
      get () {
        return this.isPopupActive
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
      return this.eventType.length <= 0 ? false : this.$store.getters['calendar/needSkis'](this.eventType)
    },
    isSkiRace () {
      return this.eventType.length <= 0 ? false : this.$store.getters['calendar/isSkiRace'](this.eventType)
    }
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
      if (this.data.allDay) {
        this.data.end = this.moment(this.data.end).add(-1, 'second').toDate()
        // console.log('this.data.allDay', this.data.end)
      }
      if (!this.datePickerConfig.enableTime && !this.data.allDay) {
        this.data.end = this.moment(this.data.end).add(1, 'second').toDate()
        // console.log('this.data.else', this.data.end)
      }
      this.datePickerConfig.enableTime = !this.data.allDay
      this.datePickerConfig.altFormat = this.data.allDay ? 'd.m.Y' : 'd.m.Y H:i'
      // RES: https://github.com/fullcalendar/fullcalendar/issues/3679
      console.log('this.data.end', this.data.end)

      this.reloadDatepicker()
    },
    initValues (force = false) {
      this.changeAllDay()
      if (!force && this.category.length > 0) return
      console.log('init values force', !force)
      console.log('init values category', this.category)
      this.category = this.$store.state.calendar.eventConfig.categories.map(x => x.id)
      this.eventType = this.$store.state.calendar.eventConfig.types[0].id
      this.location = this.$store.state.calendar.eventConfig.locations[0].id
      this.skisType = this.$store.state.calendar.eventConfig.skis.map(x => x.id)
      this.organizer = this.$store.state.calendar.eventConfig.organizers[0].id
    },
    submitData () {
      const payload = {
        start: this.data.start,
        end: this.data.allDay ? this.moment(this.data.end).add(1, 'day').toDate() : this.data.end,
        all_day: this.data.allDay,
        category: this.category,
        location: this.location,
        skis_type: this.skisType,
        organizer: this.raceOrganizer,
        type: this.eventType,
        // TODO: auto resourcetype in axios
        resourcetype: this.$store.getters['calendar/getResourceType'](this.eventType)
      }
      this.$store.dispatch('calendar/addEvent', payload).then(() => {
        this.$vs.notify({
          color: 'success',
          title: 'Event Created',
          text: 'Your event was successfully created!'
        })
        this.$emit('closePrompt')
        this.initValues(true)
      }).catch(err => {
        console.error(err.response.data)
        this.$vs.notify({
          color: 'danger',
          title: 'Cannot create event',
          text: 'Check the fields and try again'
        })
        // PREVENT PROMT FFROM CLOSING
        this.$emit('closePrompt', true)
      })
    },
    close () {
      this.isPopupActiveLocal = false
      // this.$vs.notify({
      //   color: 'warning',
      //   title: 'Closed',
      //   text: 'You close a dialog!'
      // })
    }
  }
}
</script>

<style lang="scss">
.my-prompt {
  .vs-dialog {
    max-width: 650px;
  }
}

@media only screen and (max-width: 570px) {
  .my-prompt {
    .vs-dialog {
      max-width: 90%;
    }
  }
}

.my-checkbox-alignment {
  & > * {
    margin-right: .5rem;
    margin-top: .4rem;
  }
}

</style>
