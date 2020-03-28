<template>
  <div>
    <div class="vx-row">
      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4 mb-base">
        <statistics-card-line
          :chartData="subscribersGained.series"
          :statistic="subscribersGained.analyticsData.subscribers | k_formatter"
          icon="UsersIcon"
          statisticTitle="Subscribers Gained"
          type="area"
          v-if="subscribersGained.analyticsData"/>
      </div>

      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4 mb-base">
        <statistics-card-line
          :chartData="revenueGenerated.series"
          :statistic="revenueGenerated.analyticsData.revenue | k_formatter"
          color="success"
          icon="DollarSignIcon"
          statisticTitle="Revenue Generated"
          type="area"
          v-if="revenueGenerated.analyticsData"/>
      </div>

      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4 mb-base">
        <statistics-card-line
          :chartData="quarterlySales.series"
          :statistic="quarterlySales.analyticsData.sales"
          color="danger"
          icon="ShoppingCartIcon"
          statisticTitle="Quarterly Sales"
          type="area"
          v-if="quarterlySales.analyticsData"/>
      </div>
      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4 mb-base">
        <statistics-card-line
          :chartData="ordersRecevied.series"
          :statistic="ordersRecevied.analyticsData.orders | k_formatter"
          color="warning"
          icon="ShoppingBagIcon"
          statisticTitle="Orders Received"
          type="area"
          v-if="ordersRecevied.analyticsData"/>
      </div>
    </div>

    <div class="vx-row">
      <!-- RADIAL CHART -->
      <div class="vx-col w-full sm:w-1/2 md:w-1/3 mb-base">
        <vx-card title="Goal Overview">
          <template slot="actions">
            <feather-icon icon="HelpCircleIcon" svgClasses="w-6 h-6 text-grey"></feather-icon>
          </template>

          <!-- CHART -->
          <template slot="no-body">
            <div class="mt-10">
              <vue-apex-charts
                :options="analyticsData.goalOverviewRadialBar.chartOptions"
                :series="goalOverview.series"
                height="240"
                type="radialBar"/>
            </div>
          </template>

          <!-- DATA -->
          <div
            class="flex justify-between text-center mt-4"
            slot="no-body-bottom"
            v-if="goalOverview.analyticsData">

            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0">
              <p class="mt-4">Completed</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.completed.toLocaleString() }}</p>
            </div>
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">
              <p class="mt-4">In Progress</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.inProgress.toLocaleString() }}</p>
            </div>
          </div>
        </vx-card>
      </div>
      <!-- RADIAL CHART -->
      <div class="vx-col w-full sm:w-1/2 md:w-1/3 mb-base">
        <vx-card title="Goal Overview">
          <template slot="actions">
            <feather-icon icon="HelpCircleIcon" svgClasses="w-6 h-6 text-grey"></feather-icon>
          </template>

          <!-- CHART -->
          <template slot="no-body">
            <div class="mt-10">
              <vue-apex-charts
                :options="analyticsData.goalOverviewRadialBar.chartOptions"
                :series="goalOverview.series"
                height="240"
                type="radialBar"/>
            </div>
          </template>

          <!-- DATA -->
          <div
            class="flex justify-between text-center mt-4"
            slot="no-body-bottom"
            v-if="goalOverview.analyticsData">

            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0">
              <p class="mt-4">Completed</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.completed.toLocaleString() }}</p>
            </div>
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">
              <p class="mt-4">In Progress</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.inProgress.toLocaleString() }}</p>
            </div>
          </div>
        </vx-card>
      </div>

      <div class="vx-col w-full sm:w-1/2 md:w-1/3 mb-base">
        <vx-card title="Activity Timeline">
          <vx-timeline :data="timelineData"></vx-timeline>
        </vx-card>
      </div>
    </div>

    <div class="vx-row">
      <!-- CARD 9: DISPATCHED ORDERS -->
      <div class="vx-col w-full">
        <vx-card title="Dispatched Orders">
          <div slot="no-body" class="mt-4">
            <vs-table :data="dispatchedOrders" class="table-dark-inverted">
              <template slot="thead">
                <vs-th>ORDER NO.</vs-th>
                <vs-th>STATUS</vs-th>
                <vs-th>OPERATORS</vs-th>
                <vs-th>LOCATION</vs-th>
                <vs-th>DISTANCE</vs-th>
                <vs-th>START DATE</vs-th>
                <vs-th>EST DELIVERY DATE</vs-th>
              </template>

              <template slot-scope="{data}">
                <vs-tr :key="indextr" v-for="(tr, indextr) in data">
                  <vs-td :data="data[indextr].orderNo">
                    <span>#{{data[indextr].orderNo}}</span>
                  </vs-td>
                  <vs-td :data="data[indextr].status">
                    <span class="flex items-center px-2 py-1 rounded"><div class="h-3 w-3 rounded-full mr-2"
                                                                           :class="'bg-' + data[indextr].statusColor"></div>{{data[indextr].status}}</span>
                  </vs-td>
                  <vs-td :data="data[indextr].orderNo">
                    <ul class="users-liked user-list">
                      <li v-for="(user, userIndex) in data[indextr].usersLiked" :key="userIndex">
                        <vx-tooltip :text="user.name" position="bottom">
                          <vs-avatar :src="user.img" size="30px"
                                     class="border-2 border-white border-solid -m-1"></vs-avatar>
                        </vx-tooltip>
                      </li>
                    </ul>
                  </vs-td>
                  <vs-td :data="data[indextr].orderNo">
                    <span>{{data[indextr].location}}</span>
                  </vs-td>
                  <vs-td :data="data[indextr].orderNo">
                    <span>{{data[indextr].distance}}</span>
                    <vs-progress :percent="data[indextr].distPercent" :color="data[indextr].statusColor"></vs-progress>
                  </vs-td>
                  <vs-td :data="data[indextr].orderNo">
                    <span>{{data[indextr].startDate}}</span>
                  </vs-td>
                  <vs-td :data="data[indextr].orderNo">
                    <span>{{data[indextr].estDelDate}}</span>
                  </vs-td>
                </vs-tr>
              </template>
            </vs-table>
          </div>

        </vx-card>
      </div>
    </div>

  </div>
