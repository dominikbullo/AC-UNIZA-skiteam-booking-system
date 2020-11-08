<!-- =========================================================================================
  File Name: AddNewDataSidebar.vue
  Description: Add New Data - Sidebar component
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->


<template>
  <vs-sidebar click-not-close position-right parent="body" default-index="1" color="primary"
              class="add-new-data-sidebar items-no-padding" spacer v-model="isSidebarActiveLocal">
    <div class="mt-6 flex items-center justify-between px-6">
      <h4>{{ Object.entries(this.data).length === 0 ? 'ADD NEW' : 'UPDATE' }} {{ 'accommodation' | uppercase }}</h4>
      <feather-icon icon="XIcon" @click.stop="isSidebarActiveLocal = false" class="cursor-pointer"></feather-icon>
    </div>
    <vs-divider class="mb-0"></vs-divider>

    <component :is="scrollbarTag" class="scroll-area--data-list-add-new" :settings="settings" :key="$vs.rtl">

      <div class="p-6">

        <!-- FROM -->
        <div class="mt-4">
          <label class="text-sm">{{ $t('From') }}</label>
          <flat-pickr v-model="dataStart"
                      :config="datePickerConfig"
                      class="w-full"
                      v-validate="'required'"
                      name="start"/>
          <span class="text-danger text-sm" v-show="errors.has('start')">{{ errors.first('start') }}</span>
        </div>

        <!-- TO -->
        <div class="mt-4">
          <label class="text-sm">{{ $t('To') }}</label>
          <flat-pickr v-model="dataEnd"
                      :config="datePickerConfig"
                      class="w-full"
                      v-validate="'required'"
                      name="start"/>
          <span class="text-danger text-sm" v-show="errors.has('start')">{{ errors.first('start') }}</span>
        </div>

        <!-- Name -->
        <vs-input label="Name" v-model="dataName" class="mt-5 w-full" name="item-name" v-validate="'required'"/>
        <span class="text-danger text-sm" v-show="errors.has('item-name')">{{ errors.first('item-name') }}</span>

        <!-- URL -->
        <vs-input label="URL" v-model="dataURL" class="mt-5 w-full" name="item-name" v-validate="'required'"/>
        <span class="text-danger text-sm" v-show="errors.has('item-name')">{{ errors.first('item-name') }}</span>

        <!-- ORDER STATUS -->
        <vs-select v-model="dataOrder_status" label="Status" class="mt-5 w-full">
          <vs-select-item :key="item.value" :value="item.value" :text="item.text" v-for="item in order_status_choices"/>
        </vs-select>

        <!-- PRICE -->
        <div class="mt-5 w-full vx-row">
          <vs-input
              icon="euro"
              icon-after
              label="Price"
              v-model="dataPrice"
              class="vx-col w-3/4"
              v-validate="{ required: true, regex: /\d+(\.\d+)?$/ }"
              name="item-price"/>
          <p class="vx-col w-1/4 pl-5 mt-8">/ night</p>
        </div>
        <span class="text-danger text-sm" v-show="errors.has('item-price')">{{ errors.first('item-price') }}</span>

        <div class="mt-5 w-full">
          <label style="font-size: .85rem;">{{ $t('AditionalInfo') }}</label>
          <vs-textarea v-model="dataAdditionalInfo"/>
          <span class="text-danger text-sm" v-show="errors.has('item-price')">{{ errors.first('item-price') }}</span>
        </div>
      </div>
    </component>

    <div class="flex flex-wrap items-center p-6" slot="footer">
      <vs-button class="mr-6" @click="submitData" :disabled="!isFormValid">Submit</vs-button>
      <vs-button type="border" color="danger" @click="isSidebarActiveLocal = false">Cancel</vs-button>
    </div>
  </vs-sidebar>
</template>

<script>
import VuePerfectScrollbar from 'vue-perfect-scrollbar'

import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { Slovak } from 'flatpickr/dist/l10n/sk.js'

