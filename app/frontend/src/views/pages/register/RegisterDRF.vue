<!--TODO Add gender picker-->
<template>
  <div class="clearfix">
    <vs-input
      v-validate="'required|alpha_dash|min:3'"
      data-vv-validate-on="blur"
      :label-placeholder="$t('Name')"
      name="name"
      :placeholder="$t('Name')"
      v-model="first_name"
      class="w-full mt-6"/>
    <span class="text-danger text-sm">{{ errors.first('first_name') }}</span>

    <vs-input
      v-validate="'required|alpha_dash|min:3'"
      data-vv-validate-on="blur"
      :label-placeholder="$t('Surname')"
      name="last_name"
      :placeholder="$t('Surname')"
      v-model="last_name"
      class="w-full mt-6"/>
    <span class="text-danger text-sm">{{ errors.first('last_name') }}</span>

    <!--    <vs-input-->
    <!--      v-validate="'required|date_format:dd.MM.yyyy'"-->
    <!--      data-vv-validate-on="blur"-->
    <!--      :label-placeholder="$t('BirthDate')"-->
    <!--      name="birth_date"-->
    <!--      :placeholder="$t('BirthDate')"-->
    <!--      v-model="birth_date"-->
    <!--      class="w-full mt-6"/>-->
    <!--    <span class="text-danger text-sm">{{ errors.first('birth_date') }}</span>-->

    <!-- TODO language and format -->
    <datepicker v-model="birth_date"
                name="birth_date"
                class="w-full mt-6"
                z-index="11111"
                :language="sk"
                :label-placeholder="$t('BirthDate')"
                :placeholder="$t('BirthDate')"
                format="dd.MM.yyyy"
                @closed="datepickerClosedFunction">
    </datepicker>
    <span class="text-danger text-sm">{{ errors.first('birth_date') }}</span>

    <vs-input
      v-validate="'required|email'"
      data-vv-validate-on="blur"
      name="email"
      type="email"
      :label-placeholder="$t('Email')"
      :placeholder="$t('Email')"
      v-model="email"
      class="w-full mt-6"/>
    <span class="text-danger text-sm">{{ errors.first('email') }}</span>

    <vs-input
      ref="password"
      type="password"
      data-vv-validate-on="blur"
      v-validate="'required|min:6'"
      name="password"
      :label-placeholder="$t('Password')"
      :placeholder="$t('Password')"
      v-model="password"
      class="w-full mt-6"/>
    <span class="text-danger text-sm">{{ errors.first('password') }}</span>

    <vs-input
      type="password"
      v-validate="'min:6|confirmed:password'"
      data-vv-validate-on="blur"
      data-vv-as="password"
      name="confirm_password"
      :label-placeholder="$t('ConfirmPassword')"
      :placeholder="$t('ConfirmPassword')"
      v-model="confirm_password"
      class="w-full mt-6"/>
    <span class="text-danger text-sm">{{ errors.first('confirm_password') }}</span>

    <vs-checkbox v-model="isTermsConditionAccepted" class="mt-6">{{ $t('message.terms_accept') }}.</vs-checkbox>
    <vs-button type="border" to="/pages/login" class="mt-6">{{ $t('Login') }}</vs-button>
    <vs-button class="float-right mt-6" @click="registerUserDRF" :disabled="!validateForm">{{$t('Register')}}
    </vs-button>
  </div>
</template>

<script>

import Datepicker from 'vuejs-datepicker'

export default {
  components: {
    Datepicker
  },
  data () {
    return {
      first_name: 'DefaultMeno',
      last_name: 'DefaultPriezvisko',
      birth_date: '09.12.1996',
      email: 'admin123@test.sk',
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
