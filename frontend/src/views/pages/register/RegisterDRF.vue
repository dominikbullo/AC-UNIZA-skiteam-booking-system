<template>
  <div class="clearfix">

    <vs-popup :active.sync="redirect" title="Redirect">
      <vs-progress indeterminate color="primary"></vs-progress>
      <div class="mt-4">
        <h4>You will be redirected to login page in <b>{{ countDown }}</b> second</h4>

        <p class="mt-4">If not you can to it manually
          <router-link tag="a" :to="{ name: 'page-login' }">here</router-link>
        </p>
      </div>
    </vs-popup>

    <div class="vx-row">
      <div class="vx-col sm:w-1/2 w-full mb-2">
        <vs-input
            :label-placeholder="$t('First Name')"
            :placeholder="$t('First Name')"
            :success="!errors.has('first_name') && this.first_name !==''"
            :danger="errors.has('first_name')"
            class="w-full mt-6"
            data-vv-validate-on="blur"
            name="first_name"
            v-model="first_name"
            v-validate="'required|alpha_dash|min:3'"/>
        <span class="text-danger text-sm">{{ errors.first('first_name') }}</span>
      </div>
      <div class="vx-col sm:w-1/2 w-full mb-2">
        <vs-input
            :label-placeholder="$t('Surname')"
            :placeholder="$t('Surname')"
            :success="!errors.has('last_name') && this.last_name !==''"
            :danger="errors.has('last_name')"
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
        :success="!errors.has('email') && this.email !==''"
        :danger="errors.has('email')"
        class="w-full mt-6"
        name="email"
        type="email"
        v-model="email"
        v-validate="'required|email'"/>
    <span class="text-danger text-sm">{{ errors.first('email') }}</span>

    <!-- RES: https://flatpickr.js.org/formatting/ -->
    <div>
      <label style="font-size: .85rem">{{ $t('BirthDate') }}</label>
      <flat-pickr :config="datePickerConfig" class="w-full"
                  v-model="birth_date"/>
      <span class="text-danger text-sm">{{ errors.first('birth_date') }}</span>
    </div>

    <div>
      <label style="font-size: .85rem">{{ $t('Gender') }}</label>
      <div class="demo-alignment mb-base">
        <vs-radio class="mt-2" v-model="gender" vs-value="M">{{ $t('Male') }}</vs-radio>
        <vs-radio class="mt-2" v-model="gender" vs-value="F">{{ $t('Female') }}</vs-radio>
      </div>
    </div>

    <vs-input
        :label-placeholder="$t('Password')"
        :placeholder="$t('Password')"
        :success="!errors.has('confirm_password') && this.password !=='' && this.confirm_password !==''"
        :danger="errors.has('confirm_password')"
        class="w-full mt-6"
        name="password"
        ref="password"
        type="password"
        v-model="password"
        v-validate="'required|min:8'"/>
    <span class="text-danger text-sm">{{ errors.first('password') }}</span>

    <vs-input
        :label-placeholder="$t('Confirm Password')"
        :placeholder="$t('Confirm Password')"
        :success="!errors.has('confirm_password') && this.confirm_password !==''"
        :danger="errors.has('confirm_password')"
        class="w-full mt-6"
        data-vv-as="password"
        name="confirm_password"
        type="password"
        v-model="confirm_password"
        v-validate="'min:8|confirmed:password'"/>
    <span class="text-danger text-sm">{{ errors.first('confirm_password') }}</span>

    <vs-checkbox class="mt-6" v-model="isTermsConditionAccepted">{{ $t('message.terms_accept') }}.</vs-checkbox>
    <vs-button class="mt-6" to="/login" type="border">{{ $t('Login') }}</vs-button>
    <vs-button :disabled="!validateForm" @click="registerUserDRF" class="float-right mt-6">{{
        $t('Register')
      }}
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
      redirect: false,
      countDown: 7,

      first_name: process.env.VUE_APP_NAME || '',
      last_name: process.env.VUE_APP_SURNAME || '',
      birth_date: this.moment().format('YYYY-MM-DD'),
      email: process.env.VUE_APP_LOGIN || '',
      gender: 'M',
      password: process.env.VUE_APP_PASS || '',
      confirm_password: process.env.VUE_APP_PASS || '',
      isTermsConditionAccepted: true,


      datePickerConfig: {
        altFormat: 'd.m.Y',
        altInput: true,
        allowInput: true,
        dateFormat: 'Y-m-d',
        locale: Slovak
      }
    }
  },
  computed: {
    validateForm () {
      return !this.errors.any() &&
          this.first_name !== '' &&
          this.last_name !== '' &&
          this.email !== '' &&
          this.birth_date !== '' &&
          this.gender !== '' &&
          this.password !== '' &&
          this.confirm_password !== ''
    }
  },
  methods: {
    addError (field, msg) {
      this.errors.add({
        field,
        msg
      })
    },
    countDownTimer () {
      this.redirect = true
      if (this.countDown > 0) {
        setTimeout(() => {
          this.countDown -= 1
          this.countDownTimer()
        }, 1000)
      } else {
        this.$router.push({ name: 'page-login' }).catch(() => {})
      }
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
      this.$vs.loading()
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
        this.$vs.loading.close()
        this.$vs.notify({
          color: 'success',
          title: 'Your account was created',
          text: 'Please verify your email before login'
        })
        this.countDownTimer()
      }).catch(error => {
        this.$vs.loading.close()
        console.log(error.response.data)
        // this.errors.add('Email', 'test', 'server')
        for (const [key, value] of Object.entries(error.response.data)) {
          console.log(key, value)
          this.addError(key, value[0])
        }
        this.$vs.notify({
          color: 'danger',
          title: 'Something went wrong',
          text: 'Cannot create your account. Check the fields and try again'
        })
        console.error(error)
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
