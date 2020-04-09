<template>
  <div>
    <vs-prompt
      :bind="activePrompt"
      :is-valid="validateForm"
      @accept="addChild"
      @cancel="closeComponent"
      @close="closeComponent"
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
                  <span class="text-danger text-sm">{{ errors.first('childData.first_name') }}</span>
                </div>

                <div class="vx-col sm:w-1/2 w-full mb-2">
                  <vs-input
                    :label-placeholder="$t('Surname')"
                    :placeholder="$t('Surname')"
                    class="w-full mt-6"
                    data-vv-validate-on="blur"
                    name="email"
                    type="text"
                    v-model="childData.last_name"
                    v-validate="'required|alpha_dash|min:3'"/>
                  <span class="text-danger text-sm">{{ errors.first('childData.first_name') }}</span>
                </div>
              </div>

              <vs-input
                :label-placeholder="$t('Username')"
                :placeholder="$t('Username')"
                class="w-full mt-6"
                data-vv-validate-on="blur"
                name="email"
                type="text"
                v-model="childData.username"
                v-validate="'required|alpha_dash|min:3'"/>
              <span class="text-danger text-sm">{{ errors.first('childData.first_name') }}</span>

              <vs-input
                :label-placeholder="$t('Email')"
                :placeholder="$t('Email')"
                class="w-full mt-6"
                data-vv-validate-on="blur"
                name="email"
                type="email"
                v-model="childData.email"
                v-validate="'email'"/>
              <span class="text-danger text-sm">{{ errors.first('childData.email') }}</span>


              <!-- RES: https://flatpickr.js.org/formatting/ -->
              <label style="font-size: 10px">{{ $t('BirthDate') }}</label>
              <flat-pickr :config="{ dateFormat: 'd.m.Y',maxDate: new Date().fp_incr(14) }" class="w-full"
                          v-model="childData.birth_date"/>
              <span class="text-danger text-sm">{{ errors.first('childData.birth_date') }}</span>

              <vs-input
                :label-placeholder="$t('Password')"
                :placeholder="$t('Password')"
                class="w-full mt-6"
                data-vv-validate-on="blur"
                name="password"
                ref="password"
                type="password"
                v-model="childData.password"
                v-validate="'required|min:6'"/>
              <span class="text-danger text-sm">{{ errors.first('childData.password') }}</span>

              <vs-input
                :label-placeholder="$t('ConfirmPassword')"
                :placeholder="$t('ConfirmPassword')"
                class="w-full mt-6"
                data-vv-as="password"
                data-vv-validate-on="blur"
                name="confirm_password"
                type="password"
                v-model="childData.confirm_password"
                v-validate="'min:6|confirmed:password'"/>
              <span class="text-danger text-sm">{{ errors.first('childData.confirm_password') }}</span>
            </div>
          </div>

        </form>
      </div>
    </vs-prompt>
  </div>
</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

export default {
  name: 'FamilySettingsAddNew',
  props: {
    activePrompt: {
      type: Boolean,
      required: true
    }
  },
  components: {
    flatPickr
  },
  data () {
    return {
      email: '',
      userRole: this.$acl.get[0],

      childData: {
        username: '',
        email: '',
        password: '',
        confirm_password: '',
        first_name: '',
        last_name: '',
        birth_date: new Date(),
        phone_number: '',
        location: '',
        gender: ''
      }
    }
  },
  computed: {
    validateForm () {
      return !this.errors.any()
    },
    computed: {
      modalProp: {
        get () {
          return this.modal
        },
        set (val) {
          this.$emit('update:activePrompt', val)
        }
      }
    }
  },
  methods: {
    clearFields () {
      Object.assign(this.childData, {
        username: '',
        email: '',
        password: '',
        confirm_password: '',
        first_name: '',
        last_name: '',
        birth_date: new Date(),
        phone_number: '',
        location: '',
        gender: ''
      })
    },
    addChild () {
      // if (!this.this.$validator.validateAll() || this.checkLogin())
      this.$validator.validateAll().then(result => {
        if (result) {
          this.$vs.loading.open()
          this.$store.dispatch('family/addChild', Object.assign({}, this.childData)).then(() => {
            this.$vs.loading.close()
            this.clearFields()

            this.$vs.notify({
              color: 'success',
              title: 'User Added',
              text: 'User was created successfully'
            })
          }).catch(error => {
            this.$vs.loading.close()
            console.log('tototo je error', error)

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
      })
    },
    closeComponent () {
      // RES: https://vuejs.org/v2/guide/components-custom-events.html#sync-Modifier
      this.activePrompt = false
    }
  }
}
</script>

<style scoped>

</style>
