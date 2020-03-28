<template>
  <div id="event-calendar-app">
    <vx-card class="mt-5">
      <div class="calendar-view">
        <FullCalendar
          :events="calendarEvents"
          :header="{
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridDay,timeGridWeek,dayGridMonth,listWeek'}"
          :locale="locale"
          :now-indicator="true"
          :plugins="calendarPlugins"
          :select-mirror="true"
          :selectable="true"
          :slot-label-format="{
            hour: '2-digit',
            minute: '2-digit',
            omitZeroMinute: false,
            meridiem: 'short'
          }"
          :title-format="{
          month: 'long',
          year: 'numeric',
          day: 'numeric',
          weekday: 'long'
          }"
          :weekends="true"
          @eventClick="handleEventClick"
          @eventMouseEnter="handleEventMouseEnter"
          @select="handleSelectClick"
          class="event-calendar"
          default-view="timeGridWeek"
          editable="true"
          max-time="21:00:00"
          min-time="06:00:00"
          ref="fullCalendar"
        />
      </div>
    </vx-card>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import listPlugin from '@fullcalendar/list'
import skLocale from '@fullcalendar/core/locales/sk'

import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

export default {
  components: {
    FullCalendar,
    flatPickr
  },
  data () {
    return {
      activePromptAddEvent: false,
      activePromptEditEvent: false,

      calendarPlugins: [ // plugins must be defined in the JS
        dayGridPlugin,
        timeGridPlugin,
        interactionPlugin,
        listPlugin// needed for dateClick
      ],
      locale: skLocale,

      fromDate: null,
      toDate: null,
      configFromdateTimePicker: {
        minDate: new Date(),
        maxDate: null,
        enableTime: true
      },
      configTodateTimePicker: {
        enableTime: true,
        minDate: null
      },
      showDate: new Date(),
      disabledFrom: false,
      id: 0,
      url: '',
      title: '',
      startDate: '',
      endDate: '',
      labelLocal: 'none'
    }
  },
  computed: {
    calendarEvents () {
      return this.$store.state.calendar.events
    },
    validForm () {
      // FIXME
      return true
    }
  },
  methods: {
    handleDateClick (arg) {
      console.log('handling date click', arg)
    },
    handleEventClick (arg) {
      console.log('handling event click', arg)
      console.log('id of event', arg.event.id)
    },
    handleSelectClick (arg) {
      console.log('handling select click', arg)
      this.addNewEventDialog(arg)
    },
    handleEventMouseEnter (arg) {
      console.log('handling mouse event enter', arg)
    },
    onFromChange (selectedDates, dateStr, instance) {
      this.$set(this.configTodateTimePicker, 'minDate', dateStr)
    },
    onToChange (selectedDates, dateStr, instance) {
      this.$set(this.configFromdateTimePicker, 'maxDate', dateStr)
    },
    addEvent () {
      const obj = {
        title: this.title,
        startDate: this.startDate,
        endDate: this.endDate,
        label: this.labelLocal,
        url: this.url
      }
      // obj.classes = `event-${this.labelColor(this.labelLocal)}`
      // this.$store.dispatch('calendar/addEvent', {})
    },
    clearFields () {
      console.warn('need to clean fields')
    },
    promptAddNewEvent (date) {
      this.disabledFrom = false
      this.addNewEventDialog(date)
    },
    addNewEventDialog (arg) {
      console.log('addNewEventDialog', arg)
      // this.clearFields()
      // this.startDate = arg.startStr
      // this.endDate =  arg.end
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
    }
  },
  created () {
    this.$store.dispatch('calendar/fetchEvents')
  }
}

</script>

<style lang='scss'>

  // you must include each plugins' css
  // paths prefixed with ~ signify node_modules
  @import '~@fullcalendar/core/main.css';
  @import '~@fullcalendar/daygrid/main.css';
  @import '~@fullcalendar/timegrid/main.css';

  #event-calendar-app {
    font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
    font-size: 14px;
  }

  .calendar-view {
    margin: 0 auto;
  }

  .fc-unthemed td.fc-today {
    background: #0C112E;
  }

  /*.fc-day-grid-container {*/
  /*  !* FIXME TODO *!*/
  /*  !*height: calc(var(--vh, 1vh) * 50 - 11.5rem);*!*/
  /*  max-height: 65vh;*/
  /*}*/

  /*.fc-time-grid-container {*/
  /*  !* FIXME TODO *!*/
  /*  !*height: calc(var(--vh, 1vh) * 50 - 11.5rem);*!*/
  /*  max-height: 60vh;*/
  /*}*/

  .fc-list-heading td {
    background: #00b0d3;
    color: white;
  }
</style>
