<!-- =========================================================================================
    File Name: Register.vue
    Description: Register Page
    ----------------------------------------------------------------------------------------
    Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
      Author: Pixinvent
    Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->


<template>
  <div class="h-screen flex w-full bg-img vx-row no-gutter items-center justify-center">
    <div class="vx-col sm:w-1/2 md:w-1/2 lg:w-3/4 xl:w-3/5 sm:m-0 m-4">
      <vx-card>
        <div class="full-page-bg-color" slot="no-body">
          <div class="vx-row no-gutter">
            <div class="vx-col hidden sm:hidden md:hidden lg:block lg:w-1/2 mx-auto self-center">
              <img alt="register" class="mx-auto" src="@/assets/images/logo/logo1_medium.png">
            </div>
            <div class="vx-col sm:w-full md:w-full lg:w-1/2 mx-auto self-center  d-theme-dark-bg">
              <div class="px-8 pt-8 register-tabs-container">
                <div class="vx-card__title mb-4">
                  <h4 class="mb-4">{{ $t('CreateAccount') }}</h4>
                  <p>{{ $t('message.register') }}.</p>
                </div>
                <vs-tabs>
                  <vs-tab label="Django">
                    <register-django></register-django>
                  </vs-tab>
                  <vs-tab label="Social">
                    <h1>Not implemented yet</h1>
                  </vs-tab>
                </vs-tabs>
              </div>
            </div>
          </div>
        </div>
      </vx-card>
    </div>
  </div>
</template>

<script>
import RegisterDjango from './RegisterDRF'

export default {
  components: {
    RegisterDjango
  }
}
</script>

<style lang="scss">
  .register-tabs-container {
    min-height: 517px;

    .con-tab {
      padding-bottom: 23px;
    }
  }
</style>
