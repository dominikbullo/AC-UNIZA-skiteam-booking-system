<template>
  <div id="event-edit-tab-participants">
    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2">
        <!--        <pre>{{data_local.participants}}</pre>-->
        <!--        <pre>{{data_local}}</pre>-->
        <div class="flex items-end mb-5">
          <span class="leading-none font-medium">Have been logged in to the event</span>
        </div>
        <ul class="centerx">
          <li :key="user.id" class="mb-2" v-for="user in data">
            {{user}}
            <vs-checkbox
              :vs-value="user.username"
              color="success"
              v-model="data_local">
              {{ user.displayName }}
            </vs-checkbox>
          </li>
        </ul>

      </div>
      <div class="vx-col w-full md:w-1/2">
        <div class="flex items-end mb-5">
          <span class="leading-none font-medium">Have't been logged in to the event</span>
        </div>
        <pre>{{data_local}}</pre>

        <!--        <pre>{{data}}</pre>-->
      </div>
    </div>
    <div class="vx-row">
      <div class="vx-col w-full">
        <div class="mt-8 flex flex-wrap items-center justify-end">
          <vs-button :disabled="!validateForm" @click="save_changes" class="ml-auto mt-2">Save Changes</vs-button>
          <vs-button @click="reset_data" class="ml-4 mt-2" color="warning" type="border">Reset</vs-button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import vSelect from 'vue-select'

export default {
  components: {
    vSelect,
    flatPickr
  },
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      data_local: JSON.parse(JSON.stringify(this.data)),

      langOptions: [
        {
          label: 'English',
          value: 'english'
        },
        {
          label: 'Slovak',
          value: 'slovak'
        }
      ]
    }
  },
  computed: {
    validateForm () {
      return !this.errors.any()
    }
  }
}
</script>
