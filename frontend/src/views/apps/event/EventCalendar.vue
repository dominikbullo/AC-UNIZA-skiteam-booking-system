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


        <div v-if="editedEvent" id="event-info-table">
          <div class="vx-row">
            <div class="vx-col flex-1" id="event-info-col-1">
              <table>
                <tr>
                  <td class="font-semibold">Type</td>
                  <td>{{ editedEvent.title }}</td>
                </tr>
                <tr>
                  <td class="font-semibold">Skis</td>
                  <td>{{ editedEvent.additional_info }}</td>
                </tr>
                <tr>
                  <td class="font-semibold">Skis</td>
                  <td>{{ editedEvent.skis_type }}</td>
                </tr>
              </table>
            </div>
            <div class="vx-col flex-1" id="event-info-col-2">
              <table>
                <tr>
                  <td class="font-semibold">Location</td>
                  <td>{{ editedEvent.location }}</td>
                </tr>
                <tr>
                  <td class="font-semibold">Start</td>
                  <td>{{ editedEvent.start | time }}</td>
                </tr>

              </table>
            </div>
          </div>

          <div v-if="$acl.check('isCoach')">
            <vs-divider>Coach zone</vs-divider>
            <div class="vx-col w-full flex flex-wrap items-center justify-center">
              <vs-button icon-pack="feather" icon="icon-edit" color="warning" class="mr-4"
                         :to="{name: 'app-event-edit', params: { eventId: this.editedEvent.id }}">Edit
              </vs-button>
              <vs-button type="border" color="danger" icon-pack="feather" icon="icon-trash"
                         @click="confirmDeleteRecord">Delete
              </vs-button>
            </div>
          </div>

          <ul class="centerx">
            <vs-divider>Your children</vs-divider>
            <li class="mb-2" :key="child.username" v-for="child in userChildren">
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

      editedEvent: null,

      childAddToEventPrompt: {
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
      // const members = this.$store.state.family.members
      const members = this.$store.getters['family/familyChildren']

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
      if (this.$acl.not.check('isCoach') && new Date(arg.event.start).valueOf() < new Date().valueOf()) {
        this.$vs.notify({
          color: 'danger',
          title: 'Old event',
          text: 'You cannot change an event which has already happened'
        })
        return false
      }

      this.editedEvent = Object.values(this.calendarEvents).find(obj => {
        return obj.id === parseInt(arg.event.id)
      })

      // IDEA: Check with userChildren() array
      console.log('participants', this.editedEvent['participants'])
      const myChildrenOnEvent = this.editedEvent['participants'].filter(obj => {
        console.log('obj', obj)
        return obj.family_id === this.$store.state.AppActiveUser.profile.family_id
      })
      // console.log('myChildOnEvent', myChildOnEvent)

      // TODO not parents just children
      const userNames = []
      myChildrenOnEvent.forEach((element) => {
        userNames.unshift(element['username'])
      })

      this.childAddToEventPrompt.onEvent = userNames
      this.childAddToEventPrompt.selected = userNames

      this.childAddToEventPrompt.active = true
    },
    handleSelectClick (click) {
      console.log('handling select click', click)
      if (click.start.isBefore(this.moment())) {
        this.$vs.notify({
          color: 'danger',
          title: 'Old event',
          text: 'Cannot change event that already happend'
        })
        return false
      }
      alert(`clicked ${click.startStr} - ${click.endStr}`)
    },
    handleEventMouseEnter (arg) {
      // console.log('handling mouse event enter', arg)
    },
    confirmDeleteRecord () {
      this.childAddToEventPrompt.active = false
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: 'Confirm Delete',
        text: `You are about to delete "${this.editedEvent.title}"`,
        accept: this.deleteRecord,
        acceptText: 'Delete'
      })
    },
    deleteRecord () {
      /* Below two lines are just for demo purpose */
      this.showDeleteSuccess()

      /* UnComment below lines for enabling true flow if deleting user */
      // this.$store.dispatch("userManagement/removeRecord", this.params.data.id)
      //   .then(()   => { this.showDeleteSuccess() })
      //   .catch(err => { console.error(err)       })
    },
    showDeleteSuccess () {
      this.$vs.notify({
        color: 'success',
        title: 'User Deleted',
        text: 'The selected user was successfully deleted'
      })
    },
    clearFields () {
      console.warn('need to clean fields')
    },
    changeUserChildrenOnEvent () {
      const payload = {
        'eventID': this.editedEvent.id,
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

  #event-info-table {
    table {
      td {
        padding-right: .5rem;
        padding-bottom: .8rem;
        word-break: break-all;
      }

      &:not(.permissions-table) {
        td {
          @media screen and (max-width: 370px) {
            display: block;
          }
        }
      }
    }
  }

  @media screen and (min-width: 1201px) and (max-width: 1211px),
  only screen and (min-width: 636px) and (max-width: 991px) {
    #event-info-col-1 {
      width: calc(100% - 5rem) !important;
    }
  }


</style>
