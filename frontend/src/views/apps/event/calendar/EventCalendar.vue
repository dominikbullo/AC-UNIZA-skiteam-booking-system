<template>
  <div id="event-calendar-app">
    <vx-card class="mt-5 vx-card">
      <div class="calendar-view no-scroll-content">
        <FullCalendar
            :events="calendarEvents"
            :slotDuration="calendarConfig.slotDuration"
            :header="calendarConfig.header"
            :custom-buttons="calendarConfig.customButtons"
            :locale="calendarConfig.locale"
            :plugins="calendarPlugins"
            :selectable="calendarConfig.selectable"
            :slot-label-format="calendarConfig.slot_label_format"
            :title-format="calendarConfig.title_format"
            :scrollTime="calendarConfig.scrollTime"
            :now-indicator="true"
            :select-mirror="true"
            :weekends="true"
            @eventRender="eventRender"
            @eventClick="handleEventClick"
            @select="handleSelect"
            @eventDrop="handleEventChange"
            @eventResize="handleEventChange"
            :views="calendarConfig.views"
            :default-view="calendarConfig.views.defaultView"
            :editable="calendarConfig.editable"
            min-time="06:00:00"
            max-time="21:00:00"
            :scroll-time="minEventTime"
            height="parent"
            class="custom-class"
        />
      </div>

      <add-event :isPopupActive="addEvent.active"
                 @closePrompt="toggleAddEventPrompt"
                 :data="addEvent.data"/>

      <view-event :isPromptActive="viewEvent.active"
                  @closePrompt="toggleViewEventPrompt"
                  :data="viewEvent.data"/>

    </vx-card>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue'

import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import rrulePlugin from '@fullcalendar/rrule'
import listPlugin from '@fullcalendar/list'

import skLocale from '@fullcalendar/core/locales/sk'
import enLocale from '@fullcalendar/core/locales/en-gb'

import AddEvent from './event-add/AddEvent'
import ViewEvent from './event-view/ViewEvent'

