<!--TODO Add gender picker-->
<template>
  <div class="clearfix">
    <div class="vx-row">
      <div class="vx-col sm:w-1/2 w-full mb-2">
        <vs-input
          :label-placeholder="$t('Name')"
          :placeholder="$t('Name')"
          class="w-full mt-6"
          data-vv-validate-on="blur"
          name="name"
          v-model="first_name"
          v-validate="'required|alpha_dash|min:3'"/>
        <span class="text-danger text-sm">{{ errors.first('first_name') }}</span>
      </div>
      <div class="vx-col sm:w-1/2 w-full mb-2">
        <vs-input
          :label-placeholder="$t('Surname')"
          :placeholder="$t('Surname')"
          class="w-full mt-6"
          data-vv-validate-on="blur"
          name="last_name"
          v-model="last_name"
          v-validate="'required|alpha_dash|min:3'"/>
        <span class="text-danger text-sm">{{ errors.first('last_name') }}</span>
      </div>
    </div>

    <vs-input
      :label-placeholder="$t('Email')"
      :placeholder="$t('Email')"
      class="w-full mt-6"
      data-vv-validate-on="blur"
      name="email"
      type="email"
      v-model="email"
      v-validate="'required|email'"/>
    <span class="text-danger text-sm">{{ errors.first('email') }}</span>

    <!-- RES: https://flatpickr.js.org/formatting/ -->
    <label style="font-size: 10px">{{ $t('BirthDate') }}</label>
    <flat-pickr :config="{ dateFormat: 'd.m.Y',maxDate: new Date().fp_incr(14) }" class="w-full"
                v-model="birth_date"/>
    <span class="text-danger text-sm">{{ errors.first('birth_date') }}</span>
    <div>
      <label style="font-size: 10px">{{ $t('Gender') }}</label>
      <div class="demo-alignment mb-base">
        <vs-radio class="mt-2" v-model="gender" vs-value="M">{{ $t('Male') }}</vs-radio>
        <vs-radio class="mt-2" v-model="gender" vs-value="F">{{ $t('Female') }}</vs-radio>
      </div>
    </div>
    <vs-input
      :label-placeholder="$t('Password')"
      :placeholder="$t('Password')"
      class="w-full mt-6"
      data-vv-validate-on="blur"
      name="password"
      ref="password"
      type="password"
      v-model="password"
      v-validate="'required|min:6'"/>
    <span class="text-danger text-sm">{{ errors.first('password') }}</span>

    <vs-input
      :label-placeholder="$t('ConfirmPassword')"
      :placeholder="$t('ConfirmPassword')"
      class="w-full mt-6"
      data-vv-as="password"
      data-vv-validate-on="blur"
      name="confirm_password"
      type="password"
      v-model="confirm_password"
      v-validate="'min:6|confirmed:password'"/>
    <span class="text-danger text-sm">{{ errors.first('confirm_password') }}</span>

    <vs-checkbox class="mt-6" v-model="isTermsConditionAccepted">{{ $t('message.terms_accept') }}.</vs-checkbox>
    <vs-button class="mt-6" to="/login" type="border">{{ $t('Login') }}</vs-button>
    <vs-button :disabled="!validateForm" @click="registerUserDRF" class="float-right mt-6">{{$t('Register')}}
    </vs-button>
  </div>
</template>

<script>

import Datepicker from 'vuejs-datepicker'
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

export default {
  components: {
    Datepicker,
    flatPickr
  },
  data () {
    return {
      first_name: 'DefaultMeno',
      last_name: 'DefaultPriezvisko',
      birth_date: new Date(),
      email: '',
      gender: 'M',
      password: 'testing321',
      confirm_password: 'testing321',
      isTermsConditionAccepted: true
    }
  },
  computed: {
    validateForm () {

      // TODO watch validation
      // return true
      return !this.errors.any()
        && this.first_name !== ''
        && this.last_name !== ''
        && this.birth_date !== ''
        && this.email !== ''
        && this.password !== ''
        && this.confirm_password !== ''
        && this.isTermsConditionAccepted === true
    }
  },
  methods: {
    datepickerClosedFunction () {
      // need to validate
      this.$vs.notify({
        title: 'Datepicker',
        text: this.birth_date,
        iconPack: 'feather',
        icon: 'icon-alert-circle',
        color: 'success'
      })
    },
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
          birth_date: this.birth_date,
          email: this.email,
          gender: this.gender,
          password: this.password,
          confirmPassword: this.confirm_password
        },
        notify: this.$vs.notify
      }

      this.$store.dispatch('auth/registerUserDRF', payload).then(() => {
        this.$vs.loading.close()
      }).catch(error => {
        this.$vs.loading.close()
        //https://stackoverflow.com/questions/29626729/how-to-function-call-using-this-inside-foreach-loop/29626762
        // TODO -> into formu not as notifier

        Object.keys(error.response.data).forEach(function (key) {
          console.log(error.response.data)
          this.$vs.notify({
            title: `Error in ${key}`,
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
