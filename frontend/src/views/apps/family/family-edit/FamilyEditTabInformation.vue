<template>
  <div id="family-edit-tab-info">
    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2">
        <!-- Col Header -->
        <div class="flex items-end">
          <feather-icon icon="UserIcon" class="mr-2" svgClasses="w-5 h-5"/>
          <span class="leading-none font-medium">Personal Information</span>
        </div>

        <!-- Col Content -->
        <div>

          <!-- DOB -->
          <div class="mt-4">
            <label class="text-sm">Birth Date</label>
            <flat-pickr v-model="data_local.dob"
                        :config="{ dateFormat: 'd F Y', maxDate: new Date() }" class="w-full"
                        v-validate="'required'" name="dob"/>
            <span class="text-danger text-sm" v-show="errors.has('dob')">{{ errors.first('dob') }}</span>
          </div>

          <vs-input class="w-full mt-4" label="Mobile" v-model="data_local.mobile"
                    v-validate="{regex: '^\\+?([0-9]+)$' }" name="mobile"/>
          <span class="text-danger text-sm" v-show="errors.has('mobile')">{{ errors.first('mobile') }}</span>

          <vs-input class="w-full mt-4" label="Website" v-model="data_local.website" v-validate="'url:require_protocol'"
                    name="website" data-vv-as="field"/>
          <span class="text-danger text-sm" v-show="errors.has('website')">{{ errors.first('website') }}</span>

          <div class="mt-4">
            <label class="text-sm">Languages</label>
            <v-select v-model="data_local.languages_known" multiple :closeOnSelect="false" :options="langOptions"
                      v-validate="'required'" name="lang_known" :dir="$vs.rtl ? 'rtl' : 'ltr'"/>
            <span class="text-danger text-sm" v-show="errors.has('lang_known')">{{ errors.first('lang_known') }}</span>
          </div>

        </div>
      </div>

      <!-- Address Col -->
      <div class="vx-col w-full md:w-1/2">

        <!-- Col Header -->
        <div class="flex items-end md:mt-0 mt-base">
          <feather-icon icon="MapPinIcon" class="mr-2" svgClasses="w-5 h-5"/>
          <span class="leading-none font-medium">Address</span>
        </div>

        <!--        &lt;!&ndash; Col Content &ndash;&gt;-->
        <!--        <div>-->
        <!--          <vs-input class="w-full mt-4" label="Address Line 1" v-model="data_local.location.add_line_1"-->
        <!--                    v-validate="'required'" name="addd_line_1"/>-->
        <!--          <span class="text-danger text-sm" v-show="errors.has('addd_line_1')">{{ errors.first('addd_line_1') }}</span>-->

        <!--          <vs-input class="w-full mt-4" label="Address Line 2" v-model="data_local.location.add_line_2"/>-->

        <!--          <vs-input class="w-full mt-4" label="Post Code" v-model="data_local.location.post_code"-->
        <!--                    v-validate="'required|numeric'" name="post_code"/>-->
        <!--          <span class="text-danger text-sm" v-show="errors.has('post_code')">{{ errors.first('post_code') }}</span>-->

        <!--          <vs-input class="w-full mt-4" label="City" v-model="data_local.location.city" v-validate="'required|alpha'"-->
        <!--                    name="city"/>-->
        <!--          <span class="text-danger text-sm" v-show="errors.has('city')">{{ errors.first('city') }}</span>-->

        <!--          <vs-input class="w-full mt-4" label="State" v-model="data_local.location.state" v-validate="'required|alpha'"-->
        <!--                    name="state"/>-->
        <!--          <span class="text-danger text-sm" v-show="errors.has('state')">{{ errors.first('state') }}</span>-->

        <!--          <vs-input class="w-full mt-4" label="Country" v-model="data_local.location.country"-->
        <!--                    v-validate="'required|alpha'" name="country"/>-->
        <!--          <span class="text-danger text-sm" v-show="errors.has('country')">{{ errors.first('country') }}</span>-->

        <!--        </div>-->
      </div>
    </div>

    <!-- Save & Reset Button -->
    <div class="vx-row">
      <div class="vx-col w-full">
        <div class="mt-8 flex flex-wrap items-center justify-end">
          <vs-button class="ml-auto mt-2" @click="save_changes" :disabled="!validateForm">Save Changes</vs-button>
          <vs-button class="ml-4 mt-2" type="border" color="warning" @click="reset_data">Reset</vs-button>
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
  },
  methods: {
    save_changes () {
      /* eslint-disable */
      if (!this.validateForm) return

      throw new Error('saveData - Not implemented yet!')
      this.$store.dispatch('editUser', this.data_local)
    },
    reset_data () {
      this.data_local = Object.assign({}, this.data)
    }
  }
}
</script>
