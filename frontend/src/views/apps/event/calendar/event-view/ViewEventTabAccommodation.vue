<template>
  <div id="event-calendar-view-event-tab-accommodation">

    <vs-table ref="table" :data="data.accommodation">
      <template slot="thead">
        <vs-th sort-key="name">Name</vs-th>
        <vs-th sort-key="from">From</vs-th>
        <vs-th sort-key="to">To</vs-th>
        <vs-th sort-key="price">Price adult</vs-th>
        <vs-th sort-key="price-child">Price child</vs-th>
        <vs-th>Action</vs-th>
      </template>

      <template slot-scope="{data}">
        <tbody>
        <vs-tr :data="tr" :key="indextr" v-for="(tr, indextr) in data">

          <vs-td>
            <p class="hotel-name font-medium truncate">{{ tr.name }}</p>
          </vs-td>


          <vs-td>
            <p class="hotel-name font-medium truncate">{{ tr.start | date }}</p>
          </vs-td>

          <vs-td>
            <p class="hotel-name font-medium truncate">{{ tr.end | date }}</p>
          </vs-td>

          <vs-td>
            <p class="product-price">{{ tr.price }}€</p>
          </vs-td>

          <vs-td>
            <p class="product-price">{{ tr.price }}€</p>
          </vs-td>

          <vs-td class="whitespace-no-wrap">
            <feather-icon icon="LinkIcon" svgClasses="w-5 h-5 hover:text-primary stroke-current"
                          @click.stop="alert('Not implemented yet')"/>
            <!--                    <feather-icon icon="ThumbsUpIcon" svgClasses="w-5 h-5 hover:text-success stroke-current"-->
            <!--                                  class="ml-2"-->
            <!--                                  @click.stop="alert('Not implemented yet')"/>-->
          </vs-td>

        </vs-tr>
        </tbody>
      </template>
    </vs-table>

    <div class="flex flex-wrap items-center justify-end mt-5">
      <vs-button icon-pack="feather" icon="icon-edit" type="border" color="warning" class="mt-4"
                 :to="{name: 'app-event-edit', hash:'#accommodation', params: { eventId: this.data.id }}">
        Edit accommodation
      </vs-button>
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
  }
}
</script>
