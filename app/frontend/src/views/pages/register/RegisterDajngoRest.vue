<template>
  <div class="clearfix">
    <vs-input
      v-validate="'required|alpha_dash|min:3'"
      data-vv-validate-on="blur"
      label-placeholder="Meno"
      name="name"
      placeholder="Meno"
      v-model="first_name"
      class="w-full"/>
    <span class="text-danger text-sm">{{ errors.first('displayName') }}</span>

    <vs-input
      v-validate="'required|alpha_dash|min:3'"
      data-vv-validate-on="blur"
      label-placeholder="Priezvisko"
      name="last_name"
      placeholder="Priezvisko"
      v-model="last_name"
      class="w-full"/>
    <span class="text-danger text-sm">{{ errors.first('displayName') }}</span>

    <vs-input
      v-validate="'required|email'"
      data-vv-validate-on="blur"
      name="email"
      type="email"
      label-placeholder="Email"
      placeholder="Email"
      v-model="email"
      class="w-full mt-6"/>
    <span class="text-danger text-sm">{{ errors.first('email') }}</span>

    <vs-input
      ref="password"
      type="password"
      data-vv-validate-on="blur"
      v-validate="'required|min:6'"
      name="password"
      label-placeholder="Heslo"
      placeholder="Heslo"
      v-model="password"
      class="w-full mt-6"/>
    <span class="text-danger text-sm">{{ errors.first('password') }}</span>

    <vs-input
      type="password"
      v-validate="'min:6|confirmed:password'"
      data-vv-validate-on="blur"
      data-vv-as="password"
      name="confirm_password"
      label-placeholder="Potvrdiť heslo"
      placeholder="Confirm Password"
      v-model="confirm_password"
      class="w-full mt-6"/>
    <span class="text-danger text-sm">{{ errors.first('confirm_password') }}</span>

    <vs-checkbox v-model="isTermsConditionAccepted" class="mt-6">I accept the terms & conditions.</vs-checkbox>
    <vs-button type="border" to="/pages/login" class="mt-6">Login</vs-button>
    <vs-button class="float-right mt-6" @click="registerUserDRF" :disabled="!validateForm">Register</vs-button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      first_name: 'DefaultMeno',
      last_name: 'DefaultPriezvisko',
      email: 'admin123@test.sk',
      password: 'testing321',
      confirm_password: 'testing321',
      isTermsConditionAccepted: true
    }
  },
  computed: {
    validateForm () {
      // TODO validate
      return true
      // return !this.errors.any()
      //   && this.displayName !== ''
      //   && this.email !== ''
      //   && this.password !== ''
      //   && this.confirm_password !== ''
      //   && this.isTermsConditionAccepted === true
    }
  },
  methods: {
    checkLogin () {
      // If user is already logged in notify
      if (this.$store.state.auth.isUserLoggedIn()) {

        // Close animation if passed as payload
        // this.$vs.loading.close()

        this.$vs.notify({
          title: 'Login Attempt',
          text: 'You are already logged in!',
          iconPack: 'feather',
          icon: 'icon-alert-circle',
          color: 'warning'
        })

        return false
      }
      return true
    },
    registerUserDRF () {
      // If form is not validated or user is already login return
      if (!this.validateForm || !this.checkLogin()) return

      const payload = {
        userDetails: {
          first_name: this.first_name,
          last_name: this.last_name,
          email: this.email,
          password: this.password,
          confirmPassword: this.confirm_password
        },
        notify: this.$vs.notify
      }

      this.$store.dispatch('auth/registerUserDRF', payload).then(() => {
        this.$vs.loading.close()
      }).catch(error => {
        this.$vs.loading.close()
        // for every error in error notify
        // console.log('maybeeeeeeeeee3', error.response.data)

        // TODO -> into formular not as notifyier
        //https://stackoverflow.com/questions/29626729/how-to-function-call-using-this-inside-foreach-loop/29626762
        Object.keys(error.response.data).forEach(function (key) {
          this.$vs.notify({
            title: 'Error',
            text: error.response.data[key][0],
            iconPack: 'feather',
            icon: 'icon-alert-circle',
            color: 'danger'
          })
        }, this)
      })
    }
  }
}
</script>
