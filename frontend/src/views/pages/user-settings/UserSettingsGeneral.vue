<template>
  <vx-card no-shadow>

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

    <!--    <vs-input class="w-full mb-base" icon-pack="feather" icon="icon-user" label-placeholder="Username"-->
    <!--              v-model="username"></vs-input>-->
    <!-- FIXME: If email change then need to verified again -->
    <vs-input class="w-full mb-base" icon-pack="feather" icon="icon-mail" label-placeholder="Email"
              v-model="email"></vs-input>
    <!--    <vs-input class="w-full mb-base" icon-pack="feather" icon="icon-user" label-placeholder="Full Name"-->
    <!--              v-model="full_name"></vs-input>-->


    <!-- Save & Reset Button -->
    <div class="flex flex-wrap items-center justify-end">
      <vs-button class="ml-auto mt-2">Save Changes</vs-button>
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
    }
  },
  methods: {
    resetData () {
      // TODO: for loop -> if key update
      this.username = this.$store.state.AppActiveUser.username
      this.name = this.$store.state.AppActiveUser.displayName
      this.email = this.$store.state.AppActiveUser.email
      this.full_name = this.$store.state.AppActiveUser.displayName
      this.first_name = this.$store.state.AppActiveUser.first_name
      this.last_name = this.$store.state.AppActiveUser.last_name
    }
  }
}
</script>
