<template>
  <div>
    <h2>Hello from coach dashboard</h2>
    <!-- Select child -->
    <div class="vx-row">
      <div class="vx-col w-full md:w-1/2 mb-base">
        <vx-card title="Child Selection" no-shadow card-border>
          <!-- RES (DOCS): https://vue-select.org/api/props.html#getoptionlabel -->
          <v-select
            v-model="childSelection.selected"
            :options="childSelection.options"
            :clearable="false"
            :searchable="false"
            :getOptionLabel="options => options.user.profile.full_name"
            @input="getUserStats"
          />
        </vx-card>
      </div>

      <!-- Select season -->
      <div class="vx-col w-full md:w-1/2 mb-base">
        <vx-card title="Season Selection (not implemented yet)" no-shadow card-border>
          <v-select
            v-model="seasonSelection.selected"
            :options="seasonSelection.options"
            :clearable="false"
            :searchable="false"
          />
        </vx-card>
      </div>
    </div>

    <!--    &lt;!&ndash; TODO: maybe for each statictic roll out field ?&ndash;&gt;-->
    <!--    <div v-if="stats!==undefined && stats!=={}">-->
    <!--      <div class="vx-row">-->
    <!--        <div class="vx-col w-1/2 md:w-1/3 xl:w-1/6"-->
    <!--             v-for="(item, key) in stats"-->
    <!--             :key="key">-->
    <!--          <statistics-card-line-->
    <!--            class="mb-base"-->
    <!--            hideChart-->
    <!--            icon="CheckSquareIcon"-->
    <!--            :statistic="getDisplayStats(item).percent"-->
    <!--            :statisticTitle="item.name"/>-->

    <!--          <statistics-card-line-->
    <!--            class="mb-base"-->
    <!--            hideChart-->
    <!--            icon="CheckSquareIcon"-->
    <!--            :statistic="getDisplayStats(item).ratio"-->
    <!--            :statisticTitle="item.name"/>-->
    <!--        </div>-->
    <!--      </div>-->


    <div class="vx-row">
      <div class="vx-col w-full w-1/2 sm:w-1/2 lg:w-1/3 xl:w-1/4"
           v-for="(item, key) in stats"
           :key="key">
        <vx-card :title="`${item.name}`" class="mb-10">
          <template v-slot:actions>
            <feather-icon icon="HelpCircleIcon" svgClasses="w-6 h-6 text-grey"></feather-icon>
          </template>

          <!-- CHART -->
          <template slot="no-body">
            <div class="mt-10">
              <vue-apex-charts
                :options="goalOverviewRadialBar.chartOptions"
                :series=" [getDisplayStats(item).percent]"
                height="240"
                type="radialBar"/>
            </div>
          </template>
          <!-- DATA -->
          <div
            class="flex justify-between text-center mt-4"
            slot="no-body-bottom"
            v-if="true">
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0">
              <p class="mt-4">Completed</p>
              <p class="mb-4 text-3xl font-semibold">{{item.count}}</p>
            </div>
            <div class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0">
              <p class="mt-4">Total</p>
              <p class="mb-4 text-3xl font-semibold">{{item.total}}</p>
            </div>
          </div>
        </vx-card>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'
import StatisticsCardLine from '@/components/statistics-cards/StatisticsCardLine.vue'
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
      childSelection:
        {
          selected: [],
          options: []
        },

      seasonSelection:
        {
          selected: [],
          options: []
        },

      stats: {},

      settings: { // perfectscrollbar settings
        maxScrollbarLength: 60,
        wheelSpeed: 0.60
      },

      goalOverviewRadialBar: {
        // series: [83],
        chartOptions: {
          plotOptions: {
            radialBar: {
              size: 110,
              startAngle: -150,
              endAngle: 150,
              hollow: {
                size: '77%'
              },
              track: {
                background: '#bfc5cc',
                strokeWidth: '50%'
              },
              dataLabels: {
                name: {
                  show: false
                },
                value: {
                  offsetY: 18,
                  color: '#99a2ac',
                  fontSize: '4rem'
                }
              }
            }
          },
          colors: ['#ff0000'],
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'dark',
              type: 'radial',
              shadeIntensity: 0.1,
              gradientToColors: ['#00db89'],
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100]
            }
          },
          stroke: {
            lineCap: 'round'
          },
          chart: {
            sparkline: {
              enabled: true
            },
            dropShadow: {
              enabled: true,
              blur: 3,
              left: 1,
              top: 1,
              opacity: 0.1
            }
          }
        }
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
          desc: 'Cupcake gummi bears souffl?? caramels candy',
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
          desc: 'Candy ice cream cake. Halvah gummi bears Cupcake gummi bears souffl?? caramels candy.',
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
  methods: {
    getUserStats () {
      console.log('getUserStats', this.childSelection.selected)
      this.$store.dispatch('family/fetchUserStats',
        {
          username: this.childSelection.selected.user.profile.id,
          query: { season: this.seasonSelection.selected }
        })
        .then((res) => {
          // FIXME
          // console.log('res data', res.data)
          this.stats = Object.values(res.data.data)[0]
          return res.data.data
        })
    },
    getDisplayStats (stats) {
      if (stats === undefined) {
        return 'undefined'
      }
      return {
        'percent': stats.count / stats.total * 100,
        'percentStr': `${(stats.count / stats.total * 100).toFixed(2)}%`,
        'ratio': `${stats.count} / ${stats.total}`
      }
    }
  },
  computed: {
    scrollbarTag () {
      return this.$store.getters.scrollbarTag
    },
    familyChildren () {
      // console.log('family children', this.$store.getters['family/familyChildren'])
      return this.$store.getters['family/familyChildren']
    }
  },
  created () {
    console.log('user', this.$store.state.AppActiveUser)
  }
}
</script>
