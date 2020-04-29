<template>
  <div id="page-user-stats-view">
    <vs-alert color="danger" title="User Not Found" :active.sync="user_not_found">
      <span>Statistic for this user not found. </span>
    </vs-alert>

    <!--    <div class="vx-row">-->
    <!--      <div class="vx-col w-full w-1/2 sm:w-1/2 lg:w-1/3"-->
    <!--           v-for="(item, key) in user_stats"-->
    <!--           :key="key">-->
    <!--        <vx-card :title="`${item.name}`" class="mb-10">-->
    <!--          <template slot="actions">-->
    <!--            <feather-icon icon="HelpCircleIcon" svgClasses="w-6 h-6 text-grey"></feather-icon>-->
    <!--          </template>-->

    <!--          &lt;!&ndash; CHART &ndash;&gt;-->
    <!--          <template slot="no-body">-->
    <!--            <div class="mt-10">-->
    <!--              <vue-apex-charts-->
    <!--                :options="goalOverviewRadialBar.chartOptions"-->
    <!--                :series="[28]"-->
    <!--                height="240"-->
    <!--                type="radialBar"/>-->
    <!--            </div>-->
    <!--          </template>-->
    <!--          &lt;!&ndash; DATA &ndash;&gt;-->
    <!--          <div-->
    <!--            class="flex justify-between text-center mt-4"-->
    <!--            slot="no-body-bottom"-->
    <!--            v-if="true">-->
    <!--            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0">-->
    <!--              <p class="mt-4">Completed</p>-->
    <!--              <p class="mb-4 text-3xl font-semibold">{{item.count}}</p>-->
    <!--            </div>-->
    <!--            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">-->
    <!--              <p class="mt-4">Total</p>-->
    <!--              <p class="mb-4 text-3xl font-semibold">{{item.total}}</p>-->
    <!--            </div>-->
    <!--          </div>-->
    <!--        </vx-card>-->
    <!--      </div>-->
    <!--    </div>-->

    <vue-apex-charts type="bar" height="350" :options="chartOptions" :series="series"></vue-apex-charts>
  </div>
</template>

<script>

import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'
import VueApexCharts from 'vue-apexcharts'

export default {
  components: {
    VueApexCharts
  },
  data () {
    return {
      series: [],
      chartOptions: {
        chart: {
          id: 'chart1',
          type: 'bar',
          height: 350,
          stacked: true
        },
        plotOptions: {
          bar: {
            horizontal: true
          }
        },
        stroke: {
          width: 1,
          colors: ['#fff']
        },
        xaxis: {
          categories: []// filled later
        },
        yaxis: {
          title: {
            text: undefined
          }
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return val
            }
          }
        },
        fill: {
          opacity: 1
        },
        legend: {
          position: 'top',
          horizontalAlign: 'left',
          offsetX: 40
        }
      },
      user_stats: null,
      user_not_found: false
    }
  },
  computed: {
    userAddress () {
      let str = ''
      for (const field in this.user_stats.location) {
        str += `${field} `
      }
      return str
    }
  },
  methods: {
    async changeCategories (data) {
      ApexCharts.exec('chart1', 'updateOptions', {
        xaxis: {
          categories: data
        }
      })
    },
    async processData () {
      // TODO return data via server, this must be the best way smt like /stats/summary/
      // this.$vs.loading()
      const categories = []
      const data = []
      const series = []

      const testUserData = {
        '2018-2019': {
          'SKI_TRAINING': {
            'name': 'Ski Training',
            'count': 3,
            'total': 3
          },
          'ATHLETIC_TRAINING': {
            'name': 'Athletic Training',
            'count': 0,
            'total': 1
          },
          'SKI_RACE': {
            'name': 'Ski Race',
            'count': 1,
            'total': 2
          },
          'SKI_CAMP': {
            'name': 'Ski Camp',
            'count': 0,
            'total': 0
          },
          'VIDEO_ANALYZE': {
            'name': 'Video Analyze',
            'count': 1,
            'total': 1
          },
          'MEETING': {
            'name': 'Meeting',
            'count': 0,
            'total': 0
          }
        },
        '2017-2018': {
          'SKI_TRAINING': {
            'name': 'Ski Training',
            'count': 0,
            'total': 0
          },
          'ATHLETIC_TRAINING': {
            'name': 'Athletic Training',
            'count': 1,
            'total': 0
          },
          'SKI_RACE': {
            'name': 'Ski Race',
            'count': 1,
            'total': 1
          },
          'SKI_CAMP': {
            'name': 'Ski Camp',
            'count': 0,
            'total': 0
          },
          'VIDEO_ANALYZE': {
            'name': 'Video Analyze',
            'count': 0,
            'total': 0
          },
          'MEETING': {
            'name': 'Meeting',
            'count': 0,
            'total': 0
          }
        }
      }

      for (const [season, stats] of Object.entries(testUserData)) {
        categories.push(season)
        console.log(`Value of ${season}: ${stats}`)
        for (const [key, value] of Object.entries(stats)) {
          console.log(`Value of ${key}: ${value}`)
          if (!series.hasOwnProperty(key)) {
            series[key] = {
              name: value.name,
              data: []
            }
          }
          series[key]['data'].push(value.count)
        }
      }
      const demo = [{
        name: 'Ski Training',
        data: [44, 55, 41, 37, 22, 43, 21]
      }, {
        name: 'Ski Race',
        data: [53, 32, 33, 52, 13, 43, 32]
      }, {
        name: 'Ski Camp',
        data: [44, 55, 41, 37, 22, 43, 21]
      }, {
        name: 'Athletic Training',
        data: [53, 32, 33, 52, 13, 43, 32]
      }, {
        name: 'Meeting',
        data: [12, 17, 11, 9, 15, 11, 20]
      }, {
        name: 'Video Analyze',
        data: [9, 7, 5, 8, 6, 9, 4]
      }]
      console.log('categories', categories)
      await this.changeCategories(categories)
      console.log('series', series)
      console.log('demo', demo)

      const cleanData = []
      Object.values(series).forEach((element) => {
        cleanData.unshift(element)
      })
      this.series = cleanData
      // this.$vs.loading.close()
    }
  },
  created () {
    // this.$vs.loading()
    if (!moduleUserManagement.isRegistered) {
      this.$store.registerModule('userManagement', moduleUserManagement)
      moduleUserManagement.isRegistered = true
    }
    // TODO: Do it on server and return data in correct format like this
    // this.$store.dispatch('family/fetchCompleteUserStatsGraph'
    //      const demo = [{
    //        name: 'Ski Training',
    //        data: [44, 55, 41, 37, 22, 43, 21]
    //      }, {
    //        name: 'Ski Race',
    //        data: [53, 32, 33, 52, 13, 43, 32]
    //      }]

    this.$store.dispatch('family/fetchUserStats',
      {
        username: this.$route.params.userId
      })
      .then(res => {
        // this.$vs.loading.close()
        this.user_stats = res.data
        this.processData()
      })
      .catch(err => {
        this.$vs.loading.close()
        console.error(err)
        if (err.response.status === 400) {
          this.user_not_found = true
        }
      })

  }
}

</script>
