<template>
  <vx-card no-shadow>
    <vs-input class="w-full mb-base" :type="passwordFieldType"
              :danger="errors.first('old_password')"
              label-placeholder="Old Password"
              v-model="old_password"
              data-vv-as="password"
              ref="password"
              icon-pack="feather"
              icon="icon-lock"
              v-validate="'required|min:8'"/>
    <span class="text-danger text-sm">{{ errors.first('old_password') }}</span>

    <vs-input class="w-full mb-base" :type="passwordFieldType"
              :danger="errors.first('new_password')"
              label-placeholder="New Password"
              v-model="new_password"
              name="new_password"
              ref="new_password"
              data-vv-as="password"
              v-validate="'required|min:8'"
              icon-pack="feather"
              icon="icon-lock"/>
    <span class="text-danger text-sm">{{ errors.first('new_password') }}</span>

    <vs-input class="w-full mb-base" :type="passwordFieldType"
              label-placeholder="Confirm Password"
              :danger="errors.first('confirm_password')"
              v-model="confirm_new_password"
              data-vv-as="password"
              v-validate="'min:8|confirmed:new_password'"
              icon-pack="feather"
              name="confirm_password"
              icon="icon-lock"/>
    <span class="text-danger text-sm">{{ errors.first('confirm_password') }}</span>

    <!-- Save & Reset Button -->
    <div class="flex flex-wrap items-center justify-end">
      <vs-button class="ml-auto mt-2" @click="save_changes">Change password</vs-button>
      <!--      <vs-button class="ml-4 mt-2" @click="switchVisibility">show / hide</vs-button>-->
    </div>
  </vx-card>
</template>

<script>
import moduleUserManagement from '@/store/user-management/moduleUserManagement'

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
    },
    validateForm () {
      return !this.errors.any()
    }
  },
  created () {
    if (!moduleUserManagement.isRegistered) {
      this.$store.registerModule('userManagement', moduleUserManagement)
      moduleUserManagement.isRegistered = true
    }
  },
  methods: {
    switchVisibility () {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password'
    },
    save_changes () {
      console.log('exit?', !this.validateForm)
      // if (!this.validateForm) return

      const payload = {
        old_password: this.old_password,
        new_password1: this.new_password,
        new_password2: this.confirm_new_password
      }
      console.log('payload', payload)
      this.$store.dispatch('userManagement/changePassword', payload)
        .then((res) => {
          this.$vs.notify({
            color: 'success',
            title: 'Password changed',
            text: 'Your password was successfully changed'
          })
        })
        .catch((err, res) => {
          console.log('err', err)
          this.$vs.notify({
            color: 'danger',
            title: 'Something went wrong',
            text: err.message
          })
        })

    },
    resetData () {
      this.old_password = ''
      this.new_password = ''
      this.confirm_new_password = ''
    }
  }
}
</script>
