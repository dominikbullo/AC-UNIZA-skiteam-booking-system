<template>
  <div id="page-user-stats-view">
    <ul>
      <li v-for="(value, key) in user_data" :key="`fruit-${key}`">
        <h1>Season {{key}}</h1>
        {{ value }}
      </li>
    </ul>

    <!--    <vue-apex-charts type="bar" height="350" :options="barChart.chartOptions"-->
    <!--                     :series="barChart.series"></vue-apex-charts>-->

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
      series: [{
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
      }],
      chartOptions: {
        chart: {
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
          categories: ['2018-2019', '2017-2018', '2016-2017', '2015-2016', '2014-2015', '2013-2014'],
          labels: {
            formatter: function (val) {
              return val
            }
          }
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
      themeColors: ['#7367F0', '#28C76F', '#EA5455', '#FF9F43', '#1E1E1E'],
      barChart: {
        series: [{
          data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
        }],
        chartOptions: {
          colors: this.themeColors,
          plotOptions: {
            bar: {
              horizontal: true
            }
          },
          dataLabels: {
            enabled: false
          },
          xaxis: {
            categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
              'United States', 'China', 'Germany']
          }
        }
      },
      user_data: null,
      user_not_found: false
    }
  },
  computed: {
    userAddress () {
      let str = ''
      for (const field in this.user_data.location) {
        str += `${field} `
      }
      return str
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
        this.user_data = res.data
      })
      .catch(err => {
        if (err.response.status === 404) {
          this.user_not_found = true
        }
        console.error(err)
      })
      .finally(() => {
        this.$vs.loading.close()
      })
  }
}

</script>
