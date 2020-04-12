<template>
  <div id="event-calendar-app">
    <vx-card class="mt-5 vx-card no-scroll-content">
      <div class="calendar-view  no-scroll-content">
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
          :selectable="calendarConfig.selectable"
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
          :editable="calendarConfig.editable"
          height="parent"
          ref="fullCalendar"
        />
      </div>

      <!-- Add child to EVENT -->
      <vs-prompt
        :active.sync="childAddToEventPrompt.active"
        :is-valid="validForm"
        @accept="changeUserChildrenOnEvent"
        accept-text="Save"
        class="calendar-child-add-event-dialog"
        title="Sign up child to event">


        <div class="my-4">
          <ul class="centerx">
            <li :key="child.username" v-for="child in userChildren">
              <vs-checkbox
                :vs-value="child.username"
                color="success"
                v-model="childAddToEventPrompt.selected">
                {{ child.first_name}} {{ child.last_name}}
              </vs-checkbox>
            </li>
          </ul>
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
      calendarPlugins: [ // plugins must be defined in the JS
        dayGridPlugin,
        timeGridPlugin,
        interactionPlugin,
        listPlugin// needed for dateClick
      ],
      locale: skLocale,

      calendarConfig: {
        selectable: false,
        editable: false
      },

      childAddToEventPrompt: {
        editedEventID: -1,
        active: false,
        onEvent: [],
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
      return cleanMembers
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
      this.childAddToEventPrompt.editedEventID = parseInt(arg.event.id)

      const event = Object.values(this.calendarEvents).find(obj => {
        return obj.id === this.childAddToEventPrompt.editedEventID
      })
      // console.log('event', event)

      // IDEA: Check with userChildren() array
      const myChildOnEvent = event['participants'].filter(obj => {
        return obj.family_id === this.$store.state.AppActiveUser.profile.family_id
      })
      // console.log('myChildOnEvent', myChildOnEvent)

      const userNames = []
      myChildOnEvent.forEach((element) => {
        userNames.unshift(element['username'])
      })
      // console.log('usernames', userNames)

      this.childAddToEventPrompt.onEvent = userNames
      this.childAddToEventPrompt.selected = userNames

      this.childAddToEventPrompt.active = true
    },
    handleSelectClick (click) {
      console.log('handling select click', click)
      alert(`clicked ${click.startStr} - ${click.endStr}`)
    },
    handleEventMouseEnter (arg) {
      // console.log('handling mouse event enter', arg)
    },
    onFromChange (selectedDates, dateStr, instance) {
      this.$set(this.configTodateTimePicker, 'minDate', dateStr)
    },
    onToChange (selectedDates, dateStr, instance) {
      this.$set(this.configFromdateTimePicker, 'maxDate', dateStr)
    },
    clearFields () {
      console.warn('need to clean fields')
    },
    changeUserChildrenOnEvent () {
      const payload = {
        'eventID': this.childAddToEventPrompt.editedEventID,
        'selected': this.childAddToEventPrompt.selected,
        'onEvent': this.childAddToEventPrompt.onEvent
      }

      this.$store.dispatch('calendar/changeEventMembers', payload)
    }
  },
  created () {
    this.$store.dispatch('calendar/fetchEvents')
    this.$store.dispatch('family/fetchFamily', this.$store.state.AppActiveUser.profile.family_id)
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
    max-height: calc(var(--vh, 1vh) * 100 - 16.2rem);
  }

  .fc-unthemed td.fc-today {
    background: #0C112E;
  }


  .fc-list-heading td {
    background: #00b0d3;
    color: white;
  }
</style>