</template>

<script>
// import VuePerfectScrollbar from 'vue-perfect-scrollbar'
import VueApexCharts from 'vue-apexcharts'
import StatisticsCardLine from '@/components/statistics-cards/StatisticsCardLine.vue'
import analyticsData from '../ui-elements/card/analyticsData.js'
import ChangeTimeDurationDropdown from '@/components/ChangeTimeDurationDropdown.vue'
import VxTimeline from '@/components/timeline/VxTimeline'

export default {
  components: {
    VueApexCharts,
    StatisticsCardLine,
    // VuePerfectScrollbar,
    ChangeTimeDurationDropdown,
    VxTimeline
  },
  data () {
    return {
      subscribersGained: {},
      revenueGenerated: {},
      quarterlySales: {},
      ordersRecevied: {},

      revenueComparisonLine: {},
      goalOverview: {},

      browserStatistics: [],
      clientRetentionBar: {},

      sessionsData: {},
      chatLog: [],
      chatMsgInput: '',
      customersData: {},

      analyticsData,
      settings: { // perfectscrollbar settings
        maxScrollbarLength: 60,
        wheelSpeed: .60
      },
      timelineData: [
        {
          color: 'primary',
          icon: 'PlusIcon',
          title: 'Client Meeting',
          desc: 'Bonbon macaroon jelly beans gummi bears jelly lollipop apple',
          time: '25 mins Ago'
        },
        {
          color: 'warning',
          icon: 'MailIcon',
          title: 'Email Newsletter',
          desc: 'Cupcake gummi bears soufflé caramels candy',
          time: '15 Days Ago'
        },
        {
          color: 'danger',
          icon: 'UsersIcon',
          title: 'Plan Webinar',
          desc: 'Candy ice cream cake. Halvah gummi bears',
          time: '20 days ago'
        },
        {
          color: 'success',
          icon: 'LayoutIcon',
          title: 'Launch Website',
          desc: 'Candy ice cream cake. Halvah gummi bears Cupcake gummi bears soufflé caramels candy.',
          time: '25 days ago'
        },
        {
          color: 'primary',
          icon: 'TvIcon',
          title: 'Marketing',
          desc: 'Candy ice cream cake. Halvah gummi bears Cupcake gummi bears.',
          time: '28 days ago'
        }
      ]
    }
  },
  computed: {
    scrollbarTag () {
      return this.$store.getters.scrollbarTag
    }
  },
  mounted () {
    const scroll_el = this.$refs.chatLogPS.$el || this.$refs.chatLogPS
    scroll_el.scrollTop = this.$refs.chatLog.scrollHeight
  },
  created () {
    console.log(localStorage.getItem('userInfo'))
    // Subscribers gained - Statistics
    this.$http.get('/api/card/card-statistics/subscribers')
      .then((response) => {
        this.subscribersGained = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Revenue Generated
    this.$http.get('/api/card/card-statistics/revenue')
      .then((response) => {
        this.revenueGenerated = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Sales
    this.$http.get('/api/card/card-statistics/sales')
      .then((response) => {
        this.quarterlySales = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Orders - Statistics
    this.$http.get('/api/card/card-statistics/orders')
      .then((response) => {
        this.ordersRecevied = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Revenue Comparison
    this.$http.get('/api/card/card-analytics/revenue-comparison')
      .then((response) => {
        this.revenueComparisonLine = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Goal Overview
    this.$http.get('/api/card/card-analytics/goal-overview')
      .then((response) => {
        this.goalOverview = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Browser Analytics
    this.$http.get('/api/card/card-analytics/browser-analytics')
      .then((response) => {
        this.browserStatistics = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Client Retention
    this.$http.get('/api/card/card-analytics/client-retention')
      .then((response) => {
        this.clientRetentionBar = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Sessions By Device
    this.$http.get('/api/card/card-analytics/session-by-device')
      .then((response) => {
        this.sessionsData = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Chat Log
    this.$http.get('/api/chat/demo-1/log')
      .then((response) => {
        this.chatLog = response.data
      })
      .catch((error) => {
        console.log(error)
      })

    // Customers
    this.$http.get('/api/card/card-analytics/customers')
      .then((response) => {
        this.customersData = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }
}
</script>

<style lang="scss">
  .chat-card-log {
    height: 400px;

    .chat-sent-msg {
      background-color: #f2f4f7 !important;
    }
  }
</style>
