<template>
  <div id="page-family-list">
    <!-- TODO: isPromptActiveLocal because mutating prompt-->
    <vs-prompt
        :active.sync="isPromptActiveLocal"
        @accept="addChild"
        accept-text="Add Child"
        button-cancel="border"
        title="Add Child">
      <div>
        <form>
          <div class="vx-row">
            <div class="vx-col w-full">

              <!-- Name & Surname in one row -->
              <div class="vx-row">
                <div class="vx-col sm:w-1/2 w-full mb-2">
                  <vs-input
                      :label-placeholder="$t('Name')"
                      :placeholder="$t('Name')"
                      class="w-full mt-6"
                      data-vv-validate-on="blur"
                      name="name"
                      type="text"
                      v-model="childData.first_name"
                      v-validate="'required|alpha_dash|min:3'"/>
                  <span class="text-danger text-sm">{{ errors.first('name') }}</span>
                </div>

                <div class="vx-col sm:w-1/2 w-full mb-2">
                  <vs-input
                      :label-placeholder="$t('Surname')"
                      :placeholder="$t('Surname')"
                      class="w-full mt-6"
                      data-vv-validate-on="blur"
                      name="surname"
                      type="text"
                      v-model="childData.last_name"
                      v-validate="'required|alpha_dash|min:3'"/>
                  <span class="text-danger text-sm">{{ errors.first('surname') }}</span>
                </div>
              </div>

              <vs-input
                  :label-placeholder="$t('Email')"
                  :placeholder="$t('Email')"
                  class="w-full mt-6"
                  data-vv-validate-on="blur"
                  name="email"
                  type="email"
                  v-model="childData.email"
                  v-validate="'email'"/>
              <span class="text-danger text-sm">{{ errors.first('email') }}</span>


              <!-- RES: https://flatpickr.js.org/formatting/ -->
              <div>
                <label style="font-size: .85rem">{{ $t('BirthDate') }}</label>
                <flat-pickr :config="datePickerConfig" class="w-full"
                            v-model="childData.profile.birth_date"/>
                <span class="text-danger text-sm">{{ errors.first('birth_date') }}</span>
              </div>

              <div>
                <label style="font-size: .85rem">{{ $t('Gender') }}</label>
                <div class="demo-alignment mb-base">
                  <vs-radio class="mt-2" v-model="childData.profile.gender" vs-value="M">{{ $t('Male') }}
                  </vs-radio>
                  <vs-radio class="mt-2" v-model="childData.profile.gender" vs-value="F">{{ $t('Female') }}
                  </vs-radio>
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
                  v-model="childData.password1"
                  v-validate="'required|min:6'"/>
              <span class="text-danger text-sm">{{ errors.first('password1') }}</span>

              <vs-input
                  :label-placeholder="$t('ConfirmPassword')"
                  :placeholder="$t('ConfirmPassword')"
                  class="w-full mt-6"
                  data-vv-as="password"
                  data-vv-validate-on="blur"
                  name="confirm_password"
                  type="password"
                  v-model="childData.password2"
                  v-validate="'min:6|confirmed:password'"/>
              <span class="text-danger text-sm">{{ errors.first('confirm_password') }}</span>
            </div>
          </div>

        </form>
      </div>
    </vs-prompt>

  </div>
</template>

<script>
import '@/assets/scss/vuexy/extraComponents/agGridStyleOverride.scss'
import vSelect from 'vue-select'

import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { Slovak } from 'flatpickr/dist/l10n/sk.js'


export default {
  props: {
    isPromptActive: {
      type: Boolean,
      required: true
    }
  },
  components: {
    flatPickr,
    vSelect
  },
  data () {
    return {
      childData: {
        first_name: '',
        last_name: '',
        email: '.',
        password1: '',
        password2: '',
        profile: {
          birth_date: this.moment().format('YYYY-MM-DD'),
          gender: 'M'
        }
      },

      datePickerConfig: {
        altFormat: 'd.m.Y',
        altInput: true,
        dateFormat: 'Y-m-d',
        locale: Slovak
      }
    }
  },
  watch: {
    isPromptActive (val) {
      if (!val) return
      this.initValues()
    }
  },
  computed: {
    isPromptActiveLocal: {
      get () {
        return this.isPromptActive
      },
      set (val) {
        if (!val) {
          this.$emit('closePrompt')
          this.$validator.reset()
          this.initValues()
        }
      }
    }
  },
  methods: {
    initValues () {
      Object.assign(this.childData, {
        email: '',
        password1: '',
        password2: '',
        first_name: '',
        last_name: '',
        profile: {
          birth_date: this.moment().format('DD.MM.YYYY'),
          gender: 'M'
        }
      })
    },
    addChild () {
      // TODO: validate
      this.$store.dispatch('family/addChild', Object.assign({}, this.childData))
        .then(() => {
          this.$vs.notify({
            color: 'success',
            title: 'Child Added',
            text: 'The child was successfully added'
          })
          this.initValues()
        })
        .catch(err => {
          // close and open again
          this.$emit('closePrompt', true)
          this.multipleNotify(err.response.data)
        })
    },
    // RES: https://stackoverflow.com/questions/29516136/how-to-print-all-values-of-a-nested-object
    // TODO: Global component!
    // TODO: Match error with field
    multipleNotify (obj) {
      for (const [key, value] of Object.entries(obj)) {
        if (typeof value === 'object' && !(value instanceof Array)) {
          this.multipleNotify(value)
        } else {
          this.$vs.notify({
            title: `Child NOT created. Error in ${key}`,
            text: value.join(),
            iconPack: 'feather',
            icon: 'icon-alert-circle',
            color: 'danger'
          })
        }
      }
    }
  },
  created () {
    this.$store.dispatch('family/fetchFamily', this.$store.state.AppActiveUser.profile.family_id)
  }
}
</script>
