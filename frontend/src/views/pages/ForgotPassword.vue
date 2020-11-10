<template>
  <div class="h-screen flex w-full bg-img">
    <div class="vx-col w-4/5 sm:w-4/5 md:w-3/5 lg:w-3/4 xl:w-3/5 mx-auto self-center">
      <vx-card>
        <div class="full-page-bg-color" slot="no-body">
          <div class="vx-row">
            <div class="vx-col hidden sm:hidden md:hidden lg:block lg:w-1/2 mx-auto self-center">
              <img alt="login" class="mx-auto" src="@/assets/images/pages/forgot-password.png">
            </div>
            <div class="vx-col sm:w-full md:w-full lg:w-1/2 mx-auto self-center d-theme-dark-bg">
              <div class="p-8">
                <div class="vx-card__title mb-8">
                  <h4 class="mb-4">Recover your password</h4>
                  <p>Please enter your email address and we'll send you instructions on how to reset your password.</p>
                </div>

                <div class="w-full mb-8">
                  <vs-input
                      :label-placeholder="$t('Email')"
                      data-vv-validate-on="blur"
                      :placeholder="$t('Email')"
                      :danger="errors.first('Email')"
                      class="w-full mt-6"
                      name="Email"
                      type="email"
                      v-model="email"
                      v-validate="'required|email'"/>
                  <span class="text-danger text-sm">{{ errors.first('Email') }}</span>
                </div>

                <vs-button class="px-4 w-full md:w-auto" to="/login" type="border">Back To Login</vs-button>
                <vs-button class="float-right px-4 w-full md:w-auto mt-3 mb-8 md:mt-0 md:mb-0" @click="recoverPassword">
                  Recover Password
                </vs-button>
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
  data () {
    return {
      email: ''
    }
  },
  methods: {
    recoverPassword () {
      this.$store.dispatch('auth/forgotPassword', this.email).then(response => {
        console.log('response', response)
        if (response.status === 200) {
          this.$vs.notify({
            title: 'Email send!',
            text: 'Check your email to reset password',
            iconPack: 'feather',
            icon: 'icon-alert-circle',
            color: 'success'
          })
          setTimeout(() => {
            this.$router.push({ name: 'page-login' }).catch(() => {})
          }, 3000)
        }
      }).catch(err => {
        console.error(err)
        this.$vs.notify({
          title: 'Error when reseting password',
          text: err.message,
          iconPack: 'feather',
          icon: 'icon-alert-circle',
          color: 'danger'
        })
      }
      )
    }
  }
}
</script>
