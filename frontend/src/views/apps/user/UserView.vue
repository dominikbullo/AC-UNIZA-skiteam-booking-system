<template>
  <div id="page-user-view">
    <vs-alert color="danger" title="User Not Found" :active.sync="user_not_found">
      <span>User record with id: {{ $route.params.userId }} not found. </span>
      <span>
        <span>Check </span><router-link :to="{name:'app-user-list'}"
                                        class="text-inherit underline">All Users</router-link>
      </span>
    </vs-alert>

    <div id="user-data" v-if="user_data">

      <vx-card title="Account" class="mb-base">

        <!-- Avatar -->
        <div class="vx-row">

          <!-- Avatar Col -->
          <!--          <div class="vx-col" id="avatar-col">-->
          <!--            <div class="img-container mb-4">-->
          <!--              <img :src="user_data.avatar" class="rounded w-full"/>-->
          <!--            </div>-->
          <!--          </div>-->

          <!-- Information - Col 1 -->
          <div class="vx-col flex-1" id="account-info-col-1">
            <table>
              <tr>
                <td class="font-semibold">Name</td>
                <td>{{ user_data.first_name }}</td>
              </tr>
              <tr>
                <td class="font-semibold">Email</td>
                <td>{{ user_data.email }}</td>
              </tr>
              <tr>
                <td class="font-semibold">Username</td>
                <td>{{ user_data.username }}</td>
              </tr>
            </table>
          </div>
          <!-- /Information - Col 1 -->

          <!-- Information - Col 2 -->
          <div class="vx-col flex-1" id="account-info-col-2">
            <table>
              <tr>
                <td class="font-semibold">Surname</td>
                <td>{{ user_data.last_name}}</td>
              </tr>
              <tr>
                <td class="font-semibold">Role</td>
                <td>{{ user_data.userRole | capitalize }}</td>
              </tr>
            </table>
          </div>
          <!-- /Information - Col 2 -->

          <!--          <div class="vx-col w-full flex" id="account-manage-buttons">-->
          <!--            <vs-button icon-pack="feather" icon="icon-edit" class="mr-4" :to="{name: 'page-user-settings'}">Edit-->
          <!--            </vs-button>-->
          <!--          </div>-->

        </div>

      </vx-card>

      <div class="vx-row">
        <div class="vx-col lg:w-1/2 w-full">
          <vx-card title="Information" class="mb-base">
            <table>
              <tr>
                <td class="font-semibold">Birth Date</td>
                <td>{{ user_data.dob }}</td>
              </tr>
              <tr>
                <td class="font-semibold">Mobile</td>
                <td>{{ user_data.mobile }}</td>
              </tr>
              <tr>
                <td class="font-semibold">Website</td>
                <td>{{ user_data.website }}</td>
              </tr>
            </table>
          </vx-card>
        </div>

      </div>

      <vx-card>
        <div class="vx-row">
          <div class="vx-col w-full">
            <div class="flex items-end px-3">
              <feather-icon svgClasses="w-6 h-6" icon="LockIcon" class="mr-2"/>
              <span class="font-medium text-lg leading-none">Permissions</span>
            </div>
            <vs-divider/>
          </div>
        </div>

        <div class="block overflow-x-auto">
          <table class="w-full permissions-table">
            <tr>
              <!--
                You can also use `Object.keys(Object.values(data_local.permissions)[0])` this logic if you consider,
                our data structure. You just have to loop over above variable to get table headers.
                Below we made it simple. So, everyone can understand.
               -->
              <th class="font-semibold text-base text-left px-3 py-2"
                  v-for="heading in ['Module', 'Read', 'Write', 'Create', 'Delete']" :key="heading">{{ heading }}
              </th>
            </tr>

            <tr v-for="(val, name) in user_data.permissions" :key="name">
              <td class="px-3 py-2">{{ name }}</td>
              <td v-for="(permission, name) in val" class="px-3 py-2" :key="name+permission">
                <vs-checkbox v-model="val[name]" class="pointer-events-none"/>
              </td>
            </tr>
          </table>
        </div>
        <!-- TODO only if user is from save family or you have access-->
        <div class="vx-col w-full flex" id="account-manage-buttons">
          <vs-button icon-pack="feather" icon="icon-bar-chart" class="mr-4" :to="{name: 'app-user-stats'}">More stats
          </vs-button>
        </div>
      </vx-card>
    </div>
  </div>
</template>

<script>
import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'

export default {
  data () {
    return {
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
  methods: {
    confirmDeleteRecord () {
      this.$vs.dialog({
        type: 'confirm',
        color: 'danger',
        title: 'Confirm Delete',
        text: `You are about to delete "${this.user_data.username}"`,
        accept: this.deleteRecord,
        acceptText: 'Delete'
      })
    },
    deleteRecord () {
      /* Below two lines are just for demo purpose */
      this.$router.push({ name: 'app-user-list' })
      this.showDeleteSuccess()

      /* UnComment below lines for enabling true flow if deleting user */
      // this.$store.dispatch("userManagement/removeRecord", this.user_data.id)
      //   .then(()   => { this.$router.push({name:'app-user-list'}); this.showDeleteSuccess() })
      //   .catch(err => { console.error(err)       })
    },
    showDeleteSuccess () {
      this.$vs.notify({
        color: 'success',
        title: 'User Deleted',
        text: 'The selected user was successfully deleted'
      })
    }
  },
  created () {
    // Register Module UserManagement Module
    if (!moduleUserManagement.isRegistered) {
      this.$store.registerModule('userManagement', moduleUserManagement)
      moduleUserManagement.isRegistered = true
    }

    const userId = this.$route.params.userId
    console.log('userId', userId)
    this.$store.dispatch('userManagement/fetchUser', userId)
      .then(res => {
        this.user_data = res.data
        console.log('res.data', res.data)
        console.log('this.user_data', this.user_data)
      })
      .catch(err => {
        if (err.response.status === 404) {
          this.user_not_found = true
          return
        }
        console.error(err)
      })
  }
}

</script>
