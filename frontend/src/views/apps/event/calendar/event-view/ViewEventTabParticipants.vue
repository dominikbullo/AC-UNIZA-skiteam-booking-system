<template>
  <div id="event-calendar-view-event-tab-general">
    <div class="vx-row">

      <!--      <table class="vx-col flex-1" :key="category.id" v-for="category in mergedResponses">-->
      <!--        &lt;!&ndash; TODO: There must be some component, there is no way to display 30 members as plane table&ndash;&gt;-->
      <!--        <thead>-->
      <!--        <tr>-->
      <!--          <th class="vx-col h-12" colspan="2">{{ category.displayName }}</th>-->
      <!--        </tr>-->
      <!--        </thead>-->
      <!--        <tbody>-->
      <!--        <tr v-for="child in category.members">-->
      <!--          <th>{{ child }}</th>-->
      <!--          <th>true</th>-->
      <!--        </tr>-->
      <!--        </tbody>-->
      <!--      </table>-->

      <vs-table class="vx-col w-1/5 flex-1" :data="this.mergedResponses">
        <template slot="thead">
          <vs-th>{{ $t('Name') }}</vs-th>
          <vs-th>{{ $t('Response') }}</vs-th>
        </template>
        <template slot-scope="{data}">
          <vs-tr :state="data[indextr].going === true ? 'success':data[indextr].going===false? 'danger':null"
                 :key="indextr"
                 v-for="(tr, indextr) in data">
            <vs-td :data="data[indextr].user_to_event.displayName">
              {{ data[indextr].user_to_event.displayName }}
            </vs-td>
            <vs-td :data="data[indextr].id">
              {{ data[indextr].going === true ? $t('Going') : data[indextr].going === false ? $t('Not going') : ' ' }}
            </vs-td>
          </vs-tr>
        </template>
      </vs-table>

      <!--      <table class="vx-col flex-1" :key="category.id" v-for="category in this.categories">-->
      <!--        &lt;!&ndash; TODO: There must be some component, there is no way to display 30 members as plane table&ndash;&gt;-->
      <!--        <thead>-->
      <!--        <tr>-->
      <!--          <th class="vx-col h-12" colspan="2">{{ category.displayName }}</th>-->
      <!--        </tr>-->
      <!--        </thead>-->
      <!--        <tbody>-->
      <!--        <tr v-for="child in category.members">-->
      <!--          <th>{{ child }}</th>-->
      <!--          <th>true</th>-->
      <!--        </tr>-->
      <!--        </tbody>-->
      <!--      </table>-->
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
      categories: []
    }
  },
  computed: {
    event () {
      return this.$store.getters['calendar/getEvent'](this.data.id)
    },
    mergedResponses () {
      return this.$store.getters['calendar/getEventMergedResponses'](this.data.id).filter(x => x.user_to_event.user_role === 'child')
    }
  },
  methods: {
    displayObject (object, displayKey = 'displayName') {
      return Object.values(object).map(item => item[displayKey]).toString()
    }
  }
}
</script>
