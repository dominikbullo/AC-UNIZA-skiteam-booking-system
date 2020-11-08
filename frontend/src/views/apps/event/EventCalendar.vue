<template>
  <div id="event-calendar-app">
    <vx-card class="mt-5 vx-card">
      <div class="calendar-view  no-scroll-content">
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

      <!-- TODO: separate component-->
      <!-- Add child to EVENT -->
      <vs-prompt
          :active.sync="childAddToEventPrompt.active"
          :is-valid="validForm"
          @accept="changeUserChildrenOnEvent"
          :accept-text="$t('Save')"
          class="my-prompt"
          :title="$t('Event detail')">

        <vs-tabs>
          <vs-tab label="Home">
            <div v-if="editedEvent" id="event-info-table" class="con-tab-ejemplo">

              <div class="vx-row">
                <div class="vx-col flex-1" id="event-info-col-2">
                  <table>
                    <tr>
                      <td class="font-bold">{{ $t('Location') }}</td>
                      <td>{{ editedEvent.location.displayName }}</td>
                    </tr>
                    <tr>
                      <td class="font-bold">{{ $t('Category') }}</td>
                      <td>{{ displayObject(editedEvent.category).toString() }}</td>
                    </tr>
                    <tr v-if="editedEvent.type.need_skis">
                      <td class="font-bold">{{ $t('Skis') }}</td>
                      <td>{{ displayObject(editedEvent.skis_type).toString() }}</td>
                    </tr>
                  </table>
                </div>
              </div>
              <div v-if="editedEvent.additional_info" class="vx-row">
                <div class="vx-col">
                  <p class="font-bold mr-5">{{ $t('Additional Information') }}:</p>
                  <p>{{ editedEvent.additional_info }}</p>
                </div>
              </div>
              <div v-if="$acl.check('isCoach')">
                <vs-divider>Coach zone</vs-divider>
                <div class="vx-col w-full flex flex-wrap items-center justify-center">

                  <vs-button icon-pack="feather" icon="icon-edit" class="mr-4"
                             :to="{name: 'app-event-edit', params: { eventId: this.editedEvent.id }}">Edit event
                  </vs-button>

                  <vs-button type="border" icon="group" class="mr-4"
                             :to="{name: 'app-event-edit', hash:'#participants',
                           params: { eventId: this.editedEvent.id }}"> Edit participants
                  </vs-button>

                  <vs-button type="border" color="danger" icon-pack="feather" icon="icon-trash"
                             @click="confirmDeleteRecord">Delete
                  </vs-button>
                </div>
              </div>

              <ul class="centerx">
                <vs-divider>{{ $t('Your children') }}</vs-divider>
                <!--            <pre>{{ userChildren }}</pre>-->
                <li class="mb-2" :key="child.user.profile.id" v-for="child in userChildren">
                  <vs-checkbox
                      :vs-value="child.user.profile.id"
                      color="success"
                      v-model="childAddToEventPrompt.selected">
                    {{ child.user.first_name }} {{ child.user.last_name }}
                  </vs-checkbox>
                </li>
              </ul>

            </div>
          </vs-tab>

          <vs-tab label="Detail">
            <div v-if="editedEvent" class="con-tab-ejemplo vx-row">
              <div class="vx-col flex-1" id="event-info-col-1">
                <table>
                  <tr>
                    <td class="font-bold">{{ $t('Start') }}</td>
                    <td>{{ editedEvent.start | time(true) }}</td>
                  </tr>
                  <tr v-if="editedEvent.type.need_skis">
                    <td class="font-bold">{{ $t('Skis') }}</td>
                    <td>{{ displayObject(editedEvent.skis_type).toString() }}</td>
                  </tr>
                  <tr>
                    <td class="font-bold">{{ $t('Start date') }}</td>
                    <td>{{ editedEvent.start | date }}</td>
                  </tr>
                  <tr>
                    <td class="font-bold">{{ $t('Event type') }}</td>
                    <td>{{ $t(editedEvent.type.displayName) }}</td>
                  </tr>
                </table>
                <vs-button v-if="editedEvent.accommodation.length <= 0"
                           icon-pack="feather" icon="icon-edit"
                           type="border" color="warning" class="mt-4"
                           :to="{name: 'app-event-edit', hash:'#accommodation',
                           params: { eventId: this.editedEvent.id }}">Add accommodation
                </vs-button>
              </div>
            </div>
          </vs-tab>

          <vs-tab label="Accommodation" v-if="editedEvent && editedEvent.accommodation.length > 0">
            <vs-table ref="table" :data="editedEvent.accommodation">
              <template slot="thead">
                <vs-th sort-key="name">Name</vs-th>
                <vs-th sort-key="from">From</vs-th>
                <vs-th sort-key="to">To</vs-th>
                <vs-th sort-key="price">Price adult</vs-th>
                <vs-th sort-key="price-child">Price child</vs-th>
                <vs-th>Action</vs-th>
              </template>

              <template slot-scope="{data}">
                <tbody>
                <vs-tr :data="tr" :key="indextr" v-for="(tr, indextr) in data">

                  <vs-td>
                    <p class="hotel-name font-medium truncate">{{ tr.name }}</p>
                  </vs-td>


                  <vs-td>
                    <p class="hotel-name font-medium truncate">{{ tr.start | date }}</p>
                  </vs-td>

                  <vs-td>
                    <p class="hotel-name font-medium truncate">{{ tr.end | date }}</p>
                  </vs-td>

                  <vs-td>
                    <p class="product-price">{{ tr.price }}€</p>
                  </vs-td>

                  <vs-td>
                    <p class="product-price">{{ tr.price }}€</p>
                  </vs-td>

                  <vs-td class="whitespace-no-wrap">
                    <feather-icon icon="LinkIcon" svgClasses="w-5 h-5 hover:text-primary stroke-current"
                                  @click.stop="alert('Not implemented yet')"/>
                    <!--                    <feather-icon icon="ThumbsUpIcon" svgClasses="w-5 h-5 hover:text-success stroke-current"-->
                    <!--                                  class="ml-2"-->
                    <!--                                  @click.stop="alert('Not implemented yet')"/>-->
                  </vs-td>

                </vs-tr>
                </tbody>
              </template>
            </vs-table>
            <vs-button icon-pack="feather" icon="icon-edit" type="border" color="warning" class="mt-4"
                       :to="{name: 'app-event-edit', hash:'#accommodation',
                           params: { eventId: this.editedEvent.id }}">Edit accommodation
            </vs-button>
          </vs-tab>

        </vs-tabs>
      </vs-prompt>


      <!-- ADD EVENT -->
      <vs-prompt
          :active.sync="addEventPrompt.active"
          :is-valid="true"
          @accept="addEvent"
          accept-text="Add event"
          class="my-prompt"
          id="calendar-add-event-prompt"
          :title="$t('Add Event')">

        <div class="vx-row">
          <!--          <p>{{ this.addEventPrompt }}</p>-->
          <div class="vx-col sm:w-1/2 w-full">
            <div class="mt-4">
              <label class="text-sm">{{ $t('Event type') }} </label>
              <!-- RES: https://vue-select.org/ -->
              <v-select :clearable="false"
                        label="displayName"
                        v-model="addEventPrompt.type.selected"
                        :options="addEventPrompt.type.options"/>
            </div>
          </div>

          <div class="vx-col sm:w-1/2 w-full">
            <div class="mt-4">
              <label class="text-sm">{{ $t('Location') }}</label>
              <v-select :clearable="false"
                        label="displayName"
                        v-model="addEventPrompt.location.selected"
                        :options="addEventPrompt.location.options"/>
            </div>
          </div>
        </div>

        <div class="vx-row">
          <div v-if="this.needSkis" class="vx-col w-1/2">
            <div class="mt-4">
              <label class="text-sm">{{ $t('Skis') }}</label>
              <ul class="centerx demo-alignment">
                <li :key="item.id" v-for="item in this.addEventPrompt.skis_type.options">
                  <vs-checkbox
                      :vs-value="item.id"
                      color="success"
                      v-model="addEventPrompt.skis_type.selected">
                    {{ item.displayName }}
                  </vs-checkbox>
                </li>
              </ul>
            </div>
          </div>

          <div v-if="this.isSkiRace" class="vx-col w-1/2">
            <div class="mt-4">
              <label class="text-sm">{{ $t('Organizer') }}</label>
              <v-select :clearable="false"
                        label="displayName"
                        v-model="addEventPrompt.raceOrganizer.selected"
                        :options="addEventPrompt.raceOrganizer.options"/>
            </div>
          </div>
        </div>

        <div class="mt-4">
          <label class="text-sm">{{ $t('Category') }}</label>
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
              <label class="text-sm">{{ $t('Start') }}</label>
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
              <label class="text-sm">{{ $t('End') }}</label>
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
import rrulePlugin from '@fullcalendar/rrule'
import listPlugin from '@fullcalendar/list'
import skLocale from '@fullcalendar/core/locales/sk'
import enLocale from '@fullcalendar/core/locales/en-gb'
import vSelect from 'vue-select'
import 'vue-select/dist/vue-select.css'

