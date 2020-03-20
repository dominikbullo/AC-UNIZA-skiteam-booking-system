<template>
  <vx-card no-shadow>

    <vs-input class="w-full mb-base" :type="passwordFieldType" label-placeholder="Old Password"
              v-model="old_password" icon-pack="feather" icon="icon-lock"/>
    <vs-input class="w-full mb-base" :type="passwordFieldType" label-placeholder="New Password"
              v-model="new_password" icon-pack="feather" icon="icon-lock"/>
    <vs-input class="w-full mb-base" :type="passwordFieldType" label-placeholder="Confirm Password"
              v-model="confirm_new_password" icon-pack="feather" icon="icon-lock"/>

    <!-- Save & Reset Button -->
    <div class="flex flex-wrap items-center justify-end">
      <vs-button class="ml-auto mt-2">Save Changes</vs-button>
      <vs-button class="ml-4 mt-2" type="border" color="warning" @click="resetData">Reset</vs-button>
      <vs-button class="ml-4 mt-2" @click="switchVisibility">show / hide</vs-button>
    </div>
  </vx-card>
</template>

<script>
export default {
  data () {
    return {
      old_password: '',
      new_password: '',
      confirm_new_password: '',
      passwordFieldType: 'password'
    }
  },
  computed: {
    activeUserInfo () {
      return this.$store.state.AppActiveUser
    }
  },
  methods: {
    switchVisibility () {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password'
    },
    resetData () {
      this.old_password = ''
      this.new_password = ''
      this.confirm_new_password = ''
    }
  }
}
</script>
