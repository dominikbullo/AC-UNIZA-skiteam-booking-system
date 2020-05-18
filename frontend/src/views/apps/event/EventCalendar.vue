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
          @eventDrop="handleEventDrop"
          @eventResize="handleEventResize"
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

      <!-- Add child to EVENT -->
      <vs-prompt
        :active.sync="childAddToEventPrompt.active"
        :is-valid="validForm"
        @accept="changeUserChildrenOnEvent"
        :accept-text="$t('Save')"
        class="my-prompt"
        :title="$t('Event detail')">


        <div v-if="editedEvent" id="event-info-table">
          <div class="vx-row">
            <div class="vx-col flex-1" id="event-info-col-1">
              <table>
                <tr>
                  <td class="font-bold">{{$t('Event type')}}</td>
                  <td>{{ $t(editedEvent.title) }}</td>
                </tr>
                <tr>
                  <td class="font-bold">{{$t('Location')}}</td>
                  <!-- TODO: Location with slope maybe? -->
                  <td>{{ editedEvent.location.displayName }}</td>
                </tr>
                <tr>
                  <td class="font-bold">{{$t('Category')}}</td>
                  <td>{{ displayObject(editedEvent.category).toString()}}</td>
                </tr>
              </table>
            </div>
          </div>
          <vs-divider></vs-divider>
          <div class="vx-row">
            <div class="vx-col flex-1" id="event-info-col-2">
              <table>
                <tr>
                  <td class="font-bold">{{$t('Start')}}</td>
                  <td>{{ editedEvent.start | time }}</td>
                </tr>
                <tr v-if="SKI_EVENTS.includes(editedEvent.type)">
                  <td class="font-bold">{{$t('Skis')}}</td>
                  <td>{{ editedEvent.skis_type }}</td>
                </tr>
              </table>
            </div>
            <div class="vx-col flex-1" id="event-info-col-3">
              <table>
                <tr>
                  <td class="font-bold">{{$t('End')}}</td>
                  <td>{{ editedEvent.end | time }}</td>
                </tr>
              </table>
            </div>
          </div>
          <!-- TODO: if exist -->
          <div v-if="editedEvent.additional_info" class="vx-row">
            <div class="vx-col">
              <p class="font-bold mr-5">{{$t('Additional Information')}}:</p>
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
            <vs-divider>{{$t('Your children')}}</vs-divider>
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
        @accept="addEvent"
        accept-text="Add event"
        class="my-prompt"
        :title="$t('Add Event')">

        <div class="vx-row">
          <div class="vx-col sm:w-1/2 w-full">
            <div class="mt-4">
              <label class="text-sm">{{$t('Event type')}}</label>
              <!-- RES: https://vue-select.org/ -->
              <v-select :clearable="false"
                        label="displayName"
                        :reduce="item => item.key"
                        v-model="addEventPrompt.type.selected"
                        :options="addEventPrompt.type.options"/>
            </div>
          </div>

          <div class="vx-col sm:w-1/2 w-full">
            <div class="mt-4">
              <label class="text-sm">{{$t('Location')}}</label>
              <v-select :clearable="false"
                        label="displayName"
                        :reduce="item => item.id"
                        v-model="addEventPrompt.location.selected"
                        :options="addEventPrompt.location.options"/>
            </div>
          </div>
        </div>

        <div class="vx-row">
          <div class="vx-col w-1/2">
            <div v-if="SKI_EVENTS.includes(addEventPrompt.type.selected)" class="mt-4">
              <label class="text-sm">{{$t('Skis')}}</label>
              <v-select :clearable="false"
                        label="displayName"
                        :reduce="item => item.key"
                        v-model="addEventPrompt.skis.selected"
                        :options="addEventPrompt.skis.options"/>
            </div>
          </div>

          <div class="vx-col w-1/2">
            <div v-if="addEventPrompt.type.selected === 'SKI_RACE'" class="vx-col w-full">
              <div class="mt-4">
                <label class="text-sm">{{$t('Organizer')}}</label>
                <v-select :clearable="false"
                          label="displayName"
                          :reduce="category => category.id"
                          v-model="addEventPrompt.raceOrganizer.selected"
                          :options="addEventPrompt.raceOrganizer.options"/>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-4">
          <label class="text-sm">{{$t('Category')}}</label>
          <v-select multiple
                    :closeOnSelect="false"
                    label="displayName"
                    :reduce="category => category.id"
                    v-model="addEventPrompt.category.selected"
                    :options="addEventPrompt.category.options"/>
        </div>
        <div class="vx-row">
          <div class="vx-col sm:w-1/2 w-full">
            <div class="mt-4">
              <label class="text-sm">{{$t('Start')}}</label>
              <flat-pickr v-model="newEvent.start"
                          :config="datePickerConfig"
                          class="w-full"
                          v-validate="'required'"
                          name="start"/>
              <span class="text-danger text-sm" v-show="errors.has('start')">{{ errors.first('start') }}</span>
            </div>
          </div>
          <div class="vx-col sm:w-1/2 w-full">
            <div class="mt-4">
              <label class="text-sm">{{$t('End')}}</label>
              <flat-pickr v-model="newEvent.end"
                          :config="datePickerConfig"
                          class="w-full"
                          v-validate="'required'"
                          name="end"/>
              <span class="text-danger text-sm" v-show="errors.has('end')">{{ errors.first('end') }}</span>
            </div>
          </div>
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
import enLocale from '@fullcalendar/core/locales/en-gb'
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

      SKI_EVENTS: ['SKI_TRAINING', 'SKI_RACE', 'SKI_CAMP'],

      calendarConfig: {
        locale: this.$i18n.locale === 'sk' ? skLocale : enLocale,
        selectable: this.$acl.check('isCoach'),
        editable: this.$acl.check('isCoach'),
        header: {
          // left: 'prev,next today addEvent',
          left: 'timeGridThreeDay,timeGridWeek,dayGridMonth,listWeek', // this will place the button on the right hand side
          center: 'title',
          right: 'today prev,next'
        },
        views: {
          timeGridThreeDay: {
            type: 'timeGrid',
            duration: { days: 3 },
            buttonText: `3 ${this.$t('day')}`
          },
          defaultView: screen.width <= 670 ? 'timeGridThreeDay' : 'timeGridWeek'
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
        category: {
          selected: [],
          options: []
        },
        type: {
          selected: 'SKI_TRAINING',
          options: []
        },
        skis: {
          selected: 'ALL',
          options: []
        },
        raceOrganizer: {
          selected: [],
          options: []
        },
        location: {
          selected: null,
          options: []
        }
      },

      configFromdateTimePicker: {
        minDate: new Date(),
        maxDate: null,
        enableTime: true
      },

      configToDateTimePicker: {
        enableTime: true,
        minDate: null
      },

      newEvent: {
        start: null,
        end: null,
        type: ''
      }
    }
  },
  computed: {
    minEventTime () {
      // TODO min time for view
      return '07:00:00'
    },
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
    displayObject (object, displayKey = 'displayName') {
      const ret = []
      Object.values(object).forEach((element) => {
        ret.push(element[displayKey])
      })

      return ret
    },
    getExtraInfo () {
      // TODO: Automatic with selecting event
      if (this.addEventPrompt.type.selected === 'SKI_TRAINING') {
        return { resourcetype: 'SkiTraining' }
      }
      if (this.addEventPrompt.type.selected === 'SKI_RACE') {
        return {
          resourcetype: 'SkiRace',
          organizer: this.addEventPrompt.raceOrganizer.selected
        }
      }
      return { resourcetype: 'Event' }
    },
    addEvent () {
      const eventForm = {
        category: this.addEventPrompt.category.selected,
        skis: this.addEventPrompt.skis.selected,
        type: this.addEventPrompt.type.selected,
        location: this.addEventPrompt.location.selected
      }
      const event = { ...this.newEvent, ...eventForm, ...this.getExtraInfo() }

      this.$store.dispatch('calendar/addEvent', event)
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

      // if (this.$acl.check('isCoach')) {
      //   const categoriesOnEvent = []
      //   const category = this.$store.state.calendar.eventConfig.categories
      //   Object.values(category).forEach((categoryOnEvent) => {
      //     categoriesOnEvent.push(category.find(function (entry) {
      //         return entry.id === categoryOnEvent.id
      //       })
      //     )
      //   })
      //   this.editedEvent.category = categoriesOnEvent
      // }

      // IDEA: Check with userChildren() array
      // console.log('participants', this.editedEvent['participants'])
      const myChildrenOnEvent = this.editedEvent['participants'].filter(obj => {
        // console.log('obj', obj)
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
      console.log('arg', arg)
      this.newEvent.start = arg.start
      this.newEvent.end = arg.end
      this.addEventPrompt.active = true
    },
    handleEventChange (arg) {
      console.log('handling change in event', arg.event.id, arg)
      const event = {
        id: arg.event.id,
        start: arg.event.start,
        end: arg.event.end
      }

      this.$store.dispatch('calendar/editEvent', { ...event, ...this.getExtraInfo() })
        .then(res => {
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
    handleEventDrop (eventDropInfo) {
      console.log('dropped', eventDropInfo)
      this.handleEventChange(eventDropInfo)
    },
    handleEventResize (eventResizeInfo) {
      console.log('resized', eventResizeInfo)
      this.handleEventChange(eventResizeInfo)
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
        text: `You are about to delete '${this.editedEvent.title}'`,
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
        'eventAdd': this.childAddToEventPrompt.selected,
        'eventDelete': this.childAddToEventPrompt.onEvent
      }

      this.$store.dispatch('calendar/changeEventMembers', payload)
    },
    cleanData (object, key = 'id') {
      const id = []
      Object.values(object).forEach((item) => {
        id.push(item[key])
      })
      return id
    },
    fetchConfigData () {
      console.log('Hello coach')

      this.$store.dispatch('calendar/fetchRaceOrganizers').then((res) => {
        // console.log('raceorganizers', res.data.results)
        this.addEventPrompt.raceOrganizer.options = res.data.results
        this.addEventPrompt.raceOrganizer.selected = this.cleanData(this.addEventPrompt.raceOrganizer.options)[0]
      })

      this.$store.dispatch('calendar/fetchLocations').then((res) => {
        // console.log('locations', res.data.results)
        this.addEventPrompt.location.options = res.data.results
        this.addEventPrompt.location.selected = this.cleanData(this.addEventPrompt.location.options)[0]
      })

      this.$store.dispatch('calendar/fetchCategories').then((res) => {
        this.addEventPrompt.category.options = res.data.results
        this.addEventPrompt.category.selected = this.cleanData(this.addEventPrompt.category.options)
      })


      this.$store.dispatch('calendar/fetchEventChoices').then((res) => {
        this.addEventPrompt.type.options = res.data.EventTypeChoices
        this.addEventPrompt.skis.options = res.data.SkiTypeChoices
      })
    }
  },
  created () {
    this.$store.dispatch('calendar/fetchEvents')
    this.$store.dispatch('family/fetchFamily', this.$store.state.AppActiveUser.profile.family_id)

    if (this.$acl.check('isCoach')) {
      this.fetchConfigData()
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


  .my-prompt {
    .vs-dialog {
      max-width: 650px;
    }

    /*@media only screen and (max-width: 768px) {*/
    /*  .vs-dialog {*/
    /*    max-width: 400px;*/
    /*  }*/
    /*}*/
    @media only screen and (max-width: 570px) {
      .vs-dialog {
        max-width: 90%;
      }
    }
  }

  .fc-left .fc-button-group {
    display: block;
  }

  .fc-toolbar h2 {
    font-size: 1.5em;
  }


</style>
