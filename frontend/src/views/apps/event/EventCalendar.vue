<template>
  <div id="simple-calendar-app">
    <div class="vx-card no-scroll-content">
      <calendar-view
        :displayPeriodUom="calendarView"
        :eventTop="windowWidth <= 400 ? '2rem' : '3rem'"
        :events="simpleCalendarEvents"
        :show-date="showDate"
        @click-date="openAddNewEvent"
        @click-event="openEditEvent"
        @drop-on-date="eventDragged"
        class="theme-default"
        enableDragDrop
        eventBorderHeight="0px"
        eventContentHeight="1.65rem"
        ref="calendar">

        <div class="mb-4" slot="header">

          <div class="vx-row no-gutter">

            <!-- Month Name -->
            <div class="vx-col w-1/3 items-center sm:flex hidden">
              <!-- Add new event button -->
              <vs-button @click="promptAddNewEvent(new Date())" icon="icon-plus" icon-pack="feather">Add</vs-button>
            </div>

            <!-- Current Month -->
            <div class="vx-col sm:w-1/3 w-full sm:my-0 my-3 flex sm:justify-end justify-center order-last">
              <div class="flex items-center">
                <feather-icon
                  :icon="$vs.rtl ? 'ChevronRightIcon' : 'ChevronLeftIcon'"
                  @click="updateMonth(-1)"
                  class="cursor-pointer bg-primary text-white rounded-full"
                  svgClasses="w-5 h-5 m-1"/>

                <span class="mx-3 text-xl font-medium whitespace-no-wrap">{{ showDate | month }}</span>

                <feather-icon
                  :icon="$vs.rtl ? 'ChevronLeftIcon' : 'ChevronRightIcon'"
                  @click="updateMonth(1)"
                  class="cursor-pointer bg-primary text-white rounded-full"
                  svgClasses="w-5 h-5 m-1"/>
              </div>
            </div>

            <div class="vx-col sm:w-1/3 w-full flex justify-center">
              <template v-for="(view, index) in calendarViewTypes">
                <vs-button
                  :class="{'border-l-0 rounded-l-none': index, 'rounded-r-none': calendarViewTypes.length !== index+1}"
                  :key="String(view.val) + 'filled'"
                  @click="calendarView = view.val"
                  class="p-3 md:px-8 md:py-3"
                  type="filled"
                  v-if="calendarView === view.val"
                >{{ view.label }}
                </vs-button>
                <vs-button
                  :class="{'border-l-0 rounded-l-none': index, 'rounded-r-none': calendarViewTypes.length !== index+1}"
                  :key="String(view.val) + 'border'"
                  @click="calendarView = view.val"
                  class="p-3 md:px-8 md:py-3"
                  type="border"
                  v-else
                >{{ view.label }}
                </vs-button>
              </template>

            </div>
          </div>

          <div class="vx-row sm:flex hidden mt-4">
            <div class="vx-col w-full flex">
              <!-- Labels -->
              <div class="flex flex-wrap sm:justify-start justify-center">
                <div :key="index" class="flex items-center mr-4 mb-2" v-for="(label, index) in calendarLabels">
                  <div :class="'bg-' + label.color" class="h-3 w-3 inline-block rounded-full mr-2"></div>
                  <span>{{ label.text }}</span>
                </div>
                <div class="flex items-center mr-4 mb-2">
                  <div class="h-3 w-3 inline-block rounded-full mr-2 bg-primary"></div>
                  <span>None</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </calendar-view>
    </div>

    <!-- ADD EVENT -->
    <vs-prompt
      :active.sync="activePromptAddEvent"
      :is-valid="validForm"
      @accept="addEvent"
      accept-text="Add Event"
      class="calendar-event-dialog"
      title="Add Event">

      <div class="calendar__label-container flex">

        <vs-chip :class="'bg-' + labelColor(labelLocal)" class="text-white" v-if="labelLocal != 'none'">{{ labelLocal
          }}
        </vs-chip>

        <vs-dropdown class="ml-auto my-2 cursor-pointer" vs-custom-content vs-trigger-click>

          <feather-icon @click.prevent class="cursor-pointer" icon="TagIcon" svgClasses="h-5 w-5"></feather-icon>

          <vs-dropdown-menu style="z-index: 200001">
            <vs-dropdown-item :key="index" @click="labelLocal = label.value" v-for="(label, index) in calendarLabels">
              <div :class="'bg-' + label.color" class="h-3 w-3 inline-block rounded-full mr-2"></div>
              <span>{{ label.text }}</span>
            </vs-dropdown-item>

            <vs-dropdown-item @click="labelLocal = 'none'">
              <div class="h-3 w-3 mr-1 inline-block rounded-full mr-2 bg-primary"></div>
              <span>None</span>
            </vs-dropdown-item>
          </vs-dropdown-menu>
        </vs-dropdown>

      </div>

      <vs-input class="w-full" label-placeholder="Event Title" name="event-name" v-model="title"
                v-validate="'required'"></vs-input>
      <div class="my-4">
        <small class="date-label">Start Date</small>
        <datepicker :disabled="disabledFrom" :language="$vs.rtl ? langHe : langEn" name="start-date"
                    v-model="startDate"></datepicker>
      </div>
      <div class="my-4">
        <small class="date-label">End Date</small>
        <datepicker :disabledDates="disabledDatesTo" :language="$vs.rtl ? langHe : langEn" name="end-date"
                    v-model="endDate"></datepicker>
      </div>
      <vs-input :color="!errors.has('event-url') ? 'success' : 'danger'" class="w-full mt-6"
                label-placeholder="Event URL" name="event-url" v-model="url"
                v-validate="'url'"></vs-input>

    </vs-prompt>

    <!-- EDIT EVENT -->
    <vs-prompt
      :active.sync="activePromptEditEvent"
      :is-valid="validForm"
      @accept="editEvent"
      @cancel="removeEvent"
      accept-text="Submit"
      button-cancel="border"
      cancel-text="Remove"
      class="calendar-event-dialog"
      title="Edit Event">

      <div class="calendar__label-container flex">

        <vs-chip :class="'bg-' + labelColor(labelLocal)" class="text-white" v-if="labelLocal != 'none'">{{ labelLocal
          }}
        </vs-chip>

        <vs-dropdown class="ml-auto my-2 cursor-pointer" vs-custom-content>

          <feather-icon @click.prevent icon="TagIcon" svgClasses="h-5 w-5"></feather-icon>

          <vs-dropdown-menu style="z-index: 200001">
            <vs-dropdown-item :key="index" @click="labelLocal = label.value" v-for="(label, index) in calendarLabels">
              <div :class="'bg-' + label.color" class="h-3 w-3 inline-block rounded-full mr-2"></div>
              <span>{{ label.text }}</span>
            </vs-dropdown-item>

            <vs-dropdown-item @click="labelLocal = 'none'">
              <div class="h-3 w-3 mr-1 inline-block rounded-full mr-2 bg-primary"></div>
              <span>None</span>
            </vs-dropdown-item>
          </vs-dropdown-menu>
        </vs-dropdown>

      </div>

      <vs-input class="w-full" label-placeholder="Event Title" name="event-name" v-model="title"
                v-validate="'required'"></vs-input>
      <div class="my-4">
        <small class="date-label">Start Date</small>
        <datepicker :disabledDates="disabledDatesFrom" :language="$vs.rtl ? langHe : langEn" name="start-date"
                    v-model="startDate"></datepicker>
      </div>
      <div class="my-4">
        <small class="date-label">End Date</small>
        <datepicker :disabledDates="disabledDatesTo" :language="$vs.rtl ? langHe : langEn" name="end-date"
                    v-model="endDate"></datepicker>
      </div>
      <vs-input :color="!errors.has('event-url') ? 'success' : 'danger'" class="w-full mt-6"
                label-placeholder="Event URL" name="event-url" v-model="url"
                v-validate="'url'"></vs-input>

    </vs-prompt>
  </div>
