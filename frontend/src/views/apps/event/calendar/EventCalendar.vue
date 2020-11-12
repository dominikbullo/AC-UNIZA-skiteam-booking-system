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
            :now-indicator="true"
            :plugins="calendarPlugins"
            :select-mirror="true"
            :selectable="calendarConfig.selectable"
            :slot-label-format="calendarConfig.slot_label_format"
            :title-format="calendarConfig.title_format"
            :weekends="true"
            :scrollTime="calendarConfig.scrollTime"
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

      <add-event :isSidebarActive="addEvent.active"
                 @closePrompt="toggleAddEventPrompt"
                 :data="addEvent.data"/>

      <!--      <view-event :isSidebarActive="addNewDataSidebar"-->
      <!--                  @closeSidebar="toggleDataSidebar"-->
      <!--                  :data="sidebarData"-->
      <!--                  :event_data="sidebarData"/>-->
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
// import ViewEvent from './event-view/ViewEvent'

export default {
  components: {
    FullCalendar,
    AddEvent
    // ViewEvent
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
      // TODO scroll to first event or current time
      return '07:00:00'
    },
    calendarEvents () {
      return this.$store.getters['calendar/getEventsForCal']
    }
  },
  methods: {
    eventRender (item) {
      // Adding class to old events for css
      if (item.event.start < new Date().getTime()) {
        item.el.classList.add('past-event')
      }
    },
    toggleAddEventPrompt (val = false) {
      this.addEvent.active = val
    },

    handleEventClick (arg) {
      console.log('event click', arg)
      if (this.$acl.not.check('isCoach') && new Date(arg.event.start).valueOf() < new Date().valueOf()) {
        this.$vs.notify({
          color: 'danger',
          title: 'Old event',
          text: 'You cannot change an event which has already happened'
        })
        return false
      }

      // this.$store.dispatch('calendar/fetchEvent', arg.event.id)
      //   .then(res => {
      //     this.editedEvent = res.data
      //
      //     const childrenUsersID = []
      //     Object.values(this.$store.getters['family/familyChildren']).forEach(obj => {
      //       childrenUsersID.push(obj.user.profile.id)
      //     })
      //     console.log('childrenUsersID', childrenUsersID)
      //
      //     const eventChildren = []
      //     Object.values(this.editedEvent['participants']).forEach(obj => {
      //       eventChildren.push(obj.id)
      //     })
      //     console.log('eventChildren', eventChildren)
      //
      //     const userChildrenOnEvent = childrenUsersID.filter(x => eventChildren.includes(x))
      //     console.log('userChildrenOnEvent', userChildrenOnEvent)
      //
      //     this.childAddToEventPrompt.onEvent = userChildrenOnEvent
      //     this.childAddToEventPrompt.selected = userChildrenOnEvent
      //
      //     this.childAddToEventPrompt.active = true
      //   })
    },
    handleSelect (arg) {
      this.addEvent.data = {
        start: arg.start,
        end: arg.end
      }
      this.toggleAddEventPrompt(true)
    },
    handleEventChange (arg) {
      console.log('handlerEventChange', arg)
      // console.log('handling change in event', arg.event.id, arg)
      // console.log('handling change in start', arg.event.start)
      // console.log('handling change in end', arg.event.end)
      //
      // const event = {
      //   id: arg.event.id,
      //   start: arg.event.start,
      //   end: arg.event.end
      // }

      // this.$store.dispatch('calendar/editEvent', { ...event, ...this.getExtraInfo() })
      //   .then(() => {
      //     this.$vs.notify({
      //       color: 'success',
      //       title: 'Event Updated',
      //       text: 'The selected event was successfully updated'
      //     })
      //   })
      //   .catch(err => {
      //     this.$vs.notify({
      //       color: 'danger',
      //       title: 'Event Not Changed',
      //       text: err.message
      //     })
      //     console.error(err)
      //   })
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

.fc-today {
  background-color: #0C112E !important;
}

.fc-slats td {
  height: 1.15em !important; // Change This to your required height
  font-size: .9em;
  border-bottom: 0;
}

</style>