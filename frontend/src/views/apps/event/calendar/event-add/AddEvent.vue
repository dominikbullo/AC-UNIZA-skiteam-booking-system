<template>
  <div id="event-calendar-add-event">
    <vs-prompt
        :active.sync="isSidebarActiveLocal"
        @accept="submitData"
        :accept-text="$t('Save')"
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

      <div class="vx-row">
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
                        v-validate="'required'"
                        name="end"/>
            <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
          </div>
        </div>
      </div>
    </vs-prompt>
  </div>
</template>

<script>
import vSelect from 'vue-select'
// import 'vue-select/dist/vue-select.css'

import flatPickr from 'vue-flatpickr-component'
// import 'flatpickr/dist/flatpickr.css'
import { Slovak } from 'flatpickr/dist/l10n/sk.js'

export default {
  props: {
    isSidebarActive: {
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
      category: [],
      location: [],
      skisType: [],
      raceOrganizer: [],
      eventType: [],

      datePickerConfig: {
        locale: Slovak,
        enableTime: true,
        altInput: true,
        altFormat: 'd.m.Y H:i'
      }
    }
  },
  watch: {
    isSidebarActive (val) {
      if (!val) return
      this.initValues()
    }
  },
  computed: {
    isSidebarActiveLocal: {
      get () {
        return this.isSidebarActive
      },
      set (val) {
        if (!val) {
          this.$emit('closePrompt')
          this.$validator.reset()
          this.initValues()
        }
      }
    },
    isFormValid () {
      // FIXME: validate test
      return !this.errors.any() && this.dataName && this.dataPrice > 0
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
        end: this.data.end,
        category: this.category,
        location: this.location,
        skis_type: this.skisType,
        organizer: this.raceOrganizer,
        type: this.eventType,
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
