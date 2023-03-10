<!-- =========================================================================================
  File Name: DataListListView.vue
  Description: Data List - List View
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div id="event-edit-tab-accommodation">
    <div v-if="allowed" id="data-list-list-view" class="data-list-container">
      <data-view-sidebar :isSidebarActive="addNewDataSidebar"
                         @closeSidebar="toggleDataSidebar"
                         :data="sidebarData"
                         :event_data="data"/>

      <vs-table ref="table" :max-items="itemsPerPage" :data="accommodation">

        <div slot="header" class="flex flex-wrap-reverse items-center flex-grow justify-between">

          <div class="flex flex-wrap-reverse items-center data-list-btn-container">

            <!-- ADD NEW -->
            <div
                class="btn-add-new p-3 mb-4 mr-4 rounded-lg cursor-pointer flex items-center justify-center text-lg font-medium text-base text-primary border border-solid border-primary"
                @click="addNewData">
              <feather-icon icon="PlusIcon" svgClasses="h-4 w-4"/>
              <span class="ml-2 text-base text-primary">Add New</span>
            </div>
          </div>
        </div>

        <template slot="thead">
          <vs-th sort-key="name">Name</vs-th>
          <vs-th sort-key="url">URL</vs-th>
          <!--          <vs-th sort-key="popularity">Popularity</vs-th>-->
          <vs-th sort-key="from">From</vs-th>
          <vs-th sort-key="to">To</vs-th>
          <!--          <vs-th sort-key="status">Status</vs-th>-->
          <vs-th sort-key="price">Price adult</vs-th>
          <vs-th sort-key="price">Price child</vs-th>
          <vs-th>Action</vs-th>
        </template>

        <template slot-scope="{data}">
          <tbody>
          <vs-tr :data="tr" :key="indextr" v-for="(tr, indextr) in data">

            <vs-td>
              <p class="hotel-name font-medium truncate">{{ tr.name }}</p>
            </vs-td>

            <vs-td>
              <p class="hotel-name font-medium truncate">{{ tr.website }}</p>
            </vs-td>

            <!--            <vs-td>-->
            <!--              <vs-progress :percent="Number(tr.popularity)" :color="getPopularityColor(Number(tr.popularity))"-->
            <!--                           class="shadow-md"/>-->
            <!--            </vs-td>-->

            <vs-td>
              <p class="hotel-name font-medium truncate">{{ tr.start | date }}</p>
            </vs-td>
            <vs-td>
              <p class="hotel-name font-medium truncate">{{ tr.end | date }}</p>
            </vs-td>

            <!--            <vs-td>-->
            <!--              <vs-chip :color="getOrderStatusColor(tr.order_status)" class="product-order-status">-->
            <!--                {{ tr.order_status | title }}-->
            <!--              </vs-chip>-->
            <!--            </vs-td>-->

            <vs-td>
              <p class="product-price">{{ tr.price }}???</p>
            </vs-td>

            <vs-td>
              <p class="product-price">{{ tr.price }}???</p>
            </vs-td>

            <vs-td class="whitespace-no-wrap">
              <feather-icon icon="LinkIcon" svgClasses="w-5 h-5 hover:text-primary stroke-current"
                            @click.stop="alert('Not implemented yet')"/>
              <feather-icon icon="EditIcon" svgClasses="w-5 h-5 hover:text-primary stroke-current" class="ml-2"
                            @click.stop="editData(tr)"/>
              <feather-icon icon="TrashIcon" svgClasses="w-5 h-5 hover:text-danger stroke-current" class="ml-2"
                            @click.stop="deleteData(tr.id)"/>
            </vs-td>

          </vs-tr>
          </tbody>
        </template>
      </vs-table>
      <!--      <pre>{{ accommodation }}</pre>-->
    </div>
    <div v-else>
      <h2>Accommodation disabled</h2>
      <p>Do you want to allow accommodation?</p>
      <vs-button class="mt-4" color="success" @click="allowEditAndOpenSide">Allow</vs-button>
    </div>
  </div>
</template>

<script>
import DataViewSidebar from './DataViewSidebar'
// import moduleDataList from '@/store/data-list/moduleDataList.js'

