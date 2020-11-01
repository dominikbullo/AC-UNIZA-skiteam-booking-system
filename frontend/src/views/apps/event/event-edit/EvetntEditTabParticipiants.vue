<template>
  <div id="event-edit-tab-participants">
    <!--    <pre>{{ this.data_local }}</pre>-->
    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2">
        <vs-list>
          <vs-list-header title="People Group 2" color="primary"></vs-list-header>

          <draggable :list="this.usersData" group="people" class="p-2 cursor-move">
            <!-- TODO: subtitle, category or family-->
            <vs-list-item v-for="user in this.usersData"
                          :key="user.id"
                          :vs-value="user.id"
                          v-model="data_local"
                          :title="user.displayName">
              <vs-avatar slot="avatar" :text="user.name"/>
            </vs-list-item>
          </draggable>

        </vs-list>
        <pre>{{ this.usersData }}</pre>
      </div>
      <div class="vx-col w-full md:w-1/2">
        <!--        <pre>{{ this.eventParticipants }}</pre>-->
        <vs-list>
          <vs-list-header title="People Group 1" color="primary"></vs-list-header>
          <draggable :list="this.eventParticipants" group="people" class="p-2 cursor-move">
            <vs-list-item v-for="user in this.eventParticipants"
                          :key="user.id"
                          :vs-value="user.id"
                          v-model="data_local"
                          :title="user.displayName"
                          :subtitle="user.username">
              <vs-avatar slot="avatar" :text="user.name"/>
            </vs-list-item>
          </draggable>

        </vs-list>
        <pre>{{ this.eventParticipants }}</pre>
      </div>

    </div>
  </div>

</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import vSelect from 'vue-select'
import moduleUserManagement from '@/store/user-management/moduleUserManagement'
import draggable from 'vuedraggable'

export default {
  components: {
    vSelect,
    flatPickr,
    draggable
  },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      data_local: this.data,
      langOptions: [
        {
          label: 'English',
          value: 'english'
        },
        {
          label: 'Slovak',
          value: 'slovak'
        }
      ]
    }
  },
  computed: {
    eventParticipants () {
      return this.data.participants
    },
    validateForm () {
      return !this.errors.any()
    },
    usersData () {
      // Filter only child, but in future could delete this filter
      return this.$store.state.userManagement.users.filter(member => member.userRole === 'child')
    }
  },
  methods: {
    reset_data () {
      this.data_local = this.data.participants
    },
    changeEventParticipants () {
      console.log('--------data-------------', this.data.participants)
      const userNames = []
      this.data.participants.forEach((element) => {
        userNames.unshift(element['id'])
      })

      const payload = {
        'eventID': this.data.id,
        'eventAdd': this.data_local,
        'eventDelete': userNames.filter(x => !this.data_local.includes(x))
      }
      this.$store.dispatch('calendar/changeEventMembers', payload).then(res => {
        this.data = res.data
      })
    }
  },
  created () {
    if (!moduleUserManagement.isRegistered) {
      this.$store.registerModule('userManagement', moduleUserManagement)
      moduleUserManagement.isRegistered = true
    }
    this.$store.dispatch('userManagement/fetchUsers')
  }
}
</script>
