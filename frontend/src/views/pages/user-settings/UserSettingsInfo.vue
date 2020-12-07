<template>
  <vx-card no-shadow>

    <!-- Bio -->
    <!--    <vs-textarea label="Bio" v-model="bio" placeholder="Your bio..."/>-->
    <div>
      <label style="font-size: .85rem">{{ $t('BirthDate') }}</label>
      <flat-pickr :config="datePickerConfig" class="w-full"
                  v-model="birth_date"/>
      <span class="text-danger text-sm">{{ errors.first('birth_date') }}</span>
    </div>

    <!-- Mobile Number -->
    <vs-input class="w-full mt-8" type="phone_number" label-placeholder="Mobile" v-model="phone_number"/>

    <!-- Gender -->
    <div class="mt-8 mb-base">
      <label class="text-sm">Gender</label>
      <div class="mt-2">
        <vs-radio v-model="gender" vs-value="Male" class="mr-4">Male</vs-radio>
        <vs-radio v-model="gender" vs-value="Female" class="mr-4">Female</vs-radio>
      </div>
    </div>

    <!-- Save & Reset Button -->
    <div class="flex flex-wrap items-center justify-end">
      <vs-button class="ml-auto mt-2" @click="save_changes">{{ $t('Save Changes') }}</vs-button>
      <vs-button class="ml-4 mt-2" type="border" color="warning" @click="reset_data">{{ $t('Reset') }}</vs-button>
    </div>
  </vx-card>
</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { Slovak } from 'flatpickr/dist/l10n/sk.js'


export default {
  components: {
    flatPickr
  },
  data () {
    return {
      datePickerConfig: {
        altFormat: 'd.m.Y',
        altInput: true,
        locale: Slovak
      },
      birth_date: null,
      gender: 'M',
      phone_number: ''
    }
  },
  created () {
    this.reset_data()
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
      this.birth_date = this.$store.state.AppActiveUser.birth_date
      this.gender = this.$store.state.AppActiveUser.gender
      this.phone_number = this.$store.state.AppActiveUser.phone_number
    },
    save_changes () {
      if (!this.validateForm) return

      const payload = {
        birth_date: this.birth_date,
        phone_number: this.phone_number,
        gender: this.gender
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