</template>

<script>
import { CalendarView, CalendarViewHeader } from 'vue-simple-calendar'
import moduleCalendar from '@/store/calendar/moduleCalendar.js'

import Datepicker from 'vuejs-datepicker'
import { en, he, sk } from 'vuejs-datepicker/src/locale'

require('vue-simple-calendar/static/css/default.css')

export default {
  components: {
    CalendarView,
    CalendarViewHeader,
    Datepicker
  },
  data () {
    return {
      showDate: new Date(),
      disabledFrom: false,
      id: 0,
      title: '',
      startDate: '',
      endDate: '',
      labelLocal: 'none',

      langHe: he,
      langEn: en,
      langSk: sk,

      url: '',
      calendarView: 'month',

      activePromptAddEvent: false,
      activePromptEditEvent: false,

      calendarViewTypes: [
        {
          label: 'Week',
          val: 'week'
        },
        {
          label: 'Month',
          val: 'month'
        },
        {
          label: 'Year',
          val: 'year'
        }
      ]
    }
  },
  computed: {
    simpleCalendarEvents () {
      console.log('calendar events', this.$store.state.calendar.events)
      const test = [
        {
          id: 1,
          title: 'My Event',
          startDate: new Date(new Date() - 1000 * 60 * 60 * 24 * 3),
          endDate: new Date(new Date() - 1000 * 60 * 60 * 24 * 2),
          url: '',
          classes: 'event-success',
          label: 'business'
        },
        {
          id: 2,
          title: 'My Event 2',
          startDate: new Date(new Date() - 1000 * 60 * 24 * 3),
          endDate: new Date(new Date() - 1000 * 60 * 60 * 24 * 2),
          url: '',
          classes: 'event-success',
          label: 'business'
        }
      ]
      return test
      // return this.$store.state.calendar.events
    },
    validForm () {
      return this.title !== '' && this.startDate !== '' && this.endDate !== '' && Date.parse(this.endDate) - Date.parse(this.startDate) >= 0 && !this.errors.has('event-url')
    },
    disabledDatesTo () {
      return { to: new Date(this.startDate) }
    },
    disabledDatesFrom () {
      return { from: new Date(this.endDate) }
    },
    calendarLabels () {
      return this.$store.state.calendar.eventLabels
    },
    labelColor () {
      return (label) => {
        if      (label === 'training') return 'success'
        else if (label === 'race')     return 'warning'
        else if (label === 'camp') return 'danger'
        else if (label === 'none')     return 'primary'
      }
    },
    windowWidth () {
      return this.$store.state.windowWidth
    }
  },
  methods: {
    addEvent () {
      const obj = {
        title: this.title,
        startDate: this.startDate,
        endDate: this.endDate,
        label: this.labelLocal,
        url: this.url
      }
      obj.classes = `event-${this.labelColor(this.labelLocal)}`
      this.$store.dispatch('calendar/addEvent', obj)
    },
    updateMonth (val) {
      this.showDate = this.$refs.calendar.getIncrementedPeriod(val)
    },
    clearFields () {
      this.title = this.endDate = this.url = ''
      this.id = 0
      this.labelLocal = 'none'
    },
    promptAddNewEvent (date) {
      this.disabledFrom = false
      this.addNewEventDialog(date)
    },
    addNewEventDialog (date) {
      this.clearFields()
      this.startDate = date
      this.endDate = date
      this.activePromptAddEvent = true
    },
    openAddNewEvent (date) {
      this.disabledFrom = true
      this.addNewEventDialog(date)
    },
    openEditEvent (event) {
      const e = this.$store.getters['calendar/getEvent'](event.id)
      this.id = e.id
      this.title = e.title
      this.startDate = e.startDate
      this.endDate = e.endDate
      this.url = e.url
      this.labelLocal = e.label
      this.activePromptEditEvent = true
    },
    editEvent () {
      const obj = {
        id: this.id,
        title: this.title,
        startDate: this.startDate,
        endDate: this.endDate,
        label: this.labelLocal,
        url: this.url
      }
      obj.classes = `event-${this.labelColor(this.labelLocal)}`
      this.$store.dispatch('calendar/editEvent', obj)
    },
    removeEvent () {
      this.$store.dispatch('calendar/removeEvent', this.id)
    },
    eventDragged (event, date) {
      this.$store.dispatch('calendar/eventDragged', {
        event,
        date
      })
    }
  },
  created () {
    this.$store.registerModule('calendar', moduleCalendar)
    this.$store.dispatch('calendar/fetchEvents')
    // this.$store.dispatch('calendar/fetchEventLabels')
  },
  beforeDestroy () {
    this.$store.unregisterModule('calendar')
  }
}
</script>

<style lang="scss">
  @import "@/assets/scss/vuexy/apps/simple-calendar.scss";
</style>
