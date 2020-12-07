<template>
  <div class="h-screen flex w-full bg-img vx-row no-gutter items-center justify-center" id="page-login">
    <div class="vx-col sm:w-1/2 md:w-1/2 lg:w-3/4 xl:w-3/5 sm:m-0 m-4">
      <vx-card>
        <div slot="no-body" class="full-page-bg-color">

          <div class="vx-row no-gutter justify-center items-center">

            <div class="vx-col hidden lg:block lg:w-1/2">
              <img src="@/assets/images/logo/logo1_medium.png" alt="login" class="mx-auto">
            </div>

            <div class="vx-col sm:w-full md:w-full lg:w-1/2 d-theme-dark-bg ">
              <div class="p-8 items-center">
                <div class="vx-card__title mb-8">
                  <h4 class="mb-4">{{ $t('Login') }}</h4>
                  <p>{{ $t('message.login') }}.</p>
                </div>
                <login-d-r-f></login-d-r-f>
              </div>
            </div>
          </div>
        </div>
      </vx-card>
    </div>
  </div>
</template>


<script>
import LoginDRF from './LoginDRF.vue'

export default {
  components: {
    LoginDRF
  },
  props: {
    info: {
      type: String,
      default: ''
    }
  },
  created () {
    if (this.$route.params.info) {
      if (this.$route.params.info === 'success') {
        this.$vs.notify({
          color: 'success',
          title: 'Email verified',
          text: 'Your email was successfully verified! Now you can log in.'
        })
      } else {
        this.$vs.notify({
          color: 'danger',
          title: 'Cannot verify your email',
          text: 'We are sorry. Something went wrong when verifying your email. Please try again or contact administrator.'
        })
      }
      this.$router.push({ name: 'page-login' }).catch(() => {})
    }
  }
}
</script>

<style lang="scss">
  .login-tabs-container {
    min-height: 505px;

    .con-tab {
      padding-bottom: 14px;
    }

    .con-slot-tabs {
      margin-top: 1rem;
    }
  }
</style>
