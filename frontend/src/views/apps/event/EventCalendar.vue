<template>
  <div id="event-calendar">
    <vx-card class="mt-10">
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

    <!-- ADD EVENT -->
    <vs-prompt
      :active.sync="activePromptAddEvent"
      :is-valid="validForm"
      @accept="addEvent"
      accept-text="Add Event"
      class="calendar-event-dialog"
      title="Add Event">

      <div class="calendar__label-container flex">

<!--        <vs-chip :class="'bg-' + labelColor(labelLocal)" class="text-white" v-if="labelLocal != 'none'">{{ labelLocal-->
<!--          }}-->
<!--        </vs-chip>-->

        <vs-dropdown class="ml-auto my-2 cursor-pointer" vs-custom-content vs-trigger-click>

          <feather-icon @click.prevent class="cursor-pointer" icon="TagIcon" svgClasses="h-5 w-5"></feather-icon>

          <vs-dropdown-menu style="z-index: 200001">
            <vs-dropdown-item :key="index" @click="labelLocal = label.value" v-for="(label, index) in calendarLabels">
              <div :class="'bg-' + label.color" class="h-3 w-3 inline-block rounded-full mr-2"></div>
              <span>{{ label.text }}</span>
            </vs-dropdown-item>

            <vs-dropdown-item @click="labelLocal = 'none'">
              <div class="h-3 w-3 mr-1 inline-block rounded-full mr-2 bg-primary"></div>
              <span>None</span>
            </vs-dropdown-item>
          </vs-dropdown-menu>
        </vs-dropdown>

      </div>

      <vs-input class="w-full" label-placeholder="Event Title" name="event-name" v-model="title"
                v-validate="'required'"></vs-input>
      <div class="my-4">
        <small class="date-label">Start Date</small>
        <datepicker :disabled="disabledFrom" :language="$vs.rtl ? langHe : langEn" name="start-date"
                    v-model="startDate"></datepicker>
      </div>
      <div class="my-4">
        <small class="date-label">End Date</small>
        <datepicker :disabledDates="disabledDatesTo" :language="$vs.rtl ? langHe : langEn" name="end-date"
                    v-model="endDate"></datepicker>
      </div>
      <vs-input :color="!errors.has('event-url') ? 'success' : 'danger'" class="w-full mt-6" label-placeholder="Event URL" name="event-url" v-model="url"
                v-validate="'url'"></vs-input>

    </vs-prompt>

    <!-- EDIT EVENT -->
    <vs-prompt
      :active.sync="activePromptEditEvent"
      :is-valid="validForm"
      @accept="editEvent"
      @cancel="removeEvent"
      accept-text="Submit"
      button-cancel="border"
      cancel-text="Remove"
      class="calendar-event-dialog"
      title="Edit Event">

      <div class="calendar__label-container flex">

<!--        <vs-chip :class="'bg-' + labelColor(labelLocal)" class="text-white" v-if="labelLocal != 'none'">{{ labelLocal-->
<!--          }}-->
<!--        </vs-chip>-->

        <vs-dropdown class="ml-auto my-2 cursor-pointer" vs-custom-content>

          <feather-icon @click.prevent icon="TagIcon" svgClasses="h-5 w-5"></feather-icon>

          <vs-dropdown-menu style="z-index: 200001">
            <vs-dropdown-item :key="index" @click="labelLocal = label.value" v-for="(label, index) in calendarLabels">
              <div :class="'bg-' + label.color" class="h-3 w-3 inline-block rounded-full mr-2"></div>
              <span>{{ label.text }}</span>
            </vs-dropdown-item>

            <vs-dropdown-item @click="labelLocal = 'none'">
              <div class="h-3 w-3 mr-1 inline-block rounded-full mr-2 bg-primary"></div>
              <span>None</span>
            </vs-dropdown-item>
          </vs-dropdown-menu>
        </vs-dropdown>

      </div>

      <vs-input class="w-full" label-placeholder="Event Title" name="event-name" v-model="title"
                v-validate="'required'"></vs-input>
      <div class="my-4">
        <small class="date-label">Start Date</small>
        <datepicker :disabledDates="disabledDatesFrom" :language="$vs.rtl ? langHe : langEn" name="start-date"
                    v-model="startDate"></datepicker>
      </div>
      <div class="my-4">
        <small class="date-label">End Date</small>
        <datepicker :disabledDates="disabledDatesTo" :language="$vs.rtl ? langHe : langEn" name="end-date"
                    v-model="endDate"></datepicker>
      </div>
      <vs-input :color="!errors.has('event-url') ? 'success' : 'danger'" class="w-full mt-6" label-placeholder="Event URL" name="event-url" v-model="url"
                v-validate="'url'"></vs-input>

    </vs-prompt>

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
      activePromptAddEvent: true,
      activePromptEditEvent: false,

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
      this.activePromptAddEvent = true
      //  start: arg.date,
      // allDay: arg.allDay
      // if (confirm('Would you like to add an event to ' + arg.dateStr + ' ?')) {
      //   this.calendarEvents.push({ // add new event data
      //     title: 'New Event',
      //     start: arg.date,
      //     allDay: arg.allDay
      //   })
      // }
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

 .fc-toolbar .fc-header-toolbar {
      margin-bottom: 5.5em;
 }
  .fc-list-heading td {
    background: #00b0d3;
    color: white;
  }
</style>
