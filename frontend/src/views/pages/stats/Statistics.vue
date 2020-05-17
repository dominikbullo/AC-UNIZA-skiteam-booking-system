<template>
  <div id="page-users-stats-view">

    <!--    <vs-button v-on:click="changeChart">Update</vs-button>-->
    <!--    <vs-button v-on:click=" processData">Process</vs-button>-->
    <!--    <vue-apex-charts width="300" height="300" type="donut" :options="chartOptions" :series="series"></vue-apex-charts>-->

    <div class="vx-row">
      <div class="vx-col w-full mb-base">
        <vx-card title="Number of event of child in actual season">
          <vue-apex-charts ref="totalPresenceChart" type="bar" height="350" :options="barChart.chartOptions"
                           :series="barChart.series"></vue-apex-charts>
        </vx-card>
      </div>

      <!--      <div class="vx-col w-full mb-base">-->
      <!--        <vx-card title="Number of event of child in season">-->
      <!--          <vue-apex-charts ref="usersChartCount" type="bar" height="450"-->
      <!--                           :options="chartOptions" :series="seriesCount"></vue-apex-charts>-->
      <!--        </vx-card>-->
      <!--      </div>-->
    </div>
  </div>
</template>

<script>
// Store Module
import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'

import VueApexCharts from 'vue-apexcharts'

const themeColors = [
  '#008FFB',
  '#7367f0',
  '#EA5455',
  '#28C76F',
  '#FF9F43',
  '#ff00c8'
]
export default {
  components: {
    VueApexCharts
  },
  data () {
    return {
      usersData: {},
      chartOptions: {
        chart: {
          type: 'bar',
          height: 350,
          stacked: true,
          toolbar: {
            show: true
          },
          zoom: {
            enabled: true
          }
        },
        responsive: [{
          breakpoint: 480,
          options: {
            legend: {
              position: 'bottom',
              offsetX: -10,
              offsetY: 0
            }
          }
        }],
        plotOptions: {
          bar: {
            horizontal: false
          }
        },
        xaxis: {
          type: 'datetime',
          categories: [
            '01/01/2011 GMT', '01/02/2011 GMT', '01/03/2011 GMT', '01/04/2011 GMT', '01/05/2011 GMT', '01/06/2011 GMT'
          ]
        },
        legend: {
          position: 'right',
          offsetY: 40
        },
        fill: {
          opacity: 1
        }
      },
      seriesCount: [
        {
          name: 'Inflation',
          data: [2.3, 3.1, 4.0, 10.1, 4.0, 3.6, 3.2, 2.3, 1.4, 0.8, 0.5, 0.2]
        }
      ],


      barChart: {
        chart: {
          id: 'children-chart-1'
        },
        series: [],
        chartOptions: {
          colors: themeColors,
          dataLabels: {
            enabled: false
          },
          xaxis: {
            categories: []
          },
          tooltip: {
            theme: 'dark',
            y: {
              formatter (val) {
                return val
              }
            }
          }
        }
      }
    }
  },
  methods: {
    processData2 () {
      const categories = []
      const uniqueSeasonInData = []
      const uniqueEventTypeInData = []
      let entries = {}
      const seasonMap = new Map()
      const eventTypeMap = new Map()

      this.usersData.forEach((el) => {
        categories.push(el.user.displayName)
        Object.entries(el.data).forEach(([seasonKey, seasonData]) => {
          Object.entries(seasonData).forEach(([eventTypeKey, eventTypeData]) => {
            if (!eventTypeMap.has(eventTypeKey)) {
              eventTypeMap.set(eventTypeKey, true)
              uniqueEventTypeInData.push(eventTypeKey)
              entries = { ...entries, ...eventTypeData }
              // series[season][key] = { ...series[season][key], ...{ data: [] } }
              // Here is the line where in data which i want to sho i pushing values
              entries.push({
                count: eventTypeData.count,
                total: eventTypeData.total
              })
              // entries[eventTypeKey].count.push('testCount')
              // series[season][key]['data'].push(value.count)
            }
          })

          if (!seasonMap.has(seasonKey)) {
            seasonMap.set(seasonKey, true)
            uniqueSeasonInData.push(seasonKey)
            entries.push({
              id: el.id,
              count: seasonData.count,
              total: seasonData.total
            })
          } else {
            console.log('pushi************************ng', el)
            console.log(entries)
            // entries[key].count.push('testCount')
            // entries[key].total.push('testTotal')
          }
        })
      })
      // Season
      console.log('uniqueSeasonInData', uniqueSeasonInData)
      console.log('uniqueEventTypeInData', uniqueEventTypeInData)
      console.log('categories', categories)
      console.log('entries', entries)
    },
    processData () {
      const seasons = []
      const users = []
      const series = {}
      const seasonMap = new Map()
      const eventTypeMap = new Map()

      this.usersData.forEach((user) => {
        // If has no datapoint
        if (Object.keys(user.data).length === 0) {
          return
        }
        users.push(user.user.displayName)
        // Only if have data
        Object.entries(user.data).forEach(([season, data]) => {

          if (!seasonMap.has(season)) {
            seasonMap.set(season, true)
            seasons.push(season)
            series[season] = []
          }

          // console.log('season', season)
          Object.entries(data).forEach(([key, value]) => {


            // console.log('series[season][key] BP', series[season][key])
            if (!series[season].hasOwnProperty(key)) {
              series[season][key] = { ...series[season][key], ...value }
              series[season][key] = { ...series[season][key], ...{ data: [] } }
              // console.log('series[season][key] if', series[season][key])
            }

            // Here is the line where in data which i want to sho i pushing values
            series[season][key]['data'].push(value.count)
            // console.log('series[season][key] data push', series[season][key])
          })
        })
      })
      this.$refs.totalPresenceChart.updateOptions({ xaxis: { categories: users } })
      console.log('series', series)

      // It working as expected until this -> don't touch it!

      const cleanData = []
      // TODO select season
      Object.values(series[seasons[0]]).forEach((el) => {
        // Object.entries(el).forEach(([key, value]) => {
        //   // FIXME thi is always -1
        //   const magenicIndex = cleanData.findIndex(vendor => vendor[key] === value)
        //   if (magenicIndex > -1) {
        //     cleanData[magenicIndex].data.push(...el.data)
        //   } else {
        cleanData.push({
          name: el.name,
          data: el.data
        })
        // }
        // })
      })
      console.log('cleanData final', cleanData)
      this.barChart.series = cleanData
    },
    changeChart () {
      this.series = [10, 20, 30]
      this.chartOptions.labels = ['d', 'e', 'f']

      // https://github.com/apexcharts/vue-apexcharts
      this.$refs.totalPresenceChart.updateOptions({
        xaxis: { categories: ['Jožko', 'Marienka', 'Zuzka'] }
      })

      this.barChart.series = [
        {
          name: 'Ski training',
          data: [50, 20, 30]
        },
        {
          name: 'Ski Race',
          data: [5, 6, 7]
        }
      ]
    }
  },
  created () {
    if (!moduleUserManagement.isRegistered) {
      this.$store.registerModule('userManagement', moduleUserManagement)
      moduleUserManagement.isRegistered = true
    }
    this.$store.dispatch('userManagement/fetchChildrenStatistics').then(res => {
      this.usersData = res.data
      this.processData()
    })
  }
}
</script>
