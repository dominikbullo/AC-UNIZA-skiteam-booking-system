<template>
  <div id="test_page">

    <vx-card>
      <h1>That's the dashboard!</h1>
      <p>You should only get here if you're authenticated!</p>
      <p>Your email address: {{ email }}</p>

      <!--  Roles  -->
      <p>Your current role is <strong>{{ $acl.get[0] }}</strong>.</p>

      <div class="demo-alignment mb-base">
        <vs-radio v-model="userRole" vs-value="editor">Editor</vs-radio>
        <vs-radio v-model="userRole" vs-value="admin">Admin</vs-radio>
      </div>

      <vx-card card-border code-toggler no-shadow title="Buttons">
        <div class="demo-alignment">

          <vs-button @click="activePrompt = true" icon="icon-plus" icon-pack="feather" v-show="$acl.check('editor')">{{
            $t('AddChild') }}
          </vs-button>

          <vs-prompt
            :active.sync="activePrompt"
            :is-valid="validateForm"
            @accept="addChild"
            @cancel="clearFields"
            @close="close"
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

          <vs-button @click="addEvent"
                     icon="icon-plus"
                     icon-pack="feather"
                     v-show="$acl.check('admin')"> {{ $t('AddEvent') }}
          </vs-button>

          <vs-button
            @click="askPermission"
            icon="icon-plus"
            icon-pack="feather"
            if="notificationsSupported">{{
            $t('Enable notifications') }}
          </vs-button>


        </div>
      </vx-card>


    </vx-card>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

export default {
  components: {
    flatPickr
  },
  data () {
    return {
      email: '',
      userRole: this.$acl.get[0],
      activePrompt: false,
      notificationsSupported: false,

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
    }
  },
  watch: {
    userRole (val) {
      this.$store.dispatch('updateUserRole', {
        aclChangeRole: this.$acl.change,
        userRole: val
      })
    }
  },
  created () {
    // TODO via local data
    this.$http.get('/rest-auth/user/').then(res => {
      console.log(res.data)
      this.email = res.data.email
    }).catch(error => console.log(error))

    if ('Notification' in window && 'serviceWorker' in navigator) {
      this.notificationsSupported = true
    }
  },
  methods: {
    clearFields () {
      Object.assign(this.childData, {
        title: '',
        desc: '',
        isCompleted: false,
        isImportant: false,
        isStarred: false,
        tags: []
      })
    },
    addTodo () {
      this.$validator.validateAll().then(result => {
        if (result) {
          this.$store.dispatch('todo/addTask', Object.assign({}, this.childData))
          this.clearFields()
        }
      })
    },
    addChild () {
      this.$validator.validateAll().then(result => {
        if (result) {
          this.$store.dispatch('family/addChild', Object.assign({}, this.childData))
          this.clearFields()
        }
      })
    },
    addEvent () {
      this.$vs.notify({
        title: 'Child',
        text: 'Yeah you want to add child - not implemented yet'
      })
    },
    askPermission () {
      if (this.notificationsSupported) {
        Notification.requestPermission(result => {
          console.log('result from permission question', result)
          if (result !== 'granted') {
            alert('You probably do not like notifications?!')
          } else {
            console.log('A notification will be send from the service worker => This only works in production')
            this.showNotification()
          }
        })
      }
    },
    showNotification () {
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.ready // returns a Promise, the active SW registration
          .then(swreg => swreg.showNotification('Notifications granted', {
            body: 'Here is a first notification',
            icon: '/img/icons/android-chrome-192x192.png',
            image: '/img/autumn-forest.png',
            vibrate: [300, 200, 300],
            badge: '/img/icons/plint-badge-96x96.png'
            // actions: [
            //     { action: 'confirm', title: 'Okay', icon: '/img/icons/android-chrome-192x192.png'},
            //     { action: 'cancel', title: 'Cancel', icon: '/img/icons/android-chrome-192x192.png'}
            // ],
          }))
      }
    }
  }
}
</script>

<style scoped>
  h1, p {
    text-align: center;
  }

  p {
    color: red;
  }
</style>
