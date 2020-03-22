<!-- =========================================================================================
  File Name: UserList.vue
  Description: User List page
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div id="page-family-list">
    <div class="vx-card p-6">
      <div class="flex flex-wrap items-center">

        <!-- ITEMS PER PAGE -->
        <div class="flex-grow">
          <vs-dropdown class="cursor-pointer" vs-trigger-click>
            <div
              class="p-4 border border-solid d-theme-border-grey-light rounded-full d-theme-dark-bg cursor-pointer flex items-center justify-between font-medium">
              <span class="mr-2">{{ currentPage * paginationPageSize - (paginationPageSize - 1) }} - {{ familyMembers.length - currentPage * paginationPageSize > 0 ? currentPage * paginationPageSize : familyMembers.length }} of {{ familyMembers.length }}</span>
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
          </vs-dropdown>
        </div>

        <!-- TABLE ACTION COL-2: SEARCH & EXPORT AS CSV -->
        <vs-input @input="updateSearchQuery" class="sm:mr-4 mr-0 sm:w-auto w-full sm:order-normal order-3 sm:mt-0 mt-4"
                  placeholder="Search..." v-model="searchQuery"/>
        <!-- <vs-button class="mb-4 md:mb-0" @click="gridApi.exportDataAsCsv()">Export as CSV</vs-button> -->

        <vs-button
          @click="activePrompt = true"
          class="sm:mr-4 mr-0 sm:w-auto w-full sm:order-normal order-2 sm:mt-0 mt-4"
          icon="icon-plus" icon-pack="feather"
          v-show="$acl.check('editor')">
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
                      <span class="text-danger text-sm">{{ errors.first('childData.first_name') }}</span>
                    </div>

                    <div class="vx-col sm:w-1/2 w-full mb-2">
                      <vs-input
                        :label-placeholder="$t('Surname')"
                        :placeholder="$t('Surname')"
                        class="w-full mt-6"
                        data-vv-validate-on="blur"
                        name="email"
                        type="text"
                        v-model="childData.last_name"
                        v-validate="'required|alpha_dash|min:3'"/>
                      <span class="text-danger text-sm">{{ errors.first('childData.first_name') }}</span>
                    </div>
                  </div>

                  <vs-input
                    :label-placeholder="$t('Username')"
                    :placeholder="$t('Username')"
                    class="w-full mt-6"
                    data-vv-validate-on="blur"
                    name="email"
                    type="text"
                    v-model="childData.username"
                    v-validate="'required|alpha_dash|min:3'"/>
                  <span class="text-danger text-sm">{{ errors.first('childData.first_name') }}</span>

                  <vs-input
                    :label-placeholder="$t('Email')"
                    :placeholder="$t('Email')"
                    class="w-full mt-6"
                    data-vv-validate-on="blur"
                    name="email"
                    type="email"
                    v-model="childData.email"
                    v-validate="'email'"/>
                  <span class="text-danger text-sm">{{ errors.first('childData.email') }}</span>


                  <!-- RES: https://flatpickr.js.org/formatting/ -->
                  <label style="font-size: 10px">{{ $t('BirthDate') }}</label>
                  <flat-pickr :config="{ dateFormat: 'd.m.Y',maxDate: new Date().fp_incr(14) }" class="w-full"
                              v-model="childData.profile.birth_date"/>
                  <span class="text-danger text-sm">{{ errors.first('childData.profile.birth_date') }}</span>

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
                  <span class="text-danger text-sm">{{ errors.first('childData.password1') }}</span>

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
                  <span class="text-danger text-sm">{{ errors.first('childData.password2') }}</span>
                </div>
              </div>

            </form>
          </div>
        </vs-prompt>

        <!-- ACTION - DROPDOWN -->
        <vs-dropdown class="cursor-pointer" vs-trigger-click>

          <div
            class="p-3 shadow-drop rounded-lg  d-theme-dark-light-bg cursor-pointer flex items-end justify-center text-lg font-medium w-32">
            <span class="mr-2 leading-none">Actions</span>
            <feather-icon icon="ChevronDownIcon" svgClasses="h-4 w-4"/>
          </div>

          <vs-dropdown-menu>

            <vs-dropdown-item>
                <span class="flex items-center">
                  <feather-icon class="mr-2" icon="TrashIcon" svgClasses="h-4 w-4"/>
                  <span>Delete</span>
                </span>
            </vs-dropdown-item>

            <vs-dropdown-item>
                <span class="flex items-center">
                  <feather-icon class="mr-2" icon="ArchiveIcon" svgClasses="h-4 w-4"/>
                  <span>Archive</span>
                </span>
            </vs-dropdown-item>

            <vs-dropdown-item>
                <span class="flex items-center">
                  <feather-icon class="mr-2" icon="FileIcon" svgClasses="h-4 w-4"/>
                  <span>Print</span>
                </span>
            </vs-dropdown-item>

            <vs-dropdown-item>
                <span class="flex items-center">
                  <feather-icon class="mr-2" icon="SaveIcon" svgClasses="h-4 w-4"/>
                  <span>CSV</span>
                </span>
            </vs-dropdown-item>

          </vs-dropdown-menu>
        </vs-dropdown>
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
import {AgGridVue} from 'ag-grid-vue'
import '@/assets/scss/vuexy/extraComponents/agGridStyleOverride.scss'
import vSelect from 'vue-select'


