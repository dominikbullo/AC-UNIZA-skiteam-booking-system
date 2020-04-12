<!-- =========================================================================================
  File Name: UserView.vue
  Description: User View page
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div id="page-family-view">

    <vs-alert color="danger" title="User Not Found" :active.sync="family_not_found">
      <span>
        <span>Check </span><router-link :to="{name:'page-user-list'}"
                                        class="text-inherit underline">All Users</router-link>
      </span>
    </vs-alert>

    <div id="family-data" v-if="family_data">

      <vx-card title="Information" class="mb-base">
        <!-- Avatar -->
        <div class="vx-row">

          <!--          &lt;!&ndash; Avatar Col &ndash;&gt;-->
          <!--          <div class="vx-col" id="avatar-col">-->
          <!--            <div class="img-container mb-4">-->
          <!--              <img :src="family_data.avatar" class="rounded w-full"/>-->
          <!--            </div>-->
          <!--          </div>-->

          <!-- Information - Col 1 -->
          <div class="vx-col flex-1" id="account-info-col-1">
            <table>
              <tr>
                <td class="font-semibold">Family Name</td>
                <td>{{ family_data.name }}</td>
              </tr>
              <tr>
                <td class="font-semibold">Created</td>
                <td>{{ family_data.name }}</td>
              </tr>

            </table>
          </div>
          <!-- /Information - Col 1 -->

          <!-- Information - Col 2 -->
          <div class="vx-col flex-1" id="account-info-col-2">
            <table>
              <tr>
                <td class="font-semibold">Admin</td>
                <td>{{ family_data.name }}</td>
              </tr>
              <tr>
                <td class="font-semibold">Contact</td>
                <td>{{ family_data.name }}</td>
              </tr>

            </table>
          </div>

          <!-- /Information - Col 2 -->
          <div class="vx-col w-full flex" id="account-manage-buttons">
            <vs-button icon-pack="feather" icon="icon-edit" class="mr-4"
                       :to="{name: 'app-family-edit', params: { userId: $route.params.userId }}">Edit
            </vs-button>
          </div>

        </div>

      </vx-card>

      <div class="vx-row">
        <div class="vx-col w-full">
          <vx-card title="Members" class="mb-base">
            <table>
              <tr v-for="member in family_data.members"
                  :key="member.user.username">
                <td class="font-semibold">Name:</td>
                <td>{{ member.user.profile.full_name }}</td>
              </tr>
            </table>
          </vx-card>
        </div>

        <!--        <div class="vx-col lg:w-1/2 w-full">-->
        <!--          <vx-card title="Extra info" class="mb-base">-->
        <!--            <table>-->
        <!--              <tr v-for="data in family_data"-->
        <!--                  :key="data">-->
        <!--                <td class="font-semibold">test</td>-->
        <!--                <td>{{ data }}</td>-->
        <!--              </tr>-->
        <!--            </table>-->
        <!--          </vx-card>-->
        <!--        </div>-->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      family_data: null,
      family_not_found: false
    }
  },
  created () {
    const familyId = this.$route.params.familyId
    this.$store.dispatch('family/fetchFamily', familyId)
      .then(res => {
        this.family_data = res.data
      })
      .catch(err => {
        if (err.response.status === 404) {
          this.family_not_found = true
          return
        }
        console.error(err)
      })
  }
}
// import moduleUserManagement from '@/store/user-management/moduleUserManagement.js'
//
// export default {
//   props: {
//     familyId: {
//       type: Number,
//       required: true
//     }
//   },
//   data () {
//     return {
//       user_data: null,
//       user_not_found: false
//     }
//   },
//   computed: {
//     userAddress () {
//       let str = ''
//       for (const field in this.user_data.location) {
//         str += `${field} `
//       }
//       return str
//     }
//   },
//   methods: {
//     confirmDeleteRecord () {
//       this.$vs.dialog({
//         type: 'confirm',
//         color: 'danger',
//         title: 'Confirm Delete',
//         text: `You are about to delete "${this.user_data.username}"`,
//         accept: this.deleteRecord,
//         acceptText: 'Delete'
//       })
//     },
//     deleteRecord () {
//       /* Below two lines are just for demo purpose */
//       this.$router.push({ name: 'app-user-list' })
//       this.showDeleteSuccess()
//
//       /* UnComment below lines for enabling true flow if deleting user */
//       // this.$store.dispatch("userManagement/removeRecord", this.user_data.id)
//       //   .then(()   => { this.$router.push({name:'app-user-list'}); this.showDeleteSuccess() })
//       //   .catch(err => { console.error(err)       })
//     },
//     showDeleteSuccess () {
//       this.$vs.notify({
//         color: 'success',
//         title: 'User Deleted',
//         text: 'The selected user was successfully deleted'
//       })
//     }
//   },
//   created () {
//     // // Register Module UserManagement Module
//     // if (!moduleUserManagement.isRegistered) {
//     //   this.$store.registerModule('userManagement', moduleUserManagement)
//     //   moduleUserManagement.isRegistered = true
//     // }
//
//     const familyId = this.familyId
//     this.$store.dispatch('family/fetchFamily', familyId)
//       .then(res => {
//         this.family_data = res
//       })
//       .catch(err => {
//         if (err.response.status === 404) {
//           this.user_not_found = true
//           return
//         }
//         console.error(err)
//       })
//   }
// }

</script>

<style lang="scss">
  #avatar-col {
    width: 10rem;
  }

  #page-user-view {
    table {
      td {
        vertical-align: top;
        min-width: 140px;
        padding-bottom: .8rem;
        word-break: break-all;
      }

      &:not(.permissions-table) {
        td {
          @media screen and (max-width: 370px) {
            display: block;
          }
        }
      }
    }
  }

  // #account-info-col-1 {
  //   // flex-grow: 1;
  //   width: 30rem !important;
  //   @media screen and (min-width:1200px) {
  //     & {
  //       flex-grow: unset !important;
  //     }
  //   }
  // }


  @media screen and (min-width: 1201px) and (max-width: 1211px),
  only screen and (min-width: 636px) and (max-width: 991px) {
    #account-info-col-1 {
      width: calc(100% - 12rem) !important;
    }

    // #account-manage-buttons {
    //   width: 12rem !important;
    //   flex-direction: column;

    //   > button {
    //     margin-right: 0 !important;
    //     margin-bottom: 1rem;
    //   }
    // }

  }

</style>
