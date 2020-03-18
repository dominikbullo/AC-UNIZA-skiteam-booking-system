<!-- =========================================================================================
  File Name: UserList.vue
  Description: User List page
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>

  <div id="page-user-list">
    <div class="vx-card p-6">
      <div class="flex flex-wrap items-center">

        <!-- ITEMS PER PAGE -->
        <div class="flex-grow">
          <vs-dropdown vs-trigger-click class="cursor-pointer">
            <div
              class="p-4 border border-solid d-theme-border-grey-light rounded-full d-theme-dark-bg cursor-pointer flex items-center justify-between font-medium">
              <span class="mr-2">{{ currentPage * paginationPageSize - (paginationPageSize - 1) }} - {{ usersData.length - currentPage * paginationPageSize > 0 ? currentPage * paginationPageSize : usersData.length }} of {{ usersData.length }}</span>
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
        <vs-input class="sm:mr-4 mr-0 sm:w-auto w-full sm:order-normal order-3 sm:mt-0 mt-4" v-model="searchQuery"
                  @input="updateSearchQuery" placeholder="Search..."/>
        <!-- <vs-button class="mb-4 md:mb-0" @click="gridApi.exportDataAsCsv()">Export as CSV</vs-button> -->

        <vs-button
          class="sm:mr-4 mr-0 sm:w-auto w-full sm:order-normal order-2 sm:mt-0 mt-4"
          @click="activePrompt = true"
          icon="icon-plus" icon-pack="feather"
          v-show="$acl.check('editor')">
          {{ $t('AddChild') }}
        </vs-button>

        <vs-prompt
          :active.sync="activePrompt"
          :is-valid="validateForm"
          @accept="addChild"
          @cancel="clearFields"
          @close="clearFields"
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
        <vs-dropdown vs-trigger-click class="cursor-pointer">

          <div
            class="p-3 shadow-drop rounded-lg  d-theme-dark-light-bg cursor-pointer flex items-end justify-center text-lg font-medium w-32">
            <span class="mr-2 leading-none">Actions</span>
            <feather-icon icon="ChevronDownIcon" svgClasses="h-4 w-4"/>
          </div>

          <vs-dropdown-menu>

            <vs-dropdown-item>
                <span class="flex items-center">
                  <feather-icon icon="TrashIcon" svgClasses="h-4 w-4" class="mr-2"/>
                  <span>Delete</span>
                </span>
            </vs-dropdown-item>

            <vs-dropdown-item>
                <span class="flex items-center">
                  <feather-icon icon="ArchiveIcon" svgClasses="h-4 w-4" class="mr-2"/>
                  <span>Archive</span>
                </span>
            </vs-dropdown-item>

            <vs-dropdown-item>
                <span class="flex items-center">
                  <feather-icon icon="FileIcon" svgClasses="h-4 w-4" class="mr-2"/>
                  <span>Print</span>
                </span>
            </vs-dropdown-item>

            <vs-dropdown-item>
                <span class="flex items-center">
                  <feather-icon icon="SaveIcon" svgClasses="h-4 w-4" class="mr-2"/>
                  <span>CSV</span>
                </span>
            </vs-dropdown-item>

          </vs-dropdown-menu>
        </vs-dropdown>
      </div>


      <!-- AgGrid Table -->
      <ag-grid-vue
        ref="agGridTable"
        :components="components"
        :gridOptions="gridOptions"
        class="ag-theme-material w-100 my-4 ag-grid-table"
        :columnDefs="columnDefs"
        :defaultColDef="defaultColDef"
        :rowData="usersData"
        rowSelection="multiple"
        colResizeDefault="shift"
        :animateRows="true"
        :floatingFilter="true"
        :pagination="true"
        :paginationPageSize="paginationPageSize"
        :suppressPaginationPanel="true"
        :enableRtl="$vs.rtl">
      </ag-grid-vue>

      <vs-pagination
        :total="totalPages"
        :max="7"
        v-model="currentPage"/>

    </div>
  </div>

</template>

<script>
import {AgGridVue} from 'ag-grid-vue'
import '@/assets/scss/vuexy/extraComponents/agGridStyleOverride.scss'
import vSelect from 'vue-select'


// Store Module
import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'

// Cell Renderer
import CellRendererLink from './cell-renderer/CellRendererLink.vue'
import CellRendererStatus from './cell-renderer/CellRendererStatus.vue'
import CellRendererVerified from './cell-renderer/CellRendererVerified.vue'
import CellRendererActions from './cell-renderer/CellRendererActions.vue'
// import FamilyAddNew from '../FamilyAddNew.vue'

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
      gridOptions: {},
      defaultColDef: {
        sortable: true,
        resizable: true,
        suppressMenu: true
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
          headerName: 'Country',
          field: 'country',
          filter: true,
          width: 150
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
          width: 125,
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
      components: {
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
    usersData () {
      return this.$store.state.userManagement.users
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
        title: '',
        desc: '',
        isCompleted: false,
        isImportant: false,
        isStarred: false,
        tags: []
      })
    },
    addChild () {
      this.$validator.validateAll().then(result => {
        console.log(result)
        if (result) {
          this.$store.dispatch('family/addChild', Object.assign({}, this.childData))
          this.clearFields()
          // this.closeComponent()
        }
      })
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
    if (!moduleUserManagement.isRegistered) {
      this.$store.registerModule('userManagement', moduleUserManagement)
      moduleUserManagement.isRegistered = true
    }
    this.$store.dispatch('userManagement/fetchUsers').catch(err => {
      console.error(err)
    })
    // OR
    // this.$store.dispatch('userManagement/fetchProfiles').catch(err => { console.error(err) })
  }
}

</script>

<style lang="scss">
  #page-user-list {
    .user-list-filters {
      .vs__actions {
        position: absolute;
        right: 0;
        top: 50%;
        transform: translateY(-58%);
      }
    }
  }
</style>
