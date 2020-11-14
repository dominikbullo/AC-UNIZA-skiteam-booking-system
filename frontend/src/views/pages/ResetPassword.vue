<template>
  <div class="h-screen flex w-full bg-img">
    <div class="vx-col sm:w-3/5 md:w-3/5 lg:w-3/4 xl:w-3/5 mx-auto self-center">
      <vx-card>
        <div slot="no-body" class="full-page-bg-color">
          <div class="vx-row">
            <div class="vx-col hidden sm:hidden md:hidden lg:block lg:w-1/2 mx-auto self-center">
              <img src="@/assets/images/pages/reset-password.png" alt="login" class="mx-auto">
            </div>
            <div class="vx-col sm:w-full md:w-full lg:w-1/2 mx-auto self-center  d-theme-dark-bg">
              <div class="p-8">
                <div class="vx-card__title mb-8">
                  <h4 class="mb-4">Reset Password</h4>
                  <p>Please enter your new password.</p>
                </div>

                <div class="w-full mb-6">
                  <vs-input
                      :label-placeholder="$t('Password')"
                      :placeholder="$t('Password')"
                      :danger="errors.first('confirm_password')"
                      class="w-full mt-6"
                      name="password"
                      ref="password"
                      type="password"
                      v-model="pass1"
                      v-validate="'required|min:8'"/>
                  <span class="text-danger text-sm">{{ errors.first('password') }}</span>
                </div>

                <div class="w-full mb-6">
                  <vs-input
                      :label-placeholder="$t('Confirm Password')"
                      :placeholder="$t('Confirm Password')"
                      :danger="errors.first('confirm_password')"
                      class="w-full mt-6"
                      data-vv-as="password"
                      name="confirm_password"
                      type="password"
                      v-model="pass2"
                      v-validate="'required|min:8|confirmed:password'"/>
                  <span class="text-danger text-sm">{{ errors.first('confirm_password') }}</span>
                </div>


                <div class="flex flex-wrap justify-between flex-col-reverse sm:flex-row">
                  <vs-button type="border" to="/login" class="w-full sm:w-auto mb-8 sm:mb-auto mt-3 sm:mt-auto">Go
                    Back To Login
                  </vs-button>

                  <vs-button class="w-full sm:w-auto" @click="resetPassword">Reset</vs-button>
                </div>

              </div>
            </div>
          </div>
        </div>
      </vx-card>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    resetPassword () {
      this.$store.dispatch('auth/resetPassword', {
        password: this.pass1,
        token: this.$route.params.token
      }).then(response => {
        console.log('response', response)
        if (response.status === 200) {
          this.$vs.notify({
            title: 'Password reset success',
            text: 'Now you can login with the new password',
            iconPack: 'feather',
            icon: 'icon-alert-circle',
            color: 'success'
          })
          // TODO "You will be redirected to homepage"
          setTimeout(() => {
            this.$router.push({ name: 'page-login' }).catch(() => {})
          }, 3000)
        }
      }).catch(err => {
        console.error(err)
        this.$vs.notify({
          title: err.title,
          text: err.message,
          iconPack: 'feather',
          icon: 'icon-alert-circle',
          color: 'danger'
        })
      })
    }
  },
  data () {
    return {
      pass1: '',
      pass2: '',
      token: this.$route.params.token
    }
  }

}
</script>
