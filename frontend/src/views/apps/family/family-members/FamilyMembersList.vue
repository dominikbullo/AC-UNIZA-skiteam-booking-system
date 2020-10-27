<template>
  <div id="page-family-list">
    <div class="vx-card p-6">
      <div class="flex flex-wrap items-center">

        <!-- ITEMS PER PAGE -->
        <div class="flex-grow">
          <vs-dropdown class="cursor-pointer" vs-trigger-click>
            <div
                class="p-4 border border-solid d-theme-border-grey-light rounded-full d-theme-dark-bg cursor-pointer flex items-center justify-between font-medium">
              <span class="mr-2">
                {{ currentPage * paginationPageSize - (paginationPageSize - 1) }} -
                {{
                  familyMembers.length - currentPage * paginationPageSize > 0 ? currentPage * paginationPageSize : familyMembers.length
                }} of {{ familyMembers.length }}</span>
              <feather-icon icon="ChevronDownIcon" svgClasses="h-4 w-4"/>
            </div>
            <!-- <vs-button class="btn-drop" type="line" color="primary" icon-pack="feather" icon="icon-chevron-down"></vs-button> -->
            <vs-dropdown-menu>

              <vs-dropdown-item @click="gridApi.paginationSetPageSize(10)">
                <span>10</span>
              </vs-dropdown-item>
              <vs-dropdown-item @click="gridApi.paginationSetPageSize(20)">
                <span>20</span>
              </vs-dropdown-item>
              <vs-dropdown-item @click="gridApi.paginationSetPageSize(50)">
                <span>50</span>
              </vs-dropdown-item>
              <vs-dropdown-item @click="gridApi.paginationSetPageSize(100)">
                <span>100</span>
              </vs-dropdown-item>
            </vs-dropdown-menu>
            <!--             <vs-button class="btn-drop" type="line" color="primary" icon-pack="feather" icon="icon-chevron-down"></vs-button> -->
            <div
                class="p-4 border border-solid d-theme-border-grey-light rounded-full d-theme-dark-bg cursor-pointer flex items-center justify-between font-medium">
              <span class="mr-2">{{ currentPage * paginationPageSize - (paginationPageSize - 1) }} - {{
                  familyMembers.length - currentPage * paginationPageSize > 0 ? currentPage * paginationPageSize : familyMembers.length
                }} of {{ familyMembers.length }}</span>
              <feather-icon icon="ChevronDownIcon" svgClasses="h-4 w-4"/>
            </div>
          </vs-dropdown>
        </div>

        <!-- TABLE ACTION COL-2: SEARCH & EXPORT AS CSV -->
        <vs-input @input="updateSearchQuery" class="sm:mr-4 mr-0 sm:w-auto w-full sm:order-normal order-3 sm:mt-0 mt-4"
                  placeholder="Search..." v-model="searchQuery"/>

        <vs-button
            @click="activePrompt = true"
            class="sm:mr-4 mr-0 sm:w-auto w-full sm:order-normal order-2 sm:mt-0 mt-4"
            icon="icon-plus" icon-pack="feather"
            v-show="$acl.check('isParent')">
          {{ $t('AddChild') }}
        </vs-button>

        <vs-prompt
            :active.sync="activePrompt"
            :is-valid="validateForm"
            @accept="addChild"
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
                      <span class="text-danger text-sm">{{ errors.first('name') }}</span>
                    </div>

                    <div class="vx-col sm:w-1/2 w-full mb-2">
                      <vs-input
                          :label-placeholder="$t('Surname')"
                          :placeholder="$t('Surname')"
                          class="w-full mt-6"
                          data-vv-validate-on="blur"
                          name="surname"
                          type="text"
                          v-model="childData.last_name"
                          v-validate="'required|alpha_dash|min:3'"/>
                      <span class="text-danger text-sm">{{ errors.first('surname') }}</span>
                    </div>
                  </div>

                  <vs-input
                      :label-placeholder="$t('Username')"
                      :placeholder="$t('Username')"
                      class="w-full mt-6"
                      data-vv-validate-on="blur"
                      name="username"
                      type="text"
                      v-model="childData.username"
                      v-validate="'required|alpha_dash|min:3'"/>
                  <span class="text-danger text-sm">{{ errors.first('username') }}</span>


                  <vs-input
                      :label-placeholder="$t('Email')"
                      :placeholder="$t('Email')"
                      class="w-full mt-6"
                      data-vv-validate-on="blur"
                      name="email"
                      type="email"
                      v-model="childData.email"
                      v-validate="'email'"/>
                  <span class="text-danger text-sm">{{ errors.first('email') }}</span>


                  <!-- RES: https://flatpickr.js.org/formatting/ -->
                  <div>
                    <label style="font-size: 10px">{{ $t('BirthDate') }}</label>
                    <flat-pickr :config="datePickerConfig" class="w-full"
                                v-model="childData.profile.birth_date"/>
                    <span class="text-danger text-sm">{{ errors.first('birth_date') }}</span>
                  </div>

                  <div>
                    <label style="font-size: 10px">{{ $t('Gender') }}</label>
                    <div class="demo-alignment mb-base">
                      <vs-radio class="mt-2" v-model=" childData.profile.gender" vs-value="M">{{ $t('Male') }}
                      </vs-radio>
                      <vs-radio class="mt-2" v-model="childData.profile.gender" vs-value="F">{{ $t('Female') }}
                      </vs-radio>
                    </div>
                  </div>

                  <vs-input
                      :label-placeholder="$t('Password')"
                      :placeholder="$t('Password')"
                      class="w-full mt-6"
                      data-vv-validate-on="blur"
                      name="password"
                      ref="password"
                      type="password"
                      v-model="childData.password1"
                      v-validate="'required|min:6'"/>
                  <span class="text-danger text-sm">{{ errors.first('password1') }}</span>

                  <vs-input
                      :label-placeholder="$t('ConfirmPassword')"
                      :placeholder="$t('ConfirmPassword')"
                      class="w-full mt-6"
                      data-vv-as="password"
                      data-vv-validate-on="blur"
                      name="confirm_password"
                      type="password"
                      v-model="childData.password2"
                      v-validate="'min:6|confirmed:password'"/>
                  <span class="text-danger text-sm">{{ errors.first('confirm_password') }}</span>
                </div>
              </div>

            </form>
          </div>
        </vs-prompt>

        <!-- ACTION - DROPDOWN -->
        <!--        <vs-dropdown class="cursor-pointer" vs-trigger-click>-->

        <!--          <div-->
        <!--            class="p-3 shadow-drop rounded-lg  d-theme-dark-light-bg cursor-pointer flex items-end justify-center text-lg font-medium w-32">-->
        <!--            <span class="mr-2 leading-none">Actions</span>-->
        <!--            <feather-icon icon="ChevronDownIcon" svgClasses="h-4 w-4"/>-->
        <!--          </div>-->

        <!--          <vs-dropdown-menu>-->

        <!--            <vs-dropdown-item>-->
        <!--                <span class="flex items-center">-->
        <!--                  <feather-icon class="mr-2" icon="TrashIcon" svgClasses="h-4 w-4"/>-->
        <!--                  <span>Delete</span>-->
        <!--                </span>-->
        <!--            </vs-dropdown-item>-->

        <!--            <vs-dropdown-item>-->
        <!--                <span class="flex items-center">-->
        <!--                  <feather-icon class="mr-2" icon="ArchiveIcon" svgClasses="h-4 w-4"/>-->
        <!--                  <span>Archive</span>-->
        <!--                </span>-->
        <!--            </vs-dropdown-item>-->

        <!--            <vs-dropdown-item>-->
        <!--                <span class="flex items-center">-->
        <!--                  <feather-icon class="mr-2" icon="FileIcon" svgClasses="h-4 w-4"/>-->
        <!--                  <span>Print</span>-->
        <!--                </span>-->
        <!--            </vs-dropdown-item>-->

        <!--            <vs-dropdown-item>-->
        <!--                <span class="flex items-center">-->
        <!--                  <feather-icon class="mr-2" icon="SaveIcon" svgClasses="h-4 w-4"/>-->
        <!--                  <span>CSV</span>-->
        <!--                </span>-->
        <!--            </vs-dropdown-item>-->

        <!--          </vs-dropdown-menu>-->
        <!--        </vs-dropdown>-->
      </div>

      <!-- RES: Height https://www.ag-grid.com/javascript-grid-width-and-height/-->
      <!-- AgGrid Table -->
      <ag-grid-vue
          :animateRows="true"
          :columnDefs="columnDefs"
          :components="components"
          :defaultColDef="defaultColDef"
          :enableRtl="$vs.rtl"
          :floatingFilter="true"
          :gridOptions="gridOptions"
          :pagination="true"
          :paginationPageSize="paginationPageSize"
          :rowData="familyMembers"
          :suppressPaginationPanel="true"
          class="ag-theme-material w-100 my-4 ag-grid-table"
          colResizeDefault="shift"
          ref="agGridTable"
          rowSelection="multiple">
      </ag-grid-vue>

      <vs-pagination
          :max="7"
          :total="totalPages"
          v-model="currentPage"/>

    </div>
  </div>

