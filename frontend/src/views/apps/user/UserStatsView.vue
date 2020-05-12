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
    processData () {
      const seasons = []
      const series = {}
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
          // Here is the line where in data which i want to sho i pushing values
          series[season][key]['data'].push(value.count)
        })
      })
      // console.log('series', series)
      // console.log('seasons', seasons)
      this.$refs.userChart1.updateOptions({ xaxis: { categories: seasons } })
      this.$refs.userChart2.updateOptions({ xaxis: { categories: seasons } })


      const cleanData = []
      Object.values(series).forEach((el) => {
        Object.entries(el).forEach(([key, value]) => {
          const magenicIndex = cleanData.findIndex(vendor => vendor.name === value.name)
          if (magenicIndex > -1) {
            cleanData[magenicIndex].data.push(...value.data)
          } else {
            cleanData.push({
              name: value.name,
              data: value.data
            })
          }
        })
      })
      // console.log('cleanData final', cleanData)
      this.series = cleanData
    }
  },
  created () {
    // this.$vs.loading()
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