export default {
  components: {
    DataViewSidebar
  },
  props: {
    data: {
      // TODO: send this data to sidebar
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      overrideAllowed: false,
      selected: [],
      // products: [],
      itemsPerPage: 5,
      isMounted: false,

      // Data Sidebar
      addNewDataSidebar: false,
      sidebarData: {}
    }
  },
  computed: {
    allowed () {
      return this.overrideAllowed || (Array.isArray(this.accommodation) && this.accommodation.length)
    },
    currentPage () {
      let ret = 0
      if (this.isMounted && !this.allowed) {
        ret = this.$refs.table.currentx
      }
      if (this.isMounted && this.allowed) {
        return ret
      }
      return 0
    },
    accommodation () {
      // console.log(this.$store.getters['calendar/getEvent'](parseInt(this.$route.params.eventId)).accommodation)
      return this.$store.getters['calendar/getEvent'](parseInt(this.$route.params.eventId)).accommodation
    },
    queriedItems () {
      return this.$refs.table ? this.$refs.table.queriedResults.length : this.accommodation.length
    }
  },
  methods: {
    allowEditAndOpenSide () {
      this.overrideAllowed = true
      this.addNewData()
    },
    addNewData () {
      this.sidebarData = {}
      this.toggleDataSidebar(true)
    },
    deleteData (id) {
      this.overrideAllowed = false
      this.$store.dispatch('calendar/deleteAccommodation', id)
        .then(() => {
          this.$store.dispatch('calendar/fetchEvent', this.$route.params.eventId)
        })
        .catch(err => { console.error(err) })
    },
    editData (data) {
      // this.sidebarData = JSON.parse(JSON.stringify(this.blankData))
      this.sidebarData = data
      this.toggleDataSidebar(true)
    },
    getOrderStatusColor (status) {
      if (status === 'on_hold') return 'warning'
      if (status === 'delivered') return 'success'
      if (status === 'canceled') return 'danger'
      return 'primary'
    },
    getPopularityColor (num) {
      if (num > 90) return 'success'
      if (num > 70) return 'primary'
      if (num >= 50) return 'warning'
      if (num < 50) return 'danger'
      return 'primary'
    },
    toggleDataSidebar (val = false) {
      this.addNewDataSidebar = val
    }
  },
  mounted () {
    this.isMounted = true
  }
}
</script>

<style lang="scss">
#data-list-list-view {
  .vs-con-table {

    /*
      Below media-queries is fix for responsiveness of action buttons
      Note: If you change action buttons or layout of this page, Please remove below style
    */
    @media (max-width: 689px) {
      .vs-table--search {
        margin-left: 0;
        max-width: unset;
        width: 100%;

        .vs-table--search-input {
          width: 100%;
        }
      }
    }

    @media (max-width: 461px) {
      .items-per-page-handler {
        display: none;
      }
    }

    @media (max-width: 341px) {
      .data-list-btn-container {
        width: 100%;

        .dd-actions,
        .btn-add-new {
          width: 100%;
          margin-right: 0 !important;
        }
      }
    }

    .hotel-name {
      max-width: 23rem;
    }

    .vs-table--header {
      display: flex;
      flex-wrap: wrap;
      margin-left: 1.5rem;
      margin-right: 1.5rem;

      > span {
        display: flex;
        flex-grow: 1;
      }

      .vs-table--search {
        padding-top: 0;

        .vs-table--search-input {
          padding: 0.9rem 2.5rem;
          font-size: 1rem;

          & + i {
            left: 1rem;
          }

          &:focus + i {
            left: 1rem;
          }
        }
      }
    }

    .vs-table {
      border-collapse: separate;
      border-spacing: 0 1.3rem;
      padding: 0 1rem;

      tr {
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, .05);

        td {
          padding: 20px;

          &:first-child {
            border-top-left-radius: .5rem;
            border-bottom-left-radius: .5rem;
          }

          &:last-child {
            border-top-right-radius: .5rem;
            border-bottom-right-radius: .5rem;
          }
        }

        td.td-check {
          padding: 20px !important;
        }
      }
    }

    .vs-table--thead {
      th {
        padding-top: 0;
        padding-bottom: 0;

        .vs-table-text {
          text-transform: uppercase;
          font-weight: 600;
        }
      }

      th.td-check {
        padding: 0 15px !important;
      }

      tr {
        background: none;
        box-shadow: none;
      }
    }

    .vs-table--pagination {
      justify-content: center;
    }
  }
}
</style>
