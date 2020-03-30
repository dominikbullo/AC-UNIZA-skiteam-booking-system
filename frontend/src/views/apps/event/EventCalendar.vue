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

      <!-- Add child to EVENT -->
      <vs-prompt
        :active.sync="childAddToEventPrompt.active"
        :is-valid="validForm"
        @accept="addEvent"
        accept-text="Save"
        class="calendar-child-add-event-dialog"
        title="Sign up child to event">


        <div class="my-4">
          <ul class="centerx">
            <li v-for="child in userChildren" :key="child.username">
              <vs-checkbox color="success" v-model="childAddToEventPrompt.selected" :vs-value="child.username">{{
                child.first_name}} {{ child.last_name}}
              </vs-checkbox>
            </li>
          </ul>

          <p>{{childAddToEventPrompt.selected}}</p>
        </div>

      </vs-prompt>

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
import vSelect from 'vue-select'


import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

export default {
  components: {
    FullCalendar,
    flatPickr,
    'v-select': vSelect
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


      childAddToEventPrompt: {
        active: false,
        selected: []
      },

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
    userChildren () {
      const members = this.$store.state.family.members

      const cleanMembers = []
      members.forEach((element) => {
        cleanMembers.unshift(element['user'])
      })
      console.log('cleanMembers', cleanMembers)
      return cleanMembers
    },
    validForm () {
      // FIXME
      return true
    }
  },
  methods: {
    fetchFamily (size) {
      const payload = {
        familyId: this.$store.state.AppActiveUser.profile.family_id,
        count: size
      }
      this.$store.dispatch('family/fetchFamily', payload)
    },
    handleDateClick (arg) {
      console.log('handling date click', arg)
    },
    handleEventClick (arg) {
      console.log('handling event click', arg)
      console.log('handling event click id', arg.event.id)

      const event = Object.values(this.calendarEvents).find(obj => {
        return obj.id === parseInt(arg.event.id)
      })
      console.log('event', event)

      console.log('event participants', event['participants'])
      console.log('my family id', this.$store.state.AppActiveUser.profile.family_id)

      const myChildOnEvent = event['participants'].filter(obj => {
        return obj.family_id === this.$store.state.AppActiveUser.profile.family_id
      })
      console.log('myChildOnEvent', myChildOnEvent)

      const userNames = []
      myChildOnEvent.forEach((element) => {
        userNames.unshift(element['username'])
      })
      console.log('usernames', userNames)

      this.childAddToEventPrompt.selected = userNames
      this.childAddToEventPrompt.active = true
    },
    handleSelectClick (info) {
      console.log('handling select click', info)
      alert(`clicked ${info.dateStr}`)
      this.activePromptChildToEvent = true
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
  }
  ,
  created () {
    this.$store.dispatch('calendar/fetchEvents')
    // FIXME
    this.fetchFamily(10)
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
