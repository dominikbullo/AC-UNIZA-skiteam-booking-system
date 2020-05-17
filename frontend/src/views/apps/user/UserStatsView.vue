<template>
  <div id="page-user-stats-view">
    <vs-alert color="danger" title="User Not Found" :active.sync="user_not_found">
      <span>Statistic for this user not found. </span>
    </vs-alert>

    <vue-apex-charts ref="userChart1" type="bar" height="350" :options="chartOptions"
                     :series="series"></vue-apex-charts>

    <vue-apex-charts ref="userChart2" width="300" height="300" type="donut" :options="chartOptions2"
                     :series="series2"></vue-apex-charts>

    <pre>{{user_stats}}</pre>
  </div>
</template>

<script>

import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'
import VueApexCharts from 'vue-apexcharts'

const stats = {
  count: 'count123',
  total: 'total',
  percentage: 'percentage'
}
const dataKey = 'asdasasdad'

export default {
  components: {
    VueApexCharts
  },
  data () {
    return {
      chartOptions2: {
        chart: {
          id: 'basic-donut'
        },
        labels: ['a', 'b', 'c']
      },
      series2: [30, 40, 45],
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
          // FIXME or 0
          series[season][key][dataKey][stats.percentage].push(
            (value.count / value.total * 100).toFixed(2)
          )
        })

      })
      console.log('series', series)
      return series
    },
    cleanData (series) {
      const cleanData = []
      Object.values(series).forEach((el) => {
        Object.entries(el).forEach(([key, value]) => {
          const magenicIndex = cleanData.findIndex(vendor => vendor.name === value.name)
          if (magenicIndex > -1) {
            cleanData[magenicIndex].data.push(...value[dataKey][stats.count])
          } else {
            cleanData.push({
              name: value.name,
              data: value[dataKey][stats.count]
            })
          }
        })
      })
      return cleanData
    },
    processData () {
      const series = this.formatData()
      const seasons = Object.keys(series)

      this.$refs.userChart1.updateOptions({ xaxis: { categories: seasons } })

      this.series = this.cleanData(series)
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