export default {
  components: {
    FullCalendar,
    AddEvent,
    ViewEvent
  },
  data () {
    return {
      addEvent: {
        active: false,
        data: {}
      },

      viewEvent: {
        active: false,
        data: {}
      },

      calendarPlugins: [ // plugins must be defined in the JS
        dayGridPlugin,
        timeGridPlugin,
        interactionPlugin,
        listPlugin,     // needed for dateClick
        rrulePlugin
      ],

      calendarConfig: {
        scrollTime: `${this.moment().format('HH')}:00:00`,
        locale: this.$i18n.locale === 'sk' ? skLocale : enLocale,
        selectable: this.$acl.check('isCoach'),
        editable: this.$acl.check('isCoach'),
        header: {
          // left: 'prev,next today addEvent',
          left: 'timeGridThreeDay,myCustomWeek,timeGridWeek,dayGridMonth,mylistWeek', // this will place the button on the right hand side
          center: 'title',
          right: 'today prev,next'
        },
        views: {
          mylistWeek: {
            visibleRange (currentDate) {
              // Generate a new date for manipulating in the next step
              const startDate = new Date(currentDate.valueOf())
              const endDate = new Date(currentDate.valueOf())

              // Adjust the start & end dates, respectively
              startDate.setDate(startDate.getDate())
              endDate.setDate(endDate.getDate() + 13)

              return {
                start: startDate,
                end: endDate
              }
            },
            type: 'listWeek',
            duration: { days: 14 },
            buttonText: 'list'
          },
          myCustomWeek: {
            visibleRange (currentDate) {
              // Generate a new date for manipulating in the next step
              const startDate = new Date(currentDate.valueOf())
              const endDate = new Date(currentDate.valueOf())

              // Adjust the start & end dates, respectively
              startDate.setDate(startDate.getDate()) // One day in the past
              endDate.setDate(endDate.getDate() + 6) // Two days into the future

              return {
                start: startDate,
                end: endDate
              }
            },
            type: 'timeGrid',
            duration: { days: 7 },
            buttonText: 'my week'
          },
          timeGridThreeDay: {
            type: 'timeGrid',
            duration: { days: 3 },
            buttonText: `3 ${this.$t('day')}`
          },
          defaultView: screen.width <= 670 ? 'timeGridThreeDay' : 'myCustomWeek'
        },
        customButtons: {
          addEvent: {
            text: 'Add Event',
            click () {
              console.log('test', this.addEventPrompt)
            }
          }
        },
        slot_label_format: {
          hour: '2-digit',
          minute: '2-digit',
          omitZeroMinute: false,
          meridiem: 'short'
        },
        title_format: {
          month: 'long',
          year: 'numeric',
          day: 'numeric',
          weekday: 'long'
        }
      }
    }
  },
  computed: {
    minEventTime () {
      return '07:00:00'
    },
    calendarEvents () {
      // const testEvents = [
      //   {
      //     title: 'testEvent_1_JUST_DISPLAY',
      //     start: '2020-11-20T12:30:00',
      //     end: '2020-11-24T18:30:00',
      //     allDay: true // will make the time show
      //   }
      // ]
      // return this.$store.getters['calendar/getEventsForCal'].concat(testEvents)
      return this.$store.getters['calendar/getEventsForCal']
    }
  },
  methods: {
    eventRender (item) {
      // Adding class to old events for css
      if (item.event.start < new Date().getTime()) {
        item.el.classList.add('past-event')
      }
      const canceled = this.calendarEvents.filter(x => x.canceled === true).map(x => x.id)
      if (canceled.includes(parseInt(item.event.id))) {
        item.el.classList.add('canceled-event')
      }
    },
    toggleAddEventPrompt (val = false) {
      this.addEvent.active = val
    },
    toggleViewEventPrompt (val = false) {
      this.viewEvent.active = val
    },
    handleEventClick (arg) {
      // console.log('event click', arg)
      // TODO: Read only for 30days + warning
      if (this.$acl.not.check('isCoach') && new Date(arg.event.start).valueOf() < new Date().valueOf()) {
        this.$vs.notify({
          color: 'danger',
          title: 'Old event',
          text: 'You cannot change an event which has already happened'
        })
        return false
      }
      this.$store.dispatch('calendar/fetchEvent', arg.event.id)
        .then((res) => {
          this.viewEvent.data = res.data
          this.toggleViewEventPrompt(true)
        })
    },
    handleSelect (arg) {
      this.addEvent.data = {
        start: arg.start,
        end: arg.end,
        allDay: arg.allDay
      }
      this.toggleAddEventPrompt(true)
    },
    handleAllDay (arg) {
      if (arg.hasOwnProperty('oldEvent') && arg.oldEvent.allDay === true && arg.event.allDay === false) {
        // TODO: add time by default event type average type
        return this.moment(arg.event.start).add(1, 'h').toDate()
      }
      return arg.event.end
    },
    handleEventChange (arg) {
      const event = {
        id: arg.event.id,
        start: arg.event.start,
        all_day: arg.event.allDay,
        end: this.handleAllDay(arg),
        // TODO: auto resourcetype in axios
        resourcetype: 'Event'
      }

      this.$store.dispatch('calendar/editEvent', event)
        .then(() => {
          this.$vs.notify({
            color: 'success',
            title: 'Event Updated',
            text: 'The selected event was successfully updated'
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
    fetchConfigData () {
      if (!this.$acl.check('isCoach')) return
      console.log('Hello coach')
      this.$store.dispatch('calendar/fetchEventTypes')
      this.$store.dispatch('calendar/fetchCategories')
      this.$store.dispatch('calendar/fetchLocations')
      this.$store.dispatch('calendar/fetchSkisTypes')
      this.$store.dispatch('calendar/fetchRaceOrganizers')
    }
  },
  created () {
    this.$store.dispatch('calendar/fetchEvents')
    this.fetchConfigData()
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
  max-height: calc(var(--vh, 1vh) * 100 - 15rem);
}

.fc-list-heading {
  td {
    background-color: black !important;;
    color: white;

    :hover {
      background-color: #3c3c3c !important;;
    }
  }
}

.fc-left .fc-button-group {
  display: block;
}

// RES: https://stackoverflow.com/questions/12632229/change-color-of-past-events-in-fullcalendar
.fc-past {
  background-color: #262b4573;
}

.past-event.fc-event, .past-event .fc-event-dot {
  //opacity: 0.8 !important;
  filter: grayscale(60%);
  // RES: https://css-tricks.com/stripes-css/
  background: repeating-linear-gradient(
          -45deg,
          transparent,
          transparent 5px,
          transparentize(#1f1f1f, .5) 8px,
          transparentize(#1f1f1f, .5) 10px
  ),
}

.canceled-event.fc-event, .canceled-event .fc-event-dot {
  filter: grayscale(40%);
  background-color: red !important;
  background: linear-gradient(to top left,
      rgba(0, 0, 0, 0) 0%,
      rgba(0, 0, 0, 0) calc(50% - 5px),
      rgb(0, 0, 0) 50%,
      rgba(0, 0, 0, 0) calc(50% + 5px),
      rgba(0, 0, 0, 0) 100%),
  linear-gradient(to top right,
          rgba(0, 0, 0, 0) 0%,
          rgba(0, 0, 0, 0) calc(50% - 5px),
          rgb(0, 0, 0) 50%,
          rgba(0, 0, 0, 0) calc(50% + 5px),
          rgba(0, 0, 0, 0) 100%);
}

.fc-today {
  background-color: #0C112E !important;
}

.fc-slats td {
  height: 1.15em !important; // Change This to your required height
  font-size: .9em;
  border-bottom: 0;
}

.fc-center {
  font-size: 12px;
}

</style>
