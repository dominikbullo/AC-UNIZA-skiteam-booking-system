<!-- =========================================================================================
  File Name: UserView.vue
  Description: User View page
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div id="page-user-stats-view">

    {{usersData}}

    <vue-apex-charts type="bar" height="350" :options="barChart.chartOptions"
                     :series="barChart.series"></vue-apex-charts>
  </div>
</template>

<script>
// Store Module
import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'

import VueApexCharts from 'vue-apexcharts'

export default {
  components: {
    VueApexCharts
  },
  data () {
    return {
      barChart: {
        series: [{
          data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
        }],
        chartOptions: {
          dataLabels: {
            enabled: false
          },
          xaxis: {
            categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
              'United States', 'China', 'Germany']
          }
        }
      }
    }
  },
  computed: {
    usersData () {
      return this.$store.state.userManagement.users
    }
  },
  methods: {
    created () {
      this.$store.registerModule('userManagement', moduleUserManagement)
      this.$store.dispatch('userManagement/fetchUsers')
    }
  }
}
</script>
