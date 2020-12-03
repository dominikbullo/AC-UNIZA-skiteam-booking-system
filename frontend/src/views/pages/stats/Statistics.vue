<template>
  <div id="page-users-stats-view">

    <div class="vx-row">
      <div class="vx-col w-full mb-base">
        <vx-card :title="$t('graph.total-1')">
          <vue-apex-charts ref="totalPresenceChart" type="bar" height="350"
                           :options="usersEventCountBarChart.chartOptions"
                           :series="usersEventCountBarChart.series"></vue-apex-charts>
        </vx-card>
      </div>
    </div>
  </div>
</template>

<script>
// Store Module
import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'

import VueApexCharts from 'vue-apexcharts'

// TODO: save event colors
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
      data: {},

      usersEventCountBarChart: {
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
    processData () {
      const seasons = []
      const users = []
      const series = {}
      const seasonMap = new Map()
      const eventTypeMap = new Map()

      this.data.forEach((item) => {
        console.log('forEach', item)
        // If has no datapoint
        if (!item.event_stats || Object.keys(item.event_stats).length === 0) {
          console.log('return', item)
          return
        }
        users.push(item.displayName)
        // Only if have data
        Object.entries(item.event_stats).forEach(([season, data]) => {

          if (!seasonMap.has(season)) {
            seasonMap.set(season, true)
            seasons.push(season)
            series[season] = []
          }

          console.log('season', season)
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
      this.usersEventCountBarChart.series = cleanData
    }
  },
  created () {
    if (!moduleUserManagement.isRegistered) {
      this.$store.registerModule('userManagement', moduleUserManagement)
      moduleUserManagement.isRegistered = true
    }
    this.$store.dispatch('userManagement/fetchProfileStatistics').then(res => {
      this.data = res.data.results
      this.processData()
    })
  }
}
</script>
