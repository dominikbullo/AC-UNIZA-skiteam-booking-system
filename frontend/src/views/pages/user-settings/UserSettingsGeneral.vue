<template>
  <vx-card no-shadow>
    {{data}}
    <!-- Img Row -->
    <!--    <div class="flex flex-wrap items-center mb-base">-->
    <!--      <vs-avatar :src="activeUserInfo.photoURL" size="70px" class="mr-4 mb-4"/>-->
    <!--      &lt;!&ndash;TODO change photo&ndash;&gt;-->
    <!--      <div>-->
    <!--        <vs-button class="mr-4 sm:mb-0 mb-2">Upload photo</vs-button>-->
    <!--        <vs-button type="border" color="danger">Remove</vs-button>-->
    <!--        <p class="text-sm mt-2">Allowed JPG, GIF or PNG. Max size of 800kB</p>-->
    <!--      </div>-->
    <!--    </div>-->

    <!-- Info -->
    <div class="vx-row">
      <div class="vx-col sm:w-1/2 w-full mb-2">
        <vs-input class="w-full mb-base" icon-pack="feather" icon="icon-user" label-placeholder="First Name"
                  v-model="first_name"></vs-input>
      </div>
      <div class="vx-col sm:w-1/2 w-full mb-2">
        <vs-input class="w-full mb-base" icon-pack="feather" icon="icon-user" label-placeholder="Last Name"
                  v-model="last_name"></vs-input>
      </div>
    </div>

    <div class="vx-col sm:w-1/2 w-full mb-2">
      <vs-input class="w-full mb-base" icon-pack="feather" icon="icon-mail" label-placeholder="Email"
                v-model="email"></vs-input>
    </div>

    <!-- Save & Reset Button -->
    <div class="flex flex-wrap items-center justify-end">
      <vs-button class="ml-auto mt-2" @click="saveData">Save Changes</vs-button>
      <vs-button class="ml-4 mt-2" type="border" color="warning" @click="resetData">Reset</vs-button>
    </div>
  </vx-card>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      name: '',
      email: '',
      full_name: '',
      first_name: '',
      last_name: ''
    }
  },
  created () {
    this.resetData()
  },
  computed: {
    activeUserInfo () {
      return this.$store.state.AppActiveUser
    },
    validateForm () {
      return !this.errors.any()
    }
  },
  methods: {
    resetData () {
      // TODO: for loop -> if key update
      this.first_name = this.$store.state.AppActiveUser.first_name
      this.last_name = this.$store.state.AppActiveUser.last_name
      this.email = this.$store.state.AppActiveUser.email
      // this.username = this.$store.state.AppActiveUser.username
      // this.name = this.$store.state.AppActiveUser.displayName
      // this.full_name = this.$store.state.AppActiveUser.displayName
    },
    saveData () {
      if (!this.validateForm) return

      const payload = {
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email
      }
      throw new Error('saveData - Not implemented yet!')
      this.$store.dispatch('editUser', payload)
    }
  }
}
</script>
