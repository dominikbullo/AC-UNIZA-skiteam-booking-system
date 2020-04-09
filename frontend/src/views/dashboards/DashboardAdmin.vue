<template>
  <div>
    <!-- Select child -->
    <div class="vx-row">
      <div class="vx-col w-full mb-base">
        <vx-card title="Single/Multiple Selection" code-toggler no-shadow card-border>

          <div>

            <p class="mb-3">By default, vue-select supports choosing a single value. If you need multiple values, use
              the
              multiple prop</p>

            <v-select multiple
                      :closeOnSelect="false"
                      v-model="selected"
                      :options="options"
                      :dir="$vs.rtl ? 'rtl' : 'ltr'"/>
            <br>

          </div>
        </vx-card>
      </div>
    </div>

    <!-- Stats -->
    <div class="vx-row">
      <div class="vx-col w-1/2 md:w-1/3 xl:w-1/6">
        <statistics-card-line
          class="mb-base"
          hideChart
          icon="EyeIcon"
          statistic="36.9k"
          statisticTitle="Snow trainings"/>
      </div>

      <div class="vx-col w-1/2 md:w-1/3 xl:w-1/6">
        <statistics-card-line
          class="mb-base"
          color="success"
          hideChart
          icon="MessageSquareIcon"
          statistic="12k"
          statisticTitle="Trainings"/>
      </div>

      <div class="vx-col w-1/2 md:w-1/3 xl:w-1/6">
        <statistics-card-line
          class="mb-base"
          color="warning"
          hideChart
          icon="ShoppingBagIcon"
          statistic="978"
          statisticTitle="U8/U10 races"/>
      </div>

      <div class="vx-col w-1/2 md:w-1/3 xl:w-1/6">
        <statistics-card-line
          class="mb-base"
          color="danger"
          hideChart
          icon="HeartIcon"
          statistic="26.8k"
          statisticTitle="U12/U14 races"/>
      </div>

      <div class="vx-col w-1/2 md:w-1/3 xl:w-1/6">
        <statistics-card-line
          class="mb-base"
          color="success"
          hideChart
          icon="SmileIcon"
          statistic="689"
          statisticTitle="public races"/>
      </div>

      <div class="vx-col w-1/2 md:w-1/3 xl:w-1/6">
        <statistics-card-line
          class="mb-base"
          color="warning"
          hideChart
          icon="TruckIcon"
          statistic="2"
          statisticTitle="Total members"/>
      </div>
    </div>


    <div class="vx-row">
      <!-- RADIAL CHART -->
      <div class="vx-col w-full sm:w-1/2 md:w-1/3 mb-base">
        <vx-card title="Trainings Overview">
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
              <p class="mt-4">Total</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.inProgress.toLocaleString() }}</p>
            </div>
          </div>
          <div
            class="flex justify-between text-center mt-4"
            slot="no-body-bottom"
            v-if="goalOverview.analyticsData">
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0">
              <p class="mt-4">Snow</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.completed.toLocaleString() }}</p>
            </div>
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">
              <p class="mt-4">Total</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.inProgress.toLocaleString() }}</p>
            </div>
          </div>
          <div
            class="flex justify-between text-center mt-4"
            slot="no-body-bottom"
            v-if="goalOverview.analyticsData">
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0">
              <p class="mt-4">Other</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.completed.toLocaleString() }}</p>
            </div>
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">
              <p class="mt-4">Total</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.inProgress.toLocaleString() }}</p>
            </div>
          </div>
        </vx-card>
      </div>
      <!-- RADIAL CHART -->
      <div class="vx-col w-full sm:w-1/2 md:w-1/3 mb-base">
        <vx-card title="Race Overview">
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
              <p class="mt-4">Completed total</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.completed.toLocaleString() }}</p>
            </div>
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">
              <p class="mt-4">Total</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.inProgress.toLocaleString() }}</p>
            </div>
          </div>
          <div
            class="flex justify-between text-center mt-4"
            slot="no-body-bottom"
            v-if="goalOverview.analyticsData">
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0">
              <p class="mt-4">SLA</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.completed.toLocaleString() }}</p>
            </div>
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">
              <p class="mt-4">Total</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.inProgress.toLocaleString() }}</p>
            </div>
          </div>
          <div
            class="flex justify-between text-center mt-4"
            slot="no-body-bottom"
            v-if="goalOverview.analyticsData">
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0">
              <p class="mt-4">ZSL</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.completed.toLocaleString() }}</p>
            </div>
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">
              <p class="mt-4">Total</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.inProgress.toLocaleString() }}</p>
            </div>
          </div>
          <div
            class="flex justify-between text-center mt-4"
            slot="no-body-bottom"
            v-if="goalOverview.analyticsData">
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0">
              <p class="mt-4">Public</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.completed.toLocaleString() }}</p>
            </div>
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">
              <p class="mt-4">Total</p>
              <p class="mb-4 text-3xl font-semibold">{{ goalOverview.analyticsData.inProgress.toLocaleString() }}</p>
            </div>
          </div>
        </vx-card>
      </div>

      <div class="vx-col w-full sm:w-1/3 md:w-
      1/3 mb-base">
        <vx-card title="Activity Timeline">
          <vx-timeline :data="timelineData"></vx-timeline>
        </vx-card>
      </div>
    </div>

    <!--    <div class="vx-row">-->
    <!--      &lt;!&ndash; CARD 9: DISPATCHED ORDERS &ndash;&gt;-->
    <!--      <div class="vx-col w-full mb-base">-->
    <!--        <vx-card title="Child list">-->
    <!--          <div class="mt-4" slot="no-body">-->
    <!--            <vs-table :data="dispatchedOrders" class="table-dark-inverted">-->
    <!--              <template slot="thead">-->
    <!--                <vs-th>ORDER NO.</vs-th>-->
    <!--                <vs-th>STATUS</vs-th>-->
    <!--                <vs-th>OPERATORS</vs-th>-->
    <!--                <vs-th>LOCATION</vs-th>-->
    <!--                <vs-th>DISTANCE</vs-th>-->
    <!--                <vs-th>START DATE</vs-th>-->
    <!--                <vs-th>EST DELIVERY DATE</vs-th>-->
    <!--              </template>-->

    <!--              <template slot-scope="{data}">-->
    <!--                <vs-tr :key="indextr" v-for="(tr, indextr) in data">-->
    <!--                  <vs-td :data="data[indextr].orderNo">-->
    <!--                    <span>#{{data[indextr].orderNo}}</span>-->
    <!--                  </vs-td>-->
    <!--                  <vs-td :data="data[indextr].status">-->
    <!--                        <span class="flex items-center px-2 py-1 rounded"><div-->
    <!--                          :class="'bg-' + data[indextr].statusColor"-->
    <!--                          class="h-3 w-3 rounded-full mr-2"></div>{{data[indextr].status}}</span>-->
    <!--                  </vs-td>-->
    <!--                  <vs-td :data="data[indextr].orderNo">-->
    <!--                    <ul class="users-liked user-list">-->
    <!--                      <li :key="userIndex" v-for="(user, userIndex) in data[indextr].usersLiked">-->
    <!--                        <vx-tooltip :text="user.name" position="bottom">-->
    <!--                          <vs-avatar :src="user.img" class="border-2 border-white border-solid -m-1"-->
    <!--                                     size="30px"></vs-avatar>-->
    <!--                        </vx-tooltip>-->
    <!--                      </li>-->
    <!--                    </ul>-->
    <!--                  </vs-td>-->
    <!--                  <vs-td :data="data[indextr].orderNo">-->
    <!--                    <span>{{data[indextr].location}}</span>-->
    <!--                  </vs-td>-->
    <!--                  <vs-td :data="data[indextr].orderNo">-->
    <!--                    <span>{{data[indextr].distance}}</span>-->
    <!--                    <vs-progress :color="data[indextr].statusColor" :percent="data[indextr].distPercent"></vs-progress>-->
    <!--                  </vs-td>-->
    <!--                  <vs-td :data="data[indextr].orderNo">-->
    <!--                    <span>{{data[indextr].startDate}}</span>-->
    <!--                  </vs-td>-->
    <!--                  <vs-td :data="data[indextr].orderNo">-->
    <!--                    <span>{{data[indextr].estDelDate}}</span>-->
    <!--                  </vs-td>-->
    <!--                </vs-tr>-->
    <!--              </template>-->
    <!--            </vs-table>-->
    <!--          </div>-->

    <!--        </vx-card>-->
    <!--      </div>-->
    <!--    </div>-->

  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'
import StatisticsCardLine from '@/components/statistics-cards/StatisticsCardLine.vue'
import analyticsData from '../ui-elements/card/analyticsData.js'
import ChangeTimeDurationDropdown from '@/components/ChangeTimeDurationDropdown.vue'
import VxTimeline from '@/components/timeline/VxTimeline'
import vSelect from 'vue-select'

export default {
  components: {
    VueApexCharts,
    StatisticsCardLine,
    // VuePerfectScrollbar,
    ChangeTimeDurationDropdown,
    VxTimeline,
    'v-select': vSelect
  },
  data () {
    return {
      selected: ['foo'],
      options: ['foo', 'bar', 'baz'],

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

      stats: {},

      analyticsData,
      settings: { // perfectscrollbar settings
        maxScrollbarLength: 60,
        wheelSpeed: 0.60
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
  created () {
    this.$store.dispatch('family/fetchFamily', this.$store.state.AppActiveUser.profile.family_id)
    this.$store.dispatch('family/fetchUserStats', { username: 'testsets' })
  }
}
</script>
