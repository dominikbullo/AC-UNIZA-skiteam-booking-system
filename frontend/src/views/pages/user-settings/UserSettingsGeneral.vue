<template>
  <vx-card no-shadow>
    <!--    Img Row-->
    <div class="flex flex-wrap items-center mb-base">
      <vs-avatar :src="activeUserInfo.photoURL" size="70px" class="mr-4 mb-4"/>
      <!--TODO change photo-->
      <div>
        <!-- RES: https://stackoverflow.com/questions/572768/styling-an-input-type-file-button -->
        <input id="user-settings-general-input-upload-photo"
               type="file" accept="image/jpeg"
               style="display:none;"/>
        <vs-button id="user-settings-general-upload-photo-button" class="mr-4 sm:mb-0 mb-2">Upload photo</vs-button>
        <vs-button type="border" color="danger">Remove</vs-button>
        <p class="text-sm mt-2">Allowed JPG, GIF or PNG. Max size of 800kB</p>
      </div>
    </div>

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

    <!-- Email -->
    <vs-input class="w-full" label-placeholder="Email" v-model="email"></vs-input>

    <vs-alert icon-pack="feather" icon="icon-info" class="h-full my-4" color="warning">
      <span>Your account is not verified. <a href="#" class="hover:underline">Resend Confirmation</a></span>
    </vs-alert>

    <!-- Save & Reset Button -->
    <div class="flex flex-wrap items-center justify-end">
      <vs-button class="ml-auto mt-2" @click="save_changes">{{ $t('Save Changes') }}</vs-button>
      <vs-button class="ml-4 mt-2" type="border" color="warning" @click="reset_data">{{ $t('Reset') }}</vs-button>
    </div>
  </vx-card>
</template>

<script>

export default {
  data () {
    return {
      email: '',
      first_name: '',
      last_name: ''
    }
  },
  created () {
    this.reset_data()
  },
  mounted () {
    document.getElementById('user-settings-general-upload-photo-button').addEventListener('click', () => {
      document.getElementById('user-settings-general-input-upload-photo').click()
    })
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
    reset_data () {
      // TODO: for loop -> if key update
      this.first_name = this.$store.state.AppActiveUser.first_name
      this.last_name = this.$store.state.AppActiveUser.last_name
      this.email = this.$store.state.AppActiveUser.email
    },
    save_changes () {
      if (!this.validateForm) return

      const payload = {
        first_name: this.first_name,
        last_name: this.last_name
      }
      this.$store.dispatch('userManagement/editUser', payload)
        .then(res => {
          this.$vs.notify({
            color: 'success',
            title: 'User details changed'
          })
        })
        .catch(err => {
          this.$vs.notify({
            color: 'danger',
            title: 'Something went wrong',
            text: err.message
          })
        })
    }
  }
}
</script>