import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { Slovak } from 'flatpickr/dist/l10n/sk.js'

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
      },

      datePickerConfig: {
        locale: Slovak,
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
          selected: [],
          options: []
        },
        skis_type: {
          selected: [],
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
      // TODO scroll to first event or current time
      return '07:00:00'
    },
    calendarEvents () {
      return this.$store.getters['calendar/getEventsForCal']
    },
    userChildren () {
      return this.$store.getters['family/familyChildren']
    },
    needSkis () {
      return this.addEventPrompt.type.selected.need_skis === true
    },
    isSkiTraining () {
      return this.addEventPrompt.type.selected.type === 'TRAINING' && this.needSkis
    },
    isSkiRace () {
      return this.addEventPrompt.type.selected.type === 'RACE' && this.needSkis
    },
    validForm () {
      // FIXME validate
      return true
    }
  },
  methods: {
    eventRender (item) {
      // Adding class to old events for css
      if (item.event.start < new Date().getTime()) {
        item.el.classList.add('past-event')
      }
    },
    displayObject (object, displayKey = 'displayName') {
      const ret = []
      Object.values(object).forEach((element) => {
        ret.push(element[displayKey])
      })
      return ret
    },
    getExtraInfo () {
      // TODO: separate method called from whole app
      // console.log('this.addEventPrompt', this.addEventPrompt)
      // console.log('TRAINING', this.addEventPrompt.type.selected.type === 'TRAINING')
      // console.log('RACE', this.addEventPrompt.type.selected.type === 'RACE')
      // console.log('this.addEventPrompt2', this.addEventPrompt.type.selected.need_skis)

      if (this.isSkiTraining) {
        return { resourcetype: 'SkiTraining' }
      }

      if (this.isSkiRace) {
        return {
          resourcetype: 'SkiRace',
          organizer: this.addEventPrompt.raceOrganizer.selected.id
        }
      }
      return { resourcetype: 'Event' }
    },

    addEvent () {
      console.log('this.addEventPrompt', this.addEventPrompt)
      const eventForm = {
        category: this.addEventPrompt.category.selected,
        skis_type: this.addEventPrompt.skis_type.selected,
        type: this.addEventPrompt.type.selected.id,
        location: this.addEventPrompt.location.selected
      }
      const event = { ...this.newEvent, ...eventForm, ...this.getExtraInfo() }

      this.$store.dispatch('calendar/addEvent', event)
    },
    handleDateClick (arg) {
      console.log('handling date click', arg)
    },
    handleEventClick (arg) {
      // TODO: allow click for example 14 days to view Accommodation
      console.log('event click', arg)
      if (this.$acl.not.check('isCoach') && new Date(arg.event.start).valueOf() < new Date().valueOf()) {
        this.$vs.notify({
          color: 'danger',
          title: 'Old event',
          text: 'You cannot change an event which has already happened'
        })
        return false
      }

      this.$store.dispatch('calendar/fetchEvent', arg.event.id)
        .then(res => {
          this.editedEvent = res.data

          const childrenUsersID = []
          Object.values(this.$store.getters['family/familyChildren']).forEach(obj => {
            childrenUsersID.push(obj.user.profile.id)
          })
          console.log('childrenUsersID', childrenUsersID)

          const eventChildren = []
          Object.values(this.editedEvent['participants']).forEach(obj => {
            eventChildren.push(obj.id)
          })
          console.log('eventChildren', eventChildren)

          const userChildrenOnEvent = childrenUsersID.filter(x => eventChildren.includes(x))
          console.log('userChildrenOnEvent', userChildrenOnEvent)

          this.childAddToEventPrompt.onEvent = userChildrenOnEvent
          this.childAddToEventPrompt.selected = userChildrenOnEvent

          this.childAddToEventPrompt.active = true
        })
    },
    handleSelect (arg) {
      if (this.$acl.check('isCoach')) this.fetchConfigData()

      this.newEvent.start = arg.start
      this.newEvent.end = arg.end
      this.addEventPrompt.active = true
    },

    handleEventChange (arg) {
      console.log('handling change in event', arg.event.id, arg)
      console.log('handling change in start', arg.event.start)
      console.log('handling change in end', arg.event.end)

      const event = {
        id: arg.event.id,
        start: arg.event.start,
        end: arg.event.end
      }

      this.$store.dispatch('calendar/editEvent', { ...event, ...this.getExtraInfo() })
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
      console.error('do not use this method anymore!')
      return object.map(value => value[key])
    },

    fetchConfigData () {
      console.log('Hello coach')
      // this.$vs.loading()


      this.$store.dispatch('calendar/fetchCategories').then((res) => {
        this.addEventPrompt.category.options = res.data.results
        this.addEventPrompt.category.selected = this.addEventPrompt.category.options.map(x => x.id)
      })

      // TODO: Location base on event type
      this.$store.dispatch('calendar/fetchLocations').then((res) => {
        // console.log('locations', res.data.results)
        this.addEventPrompt.location.options = res.data.results
        this.addEventPrompt.location.selected = this.addEventPrompt.location.options.map(x => x.id)[0]
      })

      this.$store.dispatch('calendar/fetchSkisTypes').then((res) => {
        console.log('event types data', res.data.results)
        this.addEventPrompt.skis_type.options = res.data.results
        this.addEventPrompt.skis_type.selected = this.addEventPrompt.skis_type.options.map(x => x.id)
      })

      this.$store.dispatch('calendar/fetchRaceOrganizers').then((res) => {
        this.addEventPrompt.raceOrganizer.options = res.data.results
        this.addEventPrompt.raceOrganizer.selected = this.addEventPrompt.raceOrganizer.options[0]
      })
    }
  },
  created () {
    this.$store.dispatch('calendar/fetchEvents')
    this.$store.dispatch('family/fetchFamily', this.$store.getters['familyID'])

    this.$store.dispatch('calendar/fetchEventTypes').then((res) => {
      this.addEventPrompt.type.options = res.data.results
      this.addEventPrompt.type.selected = this.addEventPrompt.type.options[0]
    })
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

.flatpickr-input[type="hidden"] + input {
  color: #c2c6dc;
}

.fc-left .fc-button-group {
  display: block;
}

.fc-toolbar h2 {
  font-size: 1.5em;
}

.demo-alignment {
  & > * {
    margin-right: .5rem;
    margin-top: .4rem;
  }
}

//RES: https://stackoverflow.com/questions/12632229/change-color-of-past-events-in-fullcalendar
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

.fc-body .fc-row {
  min-height: 450px;
}
</style>