export default {
  props: {
    isSidebarActive: {
      type: Boolean,
      required: true
    },
    data: {
      type: Object,
      default: () => {}
    },
    event_data: {
      type: Object,
      default: () => {}
    }

  },
  components: {
    VuePerfectScrollbar,
    flatPickr
  },
  data () {
    return {
      dataId: null,
      dataStart: this.moment(this.event_data.start).subtract(1, 'day').format('YYYY-MM-DD'),
      dataEnd: this.moment(this.event_data.start).add(1, 'day').format('YYYY-MM-DD'),
      dataURL: null,
      dataOrder_status: 'pending',
      dataAdditionalInfo: '',
      dataName: null,
      dataPrice: 0,

      datePickerConfig: {
        altFormat: 'd.m.Y',
        altInput: true,
        dateFormat: 'Y-m-d',
        locale: Slovak
      },

      category_choices: [
        {
          text: 'Audio',
          value: 'audio'
        },
        {
          text: 'Computers',
          value: 'computers'
        },
        {
          text: 'Fitness',
          value: 'fitness'
        },
        {
          text: 'Appliance',
          value: 'appliance'
        }
      ],

      order_status_choices: [
        {
          text: 'Called',
          value: 'pending'
        },
        {
          text: 'Reserved',
          value: 'reserved'
        },
        {
          text: 'Paid',
          value: 'paied'
        }
      ],
      settings: { // perfectscrollbar settings
        maxScrollbarLength: 60,
        wheelSpeed: .60
      }
    }
  },
  watch: {
    isSidebarActive (val) {
      if (!val) return
      if (Object.entries(this.data).length === 0) {
        this.initValues()
        this.$validator.reset()
      } else {
        const {
          category,
          id,
          img,
          name,
          order_status,
          price
        } = JSON.parse(JSON.stringify(this.data))
        this.dataId = id
        this.dataCategory = category
        this.dataImg = img
        this.dataName = name
        this.dataOrder_status = order_status
        this.dataPrice = price
        this.initValues()
      }
    }
  },
  computed: {
    isSidebarActiveLocal: {
      get () {
        // TODO: fixed values but not sure
        // this.initValues()
        return this.isSidebarActive
      },
      set (val) {
        if (!val) {
          this.$emit('closeSidebar')
          this.$validator.reset()
          this.initValues()
        }
      }
    },
    isFormValid () {
      // FIXME: validate test
      return !this.errors.any() && this.dataName && this.dataPrice > 0
    },
    scrollbarTag () { return this.$store.getters.scrollbarTag }
  },
  methods: {
    initValues () {
      console.log('this.data', this.data)
      if (this.data.id) return
      this.dataId = null

      this.dataStart = this.moment(this.event_data.start).subtract(1, 'day').format('YYYY-MM-DD')
      this.dataEnd = this.moment(this.event_data.start).add(1, 'day').format('YYYY-MM-DD')

      this.dataName = null
      this.dataURL = null
      this.dataPrice = 0
    },
    submitData () {
      // FIXME: validate
      // this.$validator.validateAll().then(result => {
      // if (result) {
      const obj = {
        eventID: this.$route.params.eventId,
        id: this.dataId,
        start: this.moment(this.dataStart).format('YYYY-MM-DD'),
        end: this.moment(this.dataEnd).format('YYYY-MM-DD'),
        price: this.dataPrice,
        website: this.dataURL,
        name: this.dataName
      }

      if (this.dataId !== null && this.dataId >= 0) {
        console.log('updating with', obj)
        // TODO notify
        this.$store.dispatch('calendar/updateAccommodation', obj).catch(err => { console.error(err) })
      } else {
        console.log('creating with', obj)
        delete obj.id
        // TODO notify
        this.$store.dispatch('calendar/createAccommodation', obj).then(() => {
          this.$vs.notify({
            color: 'success',
            title: 'Accommodation created'
          })
        }).catch(err => {
          this.$vs.notify({
            color: 'danger',
            title: 'Accommodation creation failed',
            text: err.message
          })
          console.error(err)
        })
      }

      this.$emit('closeSidebar')
      this.initValues()
    }
  }
}
</script>

<style lang="scss" scoped>
.add-new-data-sidebar {
  ::v-deep .vs-sidebar--background {
    z-index: 52010;
  }

  ::v-deep .vs-sidebar {
    z-index: 52010;
    width: 400px;
    max-width: 90vw;

    .img-upload {
      margin-top: 2rem;

      .con-img-upload {
        padding: 0;
      }

      .con-input-upload {
        width: 100%;
        margin: 0;
      }
    }
  }
}

.scroll-area--data-list-add-new {
  // height: calc(var(--vh, 1vh) * 100 - 4.3rem);
  height: calc(var(--vh, 1vh) * 100 - 16px - 45px - 82px);

  &:not(.ps) {
    overflow-y: auto;
  }
}
</style>