// Store Module
import moduleFamily from '@/store/family/moduleFamily.js'

// Cell Renderer
import CellRendererLink from './cell-renderer/CellRendererLink.vue'
import CellRendererStatus from './cell-renderer/CellRendererStatus.vue'
import CellRendererVerified from './cell-renderer/CellRendererVerified.vue'
import CellRendererActions from './cell-renderer/CellRendererActions.vue'

import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'

export default {
  components: {
    AgGridVue,
    flatPickr,
    vSelect,

    // Cell Renderer
    /* eslint-disable vue/no-unused-components */
    CellRendererLink,
    CellRendererStatus,
    CellRendererVerified,
    CellRendererActions
    /* eslint-enable vue/no-unused-components */
  },
  data () {
    return {
      searchQuery: '',
      activePrompt: false,

      childData: {
        username: 'testsets',
        email: 'tes@tes.sk',
        password1: 'testing321',
        password2: 'testing321',
        first_name: 'testing321',
        last_name: 'testing321',
        profile: {
          birth_date: new Date(),
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
          headerName: 'ID',
          field: 'id',
          width: 125,
          // filter: true,
          checkboxSelection: true,
          headerCheckboxSelectionFilteredOnly: true,
          headerCheckboxSelection: true
        },
        {
          headerName: 'Username',
          field: 'username',
          filter: true,
          width: 210,
          cellRendererFramework: 'CellRendererLink'
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
          headerName: 'Role',
          field: 'role',
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
      return this.$store.state.family.members
    },
    paginationPageSize () {
      if (this.gridApi) return this.gridApi.paginationGetPageSize()
      else return 10
    },
    totalPages () {
      if (this.gridApi) return this.gridApi.paginationGetTotalPages()
      else return 0
    },
    currentPage: {
      get () {
        if (this.gridApi) return this.gridApi.paginationGetCurrentPage() + 1
        else return 1
      },
      set (val) {
        this.gridApi.paginationGoToPage(val - 1)
      }
    },
    validateForm () {
      return !this.errors.any()
    }
  },
  methods: {
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
          birth_date: new Date(),
          gender: 'M'
        }
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
              title: 'User Deleted',
              text: 'The selected user was successfully deleted'
            })

          }).catch(error => {
            this.$vs.loading.close()
            // this.multipleNotify(error.response.data)
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

    /* =================================================================
      NOTE:
      Header is not aligned properly in RTL version of agGrid table.
      However, we given fix to this issue. If you want more robust solution please contact them at gitHub
    ================================================================= */
    if (this.$vs.rtl) {
      const header = this.$refs.agGridTable.$el.querySelector('.ag-header-container')
      header.style.left = `-${String(Number(header.style.transform.slice(11, -3)) + 9)}px`
    }
  },
  created () {
    // const filter = this.$route.params.filter
    // this.$store.dispatch('family/fetchFamily', {filter})
    this.$store.dispatch('family/fetchFamily')
  }
}


</script>
