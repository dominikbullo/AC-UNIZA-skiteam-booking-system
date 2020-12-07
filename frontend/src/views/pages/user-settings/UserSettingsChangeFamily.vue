<template>
  <div id="page-user-settings-change-family">
    <vx-card class="mt-5 vx-card"
             title="Generate family token"
             subtitle="You can generate token and sent it to someone. They can then join your family and manage children.">
      <div class="vx-col w-full">
        <vs-input class="vx-col w-full mt-6"
                  :label-placeholder="$t('Generated Family Token')"
                  :placeholder="$t('Generated Family Token')"
                  v-model="generatedToken"/>
        <div class="flex flex-wrap items-center justify-end mt-6">
          <vs-button color="warning" @click="copyText">Generate & Copy</vs-button>
        </div>
      </div>
    </vx-card>
    <vx-card class="mt-5 vx-card"
             title="Add to family"
             subtitle-color="danger"
             subtitle="Insert token from family which you want to join. This action cannot be reverted!">
      <div class="vx-col w-full">
        <vs-input class="vx-col w-full mt-6"
                  :label-placeholder="$t('Family Token')"
                  :placeholder="$t('Insert Family Token')"
                  v-model="token">
        </vs-input>
        <div class="flex flex-wrap items-center justify-end mt-6">
          <vs-button class="ml-auto mt-2" color="danger" @click="save_changes">{{ $t('Change Family') }}</vs-button>
        </div>
      </div>
    </vx-card>
    <!-- RES: https://github.com/lusaxweb/vuesax/issues/611 -->
    <vs-prompt
        @accept="confirmChange"
        title="Merge Family"
        color="warning"
        :active.sync="activePrompt"
        class="custom-width-dialog">
      <div class="vx-row" v-if="this.activePromptData">
        <div class="vx-col sm:w-1/2 w-full">
          <div class="mt-4">
            <ul id="family-change-list-column-1">
              <h4>Family from:</h4>
              <p><b>{{ this.activePromptData.old.name }}</b></p>
              <vs-divider></vs-divider>
              <h4 class="mb-4">Members:</h4>
              <li v-for="item in this.activePromptData.old.members" :key="item.user.id">
                {{ item.user.profile.displayName }}
              </li>
            </ul>
          </div>
        </div>
        <div class="vx-col sm:w-1/2 w-full">
          <div class="mt-4">
            <ul id="family-change-list-column-3">
              <h4> Family to:</h4>
              <p><b>{{ this.activePromptData.new.name }}</b></p>
              <vs-divider></vs-divider>
              <h4 class="mb-4">Members:</h4>
              <li v-for="item in this.activePromptData.new.members" :key="item.user.id">
                {{ item.user.profile.displayName }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </vs-prompt>
  </div>
</template>

<script>

export default {
  data () {
    return {
      activePrompt: false,
      activePromptData: null,
      generatedToken: '',
      token: ''
    }
  },
  methods: {
    confirmChange () {
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: 'Confirm',
        text: 'This action cannot be reverted!',
        accept: this.changeFamily
      })
    },
    changeFamily () {
      this.$store.dispatch('family/changeFamily', this.token).then(() => {
        this.$store.dispatch('userManagement/fetchActiveUser').then(res => {
          console.log('response', res)
          console.log('updated', this.$store.state.AppActiveUser)
          this.$vs.notify({
            time: 10000,
            title: 'Family changed',
            text: 'Your family has been changed!',
            color: 'success'
          })
        })
      }).catch(err => {
        console.log('errerr', err.response.data)
        this.$vs.notify({
          title: 'Error',
          text: 'Something went wrong.',
          color: 'danger',
          iconPack: 'feather',
          icon: 'icon-alert-circle'
        })
      })
    },
    save_changes () {
      // TODO: required token field
      // TODO: show family and information about merge
      this.$store.dispatch('family/getInfoChangeFamily', this.token).then(response => {
        this.activePrompt = true
        this.activePromptData = response.data
      }).catch(err => {
        this.$vs.notify({
          time: 10000,
          title: 'Family not found',
          text: 'Family with this token was not found. The token may have already been used. Please request to generate a new token and you try it again.',
          color: 'danger',
          iconPack: 'feather',
          icon: 'icon-alert-circle'
        })
      })
    },
    getToken () {
      return this.$store.dispatch('family/generateToken', this.$store.getters['familyID']).then(response => {
        console.log('response', response)
        this.generatedToken = response.data.token
      })
    },
    async copyText () {
      await this.getToken()
      this.$copyText(this.generatedToken).then(() => {
        this.$vs.notify({
          title: 'Success',
          text: 'Token copied successfully',
          color: 'success',
          iconPack: 'feather',
          position: 'top-center',
          icon: 'icon-check-circle'
        })
      }, () => {
        this.$vs.notify({
          title: 'Failed',
          text: 'Error in copying text',
          color: 'danger',
          iconPack: 'feather',
          position: 'top-center',
          icon: 'icon-alert-circle'
        })
      })
    }
  }
}
</script>

<style>
.custom-width-dialog .vs-dialog {
  max-width: 650px;
}
</style>
