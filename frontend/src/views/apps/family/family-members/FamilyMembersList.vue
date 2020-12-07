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
          </vs-dropdown>
        </div>

        <!-- TABLE ACTION COL-2: SEARCH & EXPORT AS CSV -->
        <vs-input @input="updateSearchQuery" class="sm:mr-4 mr-0 sm:w-auto w-full sm:order-normal order-3 sm:mt-0 mt-4"
                  placeholder="Search..." v-model="searchQuery"/>

        <vs-button
            @click="toggleAddChildPrompt(true)"
            class="sm:mr-4 mr-0 sm:w-auto w-full sm:order-normal order-2 sm:mt-0 mt-4"
            icon="icon-plus" icon-pack="feather"
            v-show="$acl.check('isParent')">
          {{ $t('AddChild') }}
        </vs-button>

        <add-child-component :isPromptActive="addChildPromptActive" @closePrompt="toggleAddChildPrompt"/>
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

import AddChildComponent from '@/components/family/AddChildComponent'

export default {
  components: {
    AgGridVue,
    AddChildComponent,

    // Cell Renderer
    /* eslint-disable vue/no-unused-components */
    CellRendererLink,
    CellRendererVerified
    // CellRendererActions
    /* eslint-enable vue/no-unused-components */
  },
  data () {
    return {
      searchQuery: '',
      addChildPromptActive: false,

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
          headerName: 'Email',
          field: 'email',
          filter: true,
          width: 300,
          cellRendererFramework: 'CellRendererLink',
          checkboxSelection: true,
          headerCheckboxSelectionFilteredOnly: true,
          headerCheckboxSelection: true
        },
        {
          headerName: 'Display Name',
          field: 'profile.displayName',
          filter: true,
          width: 250
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
        }
        // TODO actions
        // {
        //   headerName: 'Actions',
        //   field: 'transactions',
        //   width: 150,
        //   cellRendererFramework: 'CellRendererActions'
        // }
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
    toggleAddChildPrompt (val = false) {
      this.addChildPromptActive = val
    }
  },
  mounted () {
    this.gridApi = this.gridOptions.api
    // TODO: open on link
    console.log('this.$route.hash.toLowerCase()', this.$route.hash.toLowerCase())
    this.addChildPromptActive = this.$route.hash.toLowerCase() === '#addchild'

  },
  created () {
    this.$store.dispatch('family/fetchFamily', this.$store.getters['familyID'])
  }
}
</script>
