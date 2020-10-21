<template>
  <div id="page-user-stats-view">
    <vs-alert color="danger" title="User Not Found" v-model:active="user_not_found">
      <span>Statistic for this user not found. </span>
    </vs-alert>

    <div class="vx-row">

      <div class="vx-col w-full mb-base">
        <vx-card :title="$t('graph.user-1')">
          <vue-apex-charts ref="userChart1" type="bar" height="350" :options="chartOptions"
                           :series="series"></vue-apex-charts>
        </vx-card>
      </div>
    </div>
    <vx-card>
      <div class="vx-row">
        <div class="vx-col w-full md:w-1/2 mb-base">
          <vx-card :title="$t('Season Selection')" no-shadow card-border>
            <v-select
              v-model="seasons.selected"
              :options="seasons.options"
              @input="seasonStats"
              :clearable="false"
            />
          </vx-card>
        </div>
      </div>

      <div class="vx-row">
        <div class="vx-col w-full md:w-1/2 mb-base">
          <vx-card :title="$t('graph.user-2')" card-border>
            <vue-apex-charts ref="radialBar" type="radialBar" height="350" :options="chartOptionsRadial"
                             :series="radialChartSeries"></vue-apex-charts>
          </vx-card>
        </div>

        <div class="vx-col w-full md:w-1/2 mb-base">
          <vx-card :title="$t('graph.user-3')" card-border>
            <vue-apex-charts ref="userChart2" height="350" type="pie" :options="chartOptions2"
                             :series="series2"></vue-apex-charts>
          </vx-card>
        </div>
      </div>
    </vx-card>
  </div>
</template>

<script>

import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'
import VueApexCharts from 'vue-apexcharts'
import vSelect from 'vue-select'

const themeColors = [
  '#008FFB',
  '#7367f0',
  '#EA5455',
  '#28C76F',
  '#FF9F43',
  '#ff00c8'
]

const stats = {
  count: 'count',
  total: 'total',
  percentage: 'percentage'
}
const dataKey = 'data'

export default {
  components: {
    VueApexCharts,
    'v-select': vSelect
  },
  data () {
    return {
      seasons: {
        selected: '',
        options: []
      },
      radialChartSeries: [],
      chartOptionsRadial: {
        colors: themeColors,
        tooltip: {
          theme: 'dark'
        },
        legend: {
          position: 'top',
          horizontalAlign: 'left'
        },
        chart: {
          height: 350,
          type: 'radialBar'
        },
        plotOptions: {
          radialBar: {
            dataLabels: {
              name: {
                fontSize: '22px'
              },
              value: {
                fontSize: '16px'
              }
            }
          }
        },
        labels: []
      },
      chartOptions2: {
        colors: themeColors,
        tooltip: {
          theme: 'dark'
        },
        chart: {
          id: 'basic-donut'
        },
        labels: [],
        legend: {
          position: 'right',
          horizontalAlign: 'left'
        }
      },
      series2: [],
      series: [],
      chartOptions: {
        colors: themeColors,
        tooltip: {
          theme: 'dark'
        },
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
  methods: {
    formatData () {
      const series = {}

      Object.keys(this.user_stats).forEach((season) => {
        series[season] = []

        Object.entries(this.user_stats[season]).forEach(([key, value]) => {
          if (!series[season].hasOwnProperty(key)) {

            value[dataKey] = {}
            series[season][key] = { ...series[season][key], ...value }

            Object.values(stats).forEach((item) => {
              series[season][key][dataKey][item] = []
            })
          }
          // Here is the line where in data which i want to sho i pushing values
          series[season][key][dataKey][stats.count].push(value.count)
          series[season][key][dataKey][stats.total].push(value.total)
          series[season][key][dataKey][stats.total].push(value.total)
          // FIXME or 0
          series[season][key][dataKey][stats.percentage].push(
            (value.count / value.total * 100).toFixed(2)
          )
        })

      })
      console.log('series', series)
      return series
    },

    cleanData (dataToClean, key = stats.count) {
      const cleanData = []
      Object.values(dataToClean).forEach((el) => {
        Object.entries(el).forEach(([key123, value]) => {
          const magenicIndex = cleanData.findIndex(vendor => vendor.name === value.name)
          if (magenicIndex > -1) {
            cleanData[magenicIndex].data.push(...value[dataKey][key])
          } else {
            cleanData.push({
              name: value.name,
              data: value[dataKey][key]
            })
          }
        })
      })
      return cleanData
    },
    seasonStats () {

      this.series2 = []
      this.radialChartSeries = []
      const names = []

      Object.values(this.myStatData[this.seasons.selected]).forEach(item => {
        names.push(item.name)
        this.series2.push(item.count)
        this.radialChartSeries.push((item.count / item.total * 100).toFixed(2))
      })
      this.$refs.userChart2.updateOptions({ labels: names })
      this.$refs.radialBar.updateOptions({ labels: names })

    },
    processData () {
      this.myStatData = this.formatData()
      this.seasons.options = Object.keys(this.myStatData)
      this.seasons.selected = this.seasons.options[0]

      this.$refs.userChart1.updateOptions({ xaxis: { categories: Object.keys(this.myStatData) } })
      this.series = this.cleanData(this.myStatData)
      this.seasonStats()
      this.$vs.loading.close()
    }
  },
  created () {
    this.$vs.loading()
    if (!moduleUserManagement.isRegistered) {
      this.$store.registerModule('userManagement', moduleUserManagement)
      moduleUserManagement.isRegistered = true
    }
    this.$store.dispatch('family/fetchUserStats',
      {
        username: this.$route.params.userId
      })
      .then(res => {
        // this.$vs.loading.close()
        this.user_stats = res.data.data
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
