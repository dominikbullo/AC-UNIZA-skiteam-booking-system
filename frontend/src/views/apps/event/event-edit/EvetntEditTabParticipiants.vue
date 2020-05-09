<template>
  <div id="event-edit-tab-participants">
    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2">
        <!--        <pre>{{data_local.participants}}</pre>-->
        <!--        <pre>{{data_local}}</pre>-->
        <div class="flex items-end mb-5">
          <span class="leading-none font-medium">Have been logged in to the event</span>
        </div>
        <ul class="centerx">
          <li :key="user.id" class="mb-2" v-for="user in this.eventParticipants">
            <vs-checkbox
              :vs-value="user.username"
              color="success"
              v-model="data_local">
              {{ user.displayName }}
            </vs-checkbox>
          </li>
        </ul>
      </div>
      <div class="vx-col w-full md:w-1/2">
        <div class="flex items-end mb-5">
          <span class="leading-none font-medium">Have't been logged in to the event</span>
        </div>
        <ul class="centerx">
          <li :key="user.id" class="mb-2" v-for="user in this.usersData">
            <vs-checkbox
              :vs-value="user.username"
              color="success"
              v-model="data_local">
              {{ user.displayName }}
            </vs-checkbox>
          </li>
        </ul>

        <!--        <pre>{{data}}</pre>-->
      </div>
    </div>
    <div class="vx-row">
      <div class="vx-col w-full">
        {{data_local}}
        <div class="mt-8 flex flex-wrap items-center justify-end">
          <vs-button :disabled="!validateForm" @click="changeEventParticipants" class="ml-auto mt-2">Save Changes
          </vs-button>
          <vs-button @click="reset_data" class="ml-4 mt-2" color="warning" type="border">Reset</vs-button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import vSelect from 'vue-select'
import moduleUserManagement from '@/store/user-management/moduleUserManagement'

export default {
  components: {
    vSelect,
    flatPickr
  },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      data_local: this.formatLocalData(),

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
      return this.$store.state.userManagement.users
    }
  },
  methods: {
    reset_data () {
      this.data_local = this.formatLocalData()
    },
    formatLocalData () {
      const cleanData = []
      Object.values(this.data.participants).forEach((element) => {
        cleanData.unshift(element.username)
      })
      return cleanData
    },
    changeEventParticipants () {
      const userNames = []
      this.data.participants.forEach((element) => {
        userNames.unshift(element['username'])
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
    this.changeEventParticipants()
  }
}
</script>
