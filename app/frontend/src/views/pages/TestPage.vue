<template>
  <div id="test_page">
    <vx-card>
      <h1>That's the dashboard!</h1>
      <p>You should only get here if you're authenticated!</p>
      <p>Your email address: {{ email }}</p>

        <!--  Roles  -->
      <p>Your current role is <strong>{{ $acl.get[0] }}</strong>.</p>

      <div class="demo-alignment mb-base">
        <vs-radio v-model="userRole" vs-value="editor">Editor</vs-radio>
        <vs-radio v-model="userRole" vs-value="admin">Admin</vs-radio>
      </div>

      <vx-card title="Buttons" no-shadow card-border code-toggler>
        <div class="demo-alignment">
          <vs-button v-show="$acl.check('editor')" icon-pack="feather" icon="icon-plus" @click="addChild">{{ $t('AddChild') }}</vs-button>
          <vs-button v-show="$acl.check('admin')" icon-pack="feather" icon="icon-plus" @click="addEvent">{{ $t('AddEvent') }}</vs-button>
       </div>
      </vx-card>



    </vx-card>
  </div>
</template>

<script>
export default {

  data () {
    return {
      email: '',
      userRole: this.$acl.get[0]
    }
  },
  watch: {
    userRole (val) {
      this.$store.dispatch('updateUserRole', {
        aclChangeRole: this.$acl.change,
        userRole: val
      })
    }
  },
  created () {
    this.$http.get('/rest-auth/user/').then(res => {
      console.log(res.data)
      this.email = res.data.email
    }).catch(error => console.log(error))
  },
  methods: {
    addChild () {
      this.$vs.notify({
        title: 'Child',
        text: 'Yeah you want to add child - not implemented yet'
      })
    },
    addEvent () {
      this.$vs.notify({
        title: 'Child',
        text: 'Yeah you want to add child - not implemented yet'
      })
    }
  }
}
</script>

<style scoped>
  h1, p {
    text-align: center;
  }

  p {
    color: red;
  }
</style>
