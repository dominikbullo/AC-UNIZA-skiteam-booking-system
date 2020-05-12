<!--TODO Add gender picker-->
<template>
  <div class="clearfix">
    <div class="vx-row">
      <div class="vx-col sm:w-1/2 w-full mb-2">
        <vs-input
          :label-placeholder="$t('First Name')"
          :placeholder="$t('First Name')"
          :success="!errors.first('Name') && this.first_name !==''"
          :danger="errors.first('Name')"
          class="w-full mt-6"
          data-vv-validate-on="blur"
          name="Name"
          v-model="first_name"
          v-validate="'required|alpha_dash|min:3'"/>
        <span class="text-danger text-sm">{{ errors.first('Name') }}</span>
      </div>
      <div class="vx-col sm:w-1/2 w-full mb-2">
        <vs-input
          :label-placeholder="$t('Surname')"
          :placeholder="$t('Surname')"
          :success="!errors.first('Surname') && this.last_name !==''"
          :danger="errors.first('Surname')"
          class="w-full mt-6"
          data-vv-validate-on="blur"
          name="Surname"
          v-model="last_name"
          v-validate="'required|alpha_dash|min:3'"/>
        <span class="text-danger text-sm">{{ errors.first('Surname') }}</span>
      </div>
    </div>

    <vs-input
      :label-placeholder="$t('Email')"
      :placeholder="$t('Email')"
      :success="!errors.first('Email') && this.email !==''"
      :danger="errors.first('Email')"
      class="w-full mt-6"
      name="Email"
      type="email"
      v-model="email"
      v-validate="'required|email'"/>
    <span class="text-danger text-sm">{{ errors.first('Email') }}</span>

    <!-- RES: https://flatpickr.js.org/formatting/ -->
    <div>
      <label style="font-size: 10px">{{ $t('BirthDate') }}</label>
      <flat-pickr :config="datePickerConfig" class="w-full"
                  v-model="birth_date"/>
      <span class="text-danger text-sm">{{ errors.first('birth_date') }}</span>
    </div>

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
      :success="!errors.first('confirm_password') && this.password !=='' && this.confirm_password !==''"
      :danger="errors.first('confirm_password')"
      class="w-full mt-6"
      name="password"
      ref="password"
      type="password"
      v-model="password"
      v-validate="'required|min:8'"/>
    <span class="text-danger text-sm">{{ errors.first('password') }}</span>

    <vs-input
      :label-placeholder="$t('ConfirmPassword')"
      :placeholder="$t('ConfirmPassword')"
      :success="!errors.first('confirm_password') && this.confirm_password !==''"
      :danger="errors.first('confirm_password')"
      class="w-full mt-6"
      data-vv-as="password"
      name="confirm_password"
      type="password"
      v-model="confirm_password"
      v-validate="'min:8|confirmed:password'"/>
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
import { Slovak } from 'flatpickr/dist/l10n/sk.js'

export default {
  components: {
    Datepicker,
    flatPickr
  },
  data () {
    return {
      first_name: 'DefaultMeno',
      last_name: 'DefaultPriezvisko',
      birth_date: this.moment().format('YYYY-MM-DD'),
      email: 'totojetes@sasd.sk',
      gender: 'M',
      password: 'testing321',
      confirm_password: 'testing321',
      isTermsConditionAccepted: true,


      datePickerConfig: {
        altFormat: 'd.m.Y',
        altInput: true,
        dateFormat: 'Y-m-d',
        locale: Slovak
      }
    }
  },
  computed: {
    validateForm () {
      // TODO watch validation
      // return true
      return !this.errors.any() &&
        this.first_name !== '' &&
        this.last_name !== '' &&
        this.email !== '' &&
        this.birth_date !== '' &&
        this.gender !== '' &&
        this.password !== '' &&
        this.confirm_password !== '' &&
        this.isTermsConditionAccepted === true
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
          user_role: 'parent',
          birth_date: this.birth_date,
          email: this.email,
          gender: this.gender,
          password: this.password,
          confirmPassword: this.confirm_password
        },
        notify: this.$vs.notify
      }

      this.$store.dispatch('auth/registerUserDRF', payload).then((response) => {
        this.$router.push(this.$router.currentRoute.query.to || '/')
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

<style>
  .flatpickr-input[type="hidden"] + input {
    color: #c2c6dc;
  }
</style>
