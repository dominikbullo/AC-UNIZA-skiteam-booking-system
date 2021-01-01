<template>
  <div id="event-calendar-view-event-tab-general">
    <div class="vx-row">
      <!--      <vs-table class="vx-col w-1/5 flex-1" :key="item.id" v-for="item in this.data.category" :data="item">-->
      <!--        <template slot="thead">-->
      <!--          <vs-th>Name</vs-th>-->
      <!--          <vs-th>Response</vs-th>-->
      <!--        </template>-->
      <!--        <template slot-scope="{data}">-->
      <!--          <vs-tr :state="indextr == 2 || indextr == 5 ? 'success':indextr == 6 ? 'danger':null" :key="indextr"-->
      <!--                 v-for="(tr, indextr) in data">-->
      <!--            <vs-td :data="data[indextr].displayName">-->
      <!--              {{ data[indextr].displayName }}-->
      <!--            </vs-td>-->
      <!--            <vs-td :data="data[indextr].id">-->
      <!--              {{ data[indextr].id }}-->
      <!--            </vs-td>-->
      <!--          </vs-tr>-->
      <!--        </template>-->
      <!--      </vs-table>-->

      <table class="vx-col flex-1" :key="item.id" v-for="item in this.localCategory">
        <!-- TODO: There must be some component, there is no way to display 30 members as plane table-->
        <thead>
        <tr>
          <th class="vx-col h-12" colspan="2">{{ item.displayName }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in 7">
          <th>test</th>
          <th>true</th>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    data: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      children: [],
      localCategory: []
    }
  },
  computed: {
    event () {
      return this.$store.getters['calendar/getEvent'](this.data.id)
    }
    // mergedResponses () {
    //   return this.$store.getters['calendar/getEventMergedResponses'](this.data.id)
    // }
  },
  methods: {
    displayObject (object, displayKey = 'displayName') {
      return Object.values(object).map(item => item[displayKey]).toString()
    }
  },
  created () {
    this.$http.get('/children').then(res => {
      console.log(res.data.results)
      this.children = res.data.results
    }).catch(error => console.log(error))

    // sort categories by year from
    this.localCategory = this.data.category.sort(function (a, b) {
      const keyA = new Date(a.year_from), keyB = new Date(b.year_from)
      // Compare the 2 dates
      if (keyA < keyB) return 1
      if (keyA > keyB) return -1
      return 0
    })

    console.log(this.localCategory)
  }
}
</script>
