<template>
  <div id="page-user-stats-view">
    <pre>{{user_stats}}</pre>
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

    <vue-apex-charts ref="userChart1" type="bar" height="350" :options="chartOptions"
                     :series="series"></vue-apex-charts>
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
    processData () {
      const seasons = []
      const series = {}
      console.log('data', this.user_stats)
      // this.user_stats =
      //   {
      //     '2018-2019': {
      //       'SKI_TRAINING': {
      //         'name': 'Ski Training',
      //         'count': 1,
      //         'total': 1
      //       },
      //       'ATHLETIC_TRAINING': {
      //         'name': 'Athletic Training',
      //         'count': 1,
      //         'total': 5
      //       }
      //     },
      //     '2017-2018': {
      //       'SKI_TRAINING': {
      //         'name': 'Ski Training',
      //         'count': 5,
      //         'total': 20
      //       },
      //       'ATHLETIC_TRAINING': {
      //         'name': 'Athletic Training',
      //         'count': 15,
      //         'total': 10
      //       }
      //     }
      //   }
      Object.entries(this.user_stats).forEach(([season, data]) => {
        seasons.push(season)
        series[season] = []
        Object.entries(data).forEach(([key, value]) => {
          if (!series[season].hasOwnProperty(key)) {
            series[season][key] = { ...series[season][key], ...value }
            series[season][key] = { ...series[season][key], ...{ data: [] } }
          }
          series[season][key]['data'].push(value.count)
        })
      })
      console.log('series', series)
      console.log('seasons', seasons)
      this.$refs.userChart1.updateOptions({ xaxis: { categories: seasons } })
      console.log('***************************************************************')

      const cleanData = []
      console.log('aaaabp_cleanData', cleanData)
      Object.values(series).forEach((el) => {
        Object.entries(el).forEach(([key, value]) => {
          console.log('cleanData.some(e => e.name === key)', cleanData.some(e => e.name === value.name))

          const magenicIndex = cleanData.findIndex(vendor => vendor.name === value.name)
          if (magenicIndex > -1) {
            cleanData[magenicIndex].data.push(value.count)
          } else {
            cleanData.push({
              name: value.name,
              data: value.data
            })
          }
        })
      })
      console.log('cleanData final', cleanData)
      this.series = cleanData
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