</template>

<script>
import { AgGridVue } from 'ag-grid-vue'
import '@/assets/scss/vuexy/extraComponents/agGridStyleOverride.scss'
import vSelect from 'vue-select'

import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import { Slovak } from 'flatpickr/dist/l10n/sk.js'

// Cell Renderer
import CellRendererLink from './cell-renderer/CellRendererLink.vue'
import CellRendererStatus from './cell-renderer/CellRendererStatus.vue'
import CellRendererVerified from './cell-renderer/CellRendererVerified.vue'
import CellRendererActions from './cell-renderer/CellRendererActions.vue'


export default {
  components: {
    AgGridVue,
    flatPickr,
    vSelect,

    // Cell Renderer
    /* eslint-disable vue/no-unused-components */
    CellRendererLink,
    CellRendererVerified,
    CellRendererActions
    /* eslint-enable vue/no-unused-components */
  },
  data () {
    return {
      searchQuery: '',
      activePrompt: false,
      activePrompt1: false,

      datePickerConfig: {
        altFormat: 'd.m.Y',
        altInput: true,
        dateFormat: 'Y-m-d',
        locale: Slovak
      },
      childData: {
        id: null,
        username: 'testsets',
        email: 'tes@tes.sk',
        password1: 'testing321',
        password2: 'testing321',
        first_name: 'testing321',
        last_name: 'testing321',
        profile: {
          birth_date: this.moment().format('YYYY-MM-DD'),
          phone_number: '',
          location: '',
          gender: 'M'
        }
      },

      // AgGrid
      gridApi: null,
      gridOptions:
          {},

      defaultColDef: {
        sortable: true,
        resizable:
            true,
        suppressMenu:
            true
      },

      columnDefs: [

        {
          headerName: 'Username',
          field: 'username',
          filter: true,
          width: 210,
          cellRendererFramework: 'CellRendererLink',
          checkboxSelection: true,
          headerCheckboxSelectionFilteredOnly: true,
          headerCheckboxSelection: true
        },
        {
          headerName: 'Email',
          field: 'email',
          filter: true,
          width: 210
        },
        {
          headerName: 'First Name',
          field: 'first_name',
          filter: true,
          width: 200
        },
        {
          headerName: 'Surname',
          field: 'last_name',
          filter: true,
          width: 200
        },
        {
          headerName: 'Birth Date',
          field: 'profile.birth_date',
          filter: true,
          width: 150
        },
        {
          headerName: 'Gender',
          field: 'profile.gender',
          cellClass: 'text-center',
          filter: true,
          width: 110
        },
        {
          headerName: 'Role',
          field: 'profile.userRole',
          filter: true,
          width: 150
        },
        // {
        //   headerName: 'Status',
        //   field: 'status',
        //   filter: true,
        //   width: 150,
        //   cellRendererFramework: 'CellRendererStatus'
        // },
        {
          headerName: 'Verified',
          field: 'verified_email',
          filter: true,
          width: 110,
          cellRendererFramework: 'CellRendererVerified',
          cellClass: 'text-center'
        },
        // TODO actions
        {
          headerName: 'Actions',
          field: 'transactions',
          width: 150,
          cellRendererFramework: 'CellRendererActions'
        }
      ],

      // Cell Renderer Components
      components:
          {
            CellRendererLink,
            CellRendererStatus,
            CellRendererVerified,
            CellRendererActions
          }
    }
  },
  watch: {
    roleFilter (obj) {
      this.setColumnFilter('role', obj.value)
    },
    statusFilter (obj) {
      this.setColumnFilter('status', obj.value)
    },
    isVerifiedFilter (obj) {
      const val = obj.value === 'all' ? 'all' : obj.value === 'yes' ? 'true' : 'false'
      this.setColumnFilter('is_verified', val)
    },
    departmentFilter (obj) {
      this.setColumnFilter('department', obj.value)
    }
  },
  computed: {
    familyMembers () {
      const members = this.$store.state.family.members

      const cleanMembers = []
      members.forEach((element) => {
        cleanMembers.unshift(element['user'])
      })
      return cleanMembers
    },
    paginationPageSize () {
      if (this.gridApi) {
        return this.gridApi.paginationGetPageSize()
      } else {
        return 10
      }
    },
    totalPages () {
      if (this.gridApi) {
        return this.gridApi.paginationGetTotalPages()
      } else {
        return 0
      }
    },
    currentPage: {
      get () {
        if (this.gridApi) {
          return this.gridApi.paginationGetCurrentPage() + 1
        } else {
          return 1
        }
      },
      set (val) {
        console.log('val', val)
        this.gridApi.paginationGoToPage(val - 1)
      }
    },
    validateForm () {
      return true
      // return !this.errors.any()
    }
  },
  methods: {
    openConfirm () {
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: 'Confirm',
        text: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
      })
    },
    setColumnFilter (column, val) {
      const filter = this.gridApi.getFilterInstance(column)
      let modelObj = null

      if (val !== 'all') {
        modelObj = {
          type: 'equals',
          filter: val
        }
      }

      filter.setModel(modelObj)
      this.gridApi.onFilterChanged()
    },
    resetColFilters () {
      // Reset Grid Filter
      this.gridApi.setFilterModel(null)
      this.gridApi.onFilterChanged()

      // Reset Filter Options
      this.roleFilter = this.statusFilter = this.isVerifiedFilter = this.departmentFilter = {
        label: 'All',
        value: 'all'
      }

      this.$refs.filterCard.removeRefreshAnimation()
    },
    updateSearchQuery (val) {
      this.gridApi.setQuickFilter(val)
    },
    clearFields () {
      Object.assign(this.childData, {
        username: '',
        email: '',
        password1: '',
        password2: '',
        first_name: '',
        last_name: '',
        profile: {
          birth_date: this.moment().format('DD.MM.YYYY'),
          gender: 'M'
        }
      })
    },
    close () {
      this.$vs.notify({
        color: 'danger',
        title: 'Closed',
        text: 'You close a dialog!'
      })
    },
    addChild () {
      // if (!this.this.$validator.validateAll() || this.checkLogin())
      this.$validator.validateAll().then(result => {

        if (result) {
          this.$store.dispatch('family/addChild', Object.assign({}, this.childData)).then(() => {
            this.clearFields()
            this.$vs.notify({
              color: 'success',
              title: 'Child Added',
              text: 'The child was successfully added'
            })
            this.clearFields()
          }).catch(error => {
            this.$vs.loading.close()
            console.error(error)
            this.$vs.notify({
              color: 'danger',
              title: 'Child Not added',
              text: error.message
            })
            // this.multipleNotify(error.response.data)
          })
        } else {
          this.$vs.notify({
            color: 'danger',
            title: 'Child Not added',
            text: 'Form is not valid'
          })
        }
      })
    },
    // RES: https://stackoverflow.com/questions/29516136/how-to-print-all-values-of-a-nested-object
    multipleNotify (obj) {
      for (const key in obj) {
        if (typeof obj[key] === 'object') {
          this.multipleNotify(obj[key])
        } else {
          this.$vs.notify({
            title: 'Error',
            text: obj[key],
            iconPack: 'feather',
            icon: 'icon-alert-circle',
            color: 'danger'
          })
        }
      }
    }
  },
  mounted () {
    this.gridApi = this.gridOptions.api
  },
  created () {
    this.$store.dispatch('family/fetchFamily', this.$store.state.AppActiveUser.profile.family_id)
  }
}
</script>
