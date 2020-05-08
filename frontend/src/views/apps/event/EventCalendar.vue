<template>
  <div id="event-calendar-app">
    <vx-card class="mt-5 vx-card no-scroll-content">
      <div class="calendar-view  no-scroll-content">
        <FullCalendar
          :events="calendarEvents"
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
          @eventClick="handleEventClick"
          @eventMouseEnter="handleEventMouseEnter"
          @select="handleSelect"
          :views="calendarConfig.views"
          :default-view="calendarConfig.views.defaultView"
          :editable="calendarConfig.editable"
          height="parent"
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
                  <td class="font-bold">Type</td>
                  <td>{{ editedEvent.title }}</td>
                </tr>
                <tr>
                  <td class="font-bold">Location</td>
                  <td>{{ editedEvent.location }}</td>
                </tr>
                <tr>
                  <td class="font-bold">Category</td>
                  <td>{{ editedEvent.category}}</td>
                </tr>
              </table>
            </div>
          </div>
          <vs-divider></vs-divider>
          <div class="vx-row">
            <div class="vx-col flex-1" id="event-info-col-2">
              <table>
                <tr>
                  <td class="font-bold">Start</td>
                  <td>{{ editedEvent.start | time }}</td>
                </tr>
                <tr>
                  <td class="font-bold">Skis</td>
                  <td>{{ editedEvent.skis_type }}</td>
                </tr>
              </table>
            </div>
            <div class="vx-col flex-1" id="event-info-col-3">
              <table>
                <tr>
                  <td class="font-bold">End</td>
                  <td>{{ editedEvent.end | time }}</td>
                </tr>
                <tr>
                  <td class="font-bold">Skis</td>
                  <td>{{ editedEvent.skis_type }}</td>
                </tr>
              </table>
            </div>
          </div>
          <!-- TODO: if exist -->
          <div class="vx-row">
            <div class="vx-col">
              <p class="font-bold mr-5">Additional information:</p>
              <p>{{ editedEvent.additional_info }}</p>
            </div>
          </div>
          <div v-if="$acl.check('isCoach')">
            <vs-divider>Coach zone</vs-divider>
            <div class="vx-col w-full flex flex-wrap items-center justify-center">

              <vs-button icon-pack="feather" icon="icon-edit" class="mr-4"
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


      <!-- ADD EVENT -->
      <vs-prompt
        :active.sync="addEventPrompt.active"
        :is-valid="true"
        @accept="newEvent"
        accept-text="Save"
        class="calendar-add-event-dialog"
        title="Add event">

        <!--        <p>Choices</p>-->
        <!--        <p>{{eventChoices}}</p>-->

        <!--        <p>Categories</p>-->
        <!--        <p>{{this.$store.state.calendar.eventConfig.categories}}</p>-->

        <!--        <p>DATA</p>-->
        <!--        <p>{{addEvent}}</p>-->


        <vs-input name="event-name" v-validate="'required'" class="w-full" label-placeholder="Event Title"
                  v-model="newEvent.title"></vs-input>

        <div class="mt-4">
          <label class="text-sm">Categories</label>
          <!-- RES: https://vue-select.org/ -->
          <v-select multiple
                    :closeOnSelect="false"
                    label="displayName"
                    v-model="addEventPrompt.selected"
                    :options="addEventPrompt.options"/>
        </div>

        <div class="mt-4">
          <label class="text-sm">Start</label>
          <flat-pickr v-model="newEvent.startDate"
                      :config="datePickerConfig"
                      class="w-full"
                      v-validate="'required'"
                      name="start"/>
          <span class="text-danger text-sm" v-show="errors.has('start')">{{ errors.first('start') }}</span>
        </div>

        <div class="mt-4">
          <label class="text-sm">End</label>
          <flat-pickr v-model="newEvent.endDate"
                      :config="datePickerConfig"
                      class="w-full"
                      v-validate="'required'"
                      name="end"/>
          <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
        </div>
        <!--        <div class="my-4">-->
        <!--          <small class="date-label">Start Date</small>-->
        <!--          <datepicker name="start-date" v-model="addEvent.startDate" :disabled="addEvent.disabledFrom"></datepicker>-->
        <!--        </div>-->
        <!--        <div class="my-4">-->
        <!--          <small class="date-label">End Date</small>-->
        <!--          <datepicker :disabledDates="addEvent.disabledDatesTo" name="end-date" v-model="addEvent.endDate"></datepicker>-->
        <!--        </div>-->
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

      calendarConfig: {
        locale: skLocale,
        selectable: this.$acl.check('isCoach'),
        editable: this.$acl.check('isCoach'),
        header: {
          // left: 'prev,next today addEvent',
          left: 'prev,next today',
          center: 'title',
          right: 'timeGridThreeDay,timeGridWeek,dayGridMonth,listWeek' // this will place the button on the right hand side
        },
        views: {
          timeGridThreeDay: {
            type: 'timeGrid',
            duration: { days: 3 },
            buttonText: '3 dni'
          },
          defaultView: 'timeGridWeek'
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
      },

      datePickerConfig: {
        enableTime: true,
        altInput: true,
        altFormat: 'd.m.Y H:i'
      },

      editedEvent: null,

      childAddToEventPrompt: {
        active: false,
        onEvent: [],
        selected: []
      },

      addEventPrompt: {
        active: false,
        onEvent: [],
        selected: [],
        options: []
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

      newEvent: {
        showDate: new Date(),
        disabledFrom: false,
        disabledDatesTo: false,
        title: '',
        startDate: '',
        endDate: ''
      }
    }
  },
  computed: {
    calendarEvents () {
      return this.$store.state.calendar.events
    },
    eventChoices () {
      return this.$store.state.calendar.eventConfig.choices
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
    addEvent () {
      console.log('adding event')
      // const event = {
      //   type: 'ATHLETIC_TRAINING',
      //   start: arg.start,
      //   end: arg.end,
      //   allDay: arg.allDay,
      //   season: 1,
      //   location: 1,
      //   category: [1, 2, 3],
      //   resourcetype: 'event'
      // }
      // this.$store.dispatch('calendar/addEvent', event)
    },
    handleDateClick (arg) {
      console.log('handling date click', arg)
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
      this.editedEvent = Object.values(this.calendarEvents).find(obj => {
        return obj.id === parseInt(arg.event.id)
      })

      const categories = []
      Object.values(this.editedEvent.category).forEach((element) => {
        categories.unshift(element['displayName'])
      })
      this.editedEvent.category = categories


      // IDEA: Check with userChildren() array
      // console.log('participants', this.editedEvent['participants'])
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
    handleSelect (arg) {
      console.log('handling select click', arg)
      this.addEventPrompt.active = true
      console.log('handling select click123', arg.start)
      this.newEvent.startDate = arg.start
      this.newEvent.endDate = arg.end
      //    {
      // "type":"ATHLETIC_TRAINING",
      // "start":"2020-05-06T08:55:00+02:00",
      // "end":"2020-05-06T11:55:00+02:00",
      // "season":1,
      // "location":1,
      // "category":[
      //    1
      // ],
      // "resourcetype":"event"

      const event = {
        type: 'ATHLETIC_TRAINING',
        start: arg.start,
        end: arg.end,
        allDay: arg.allDay,
        season: 1,
        location: 1,
        category: [1, 2],
        resourcetype: 'event'
      }
      this.$store.dispatch('calendar/addEvent', event)
    },
    handleEventMouseEnter (arg) {
      // console.log('handling mouse event enter', arg)
    },
    confirmDeleteRecord () {
      console.log('event', this.editedEvent)
      this.childAddToEventPrompt.active = false
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: 'Confirm Delete',
        text: `You are about to delete "${this.editedEvent.title}"`,
        accept: this.deleteEvent,
        acceptText: 'Delete'
      })
    },
    deleteEvent () {
      this.$store.dispatch('calendar/deleteEvent', this.editedEvent)
        .then(res => {
          this.$vs.notify({
            color: 'success',
            title: 'Event Deleted',
            text: 'The selected event was successfully deleted'
          })
        })
        .catch(err => {
          this.$vs.notify({
            color: 'danger',
            title: 'Event Not Deleted',
            text: 'The selected user was successfully deleted'
          })
          console.error(err)
        })
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

    if (this.$acl.check('isCoach')) {
      console.log('Hello coach')
      this.$store.dispatch('calendar/fetchEventChoices')
      this.$store.dispatch('calendar/fetchCategories').then((response) => {
        this.addEventPrompt.options = this.addEventPrompt.selected = response.data.results
      })
    }
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

  .my-column {
    table {
      td {
        padding-right: .5rem;
        padding-bottom: .8rem;
        word-break: break-all;
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
