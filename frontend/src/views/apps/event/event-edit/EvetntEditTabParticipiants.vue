<template>
  <div id="event-edit-tab-participants">
    <div class="vx-row">
      <div class="vx-col w-full">
        <v-multiselect-listbox :options="this.usersData"
                               v-model="data_local"
                               :change="this.onChangeList()"
                               :reduce-display-property="(option) => option.displayName"
                               :reduce-value-property="(option) => option.id">
        </v-multiselect-listbox>
      </div>
    </div>
  </div>
</template>

<script>
import moduleUserManagement from '@/store/user-management/moduleUserManagement'

import vMultiselectListbox from 'vue-multiselect-listbox'
import 'vue-multiselect-listbox/dist/vue-multi-select-listbox.css'

export default {
  components: {
    vMultiselectListbox
  },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      data_local: this.data.participants,
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
    validateForm () {
      return !this.errors.any()
    },
    usersData () {
      return this.$store.state.userManagement.users.filter(member => member.userRole === 'child')
    }
  },
  methods: {
    reset_data () {
      this.data_local = this.data.participants
    },
    onChangeList () {
      console.log('change')
      this.changeEventParticipants()
    },
    changeEventParticipants () {
      const payload = {
        'id': this.data.id,
        'data': this.data_local.map(value => value.id)
      }
      this.$store.dispatch('calendar/changeEventMembersDirect', payload)
    }
  },
  created () {
    this.$store.dispatch('userManagement/fetchUsers')
  }
}
</script>
