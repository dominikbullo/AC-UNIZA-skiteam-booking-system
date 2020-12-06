<template>
  <vx-card no-shadow>
    <vs-input class="w-full mt-6"
              :label-placeholder="$t('Old password')"
              :placeholder="$t('Old password')"
              :danger="errors.first('old_password')"
              v-model="old_password"
              data-vv-as="password"
              name="old_password"
              ref="old_password"
              type="password"
              icon-pack="feather"
              icon="icon-lock"
              v-validate="'required|min:8'"/>
    <span class="text-danger text-sm">{{ errors.first('old_password') }}</span>

    <vs-input
      :label-placeholder="$t('New password')"
      :placeholder="$t('New password')"
      :danger="errors.first('confirm_password')"
      class="w-full mt-6"
      name="password"
      data-vv-as="password"
      ref="password"
      type="password"
      icon-pack="feather"
      icon="icon-lock"
      v-model="new_password"
      v-validate="'required|min:8'"/>
    <span class="text-danger text-sm">{{ errors.first('password') }}</span>

    <vs-input
      :label-placeholder="$t('Confirm Password')"
      :placeholder="$t('Confirm Password')"
      :danger="errors.first('confirm_password')"
      data-vv-validate-on="blur"
      class="w-full mt-6"
      data-vv-as="password"
      name="confirm_password"
      type="password"
      icon-pack="feather"
      icon="icon-lock"
      v-model="confirm_new_password"
      v-validate="'min:8|confirmed:password'"/>
    <span class="text-danger text-sm">{{ errors.first('confirm_password') }}</span>


    <!-- Save & Reset Button -->
    <div class="flex flex-wrap items-center justify-end">

      <vs-button class="ml-auto mt-2" @click="save_changes">{{$t('Change Password')}}</vs-button>
      <!--      <vs-button class="ml-4 mt-2" @click="switchVisibility">show / hide</vs-button>-->
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
    },
    validateForm () {
      return !this.errors.any()
    }
  },
  methods: {
    switchVisibility () {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password'
    },
    save_changes () {
      console.log('exit?', !this.validateForm)
      if (!this.validateForm) return

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
