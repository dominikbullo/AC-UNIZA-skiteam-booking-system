<template>
  <div id="test_calendar">
    <vx-card class="mt-20">
      <div class="demo-app">
        <FullCalendar
          :events="calendarEvents"
          :header="{
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridDay,timeGridWeek,dayGridMonth,listWeek'
          }"
          :locale="locale"
          :now-indicator="true"
          :plugins="calendarPlugins"
          :weekends="calendarWeekends"
          @dateClick="handleDateClick"
          class='demo-app-calendar'
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

export default {
  components: {
    FullCalendar // make the <FullCalendar> tag available
  },
  data () {
    return {
      calendarPlugins: [ // plugins must be defined in the JS
        dayGridPlugin,
        timeGridPlugin,
        interactionPlugin,
        listPlugin// needed for dateClick
      ],
      calendarWeekends: true,
      locale: skLocale
    }
  },
  computed: {
    calendarEvents () {
      return this.$store.state.calendar.events
    }
  },
  methods: {
    handleDateClick (arg) {
      if (confirm('Would you like to add an event to ' + arg.dateStr + ' ?')) {
        this.calendarEvents.push({ // add new event data
          title: 'New Event',
          start: arg.date,
          allDay: arg.allDay
        })
      }
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

  .demo-app {
    font-family: Arial, Helvetica Neue, Helvetica, sans-serif;
    font-size: 14px;
  }

  .demo-app-top {
    margin: 0 0 3em;
  }

  .demo-app-calendar {
    margin: 0 auto;
    max-width: 900px;
  }

  .fc-unthemed td.fc-today {
    background: #0C112E;
  }

  .fc-list-heading td {
    background: #00b0d3;
    color: white;
  }
</style>
