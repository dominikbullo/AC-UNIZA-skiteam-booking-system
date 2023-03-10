<template>
  <div>
    <vs-input
        v-validate="'required|min:3'"
        name="email"
        icon-no-border
        icon="icon icon-user"
        icon-pack="feather"
        :label-placeholder="$t('placeholders.email/username')"
        v-model="email"
        class="w-full"/>
    <span class="text-danger text-sm">{{ errors.first('email') }}</span>

    <vs-input
        v-validate="'required|min:6'"
        type="password"
        name="password"
        icon-no-border
        icon="icon icon-lock"
        icon-pack="feather"
        :label-placeholder="$t('Password')"
        v-model="password"
        class="w-full mt-6"/>
    <span class="text-danger text-sm">{{ errors.first('Password') }}</span>

    <div class="flex flex-wrap justify-between my-5">
      <vs-checkbox v-model="checkbox_remember_me" class="mb-3">{{ $t('RememberMe') }}</vs-checkbox>
      <router-link to="/forgot-password">{{ $t('ForgotPassword') }}?</router-link>
    </div>
    <div class="flex flex-wrap justify-between mb-3">
      <vs-button type="border" @click="registerUser">{{ $t('Register') }}</vs-button>
      <vs-button :disabled="!validateForm" @click="loginDRF">{{ $t('Login') }}</vs-button>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      email: process.env.VUE_APP_LOGIN || '',
      password: process.env.VUE_APP_PASS || '',
      checkbox_remember_me: true
    }
  },
  created () {
    // redirect from login if is already logged
    // eslint-disable-next-line no-useless-return
    if (!this.checkLogin()) return
  },
  computed: {
    validateForm () {
      return !this.errors.any()
          && this.email !== ''
          && this.password !== ''
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

        this.$router.push('/').catch(() => {
        })
        return false
      }
      return true
    },
    loginDRF () {
      if (!this.checkLogin()) return

      // Loading
      this.$vs.loading()

      const payload = {
        checkbox_remember_me: this.checkbox_remember_me,
        userDetails: {
          email: this.email,
          password: this.password
        }
      }

      this.$store.dispatch('auth/loginDRF', payload).then((response) => {
        this.$store.dispatch('updateUserRole', {
          aclChangeRole: this.$acl.change,
          userRole: response.data.user.profile.userRole
        })
        // TODO: send parameter to enable prompt or send to another url to add family
        this.$router.push(this.$router.currentRoute.query.to || '/')

        this.$vs.loading.close()
      }).catch(error => {
        this.$vs.loading.close()
        this.$vs.notify({
          title: 'Error',
          text: error.message,
          iconPack: 'feather',
          icon: 'icon-alert-circle',
          color: 'danger'
        })
      })
    },
    registerUser () {
      if (!this.checkLogin()) return
      this.$router.push('/register').catch(() => {
      })
    }
  }
}

</script>

