<template>
    <div id="dashboard">
        <h1>That's the dashboard!</h1>
        <p>You should only get here if you're authenticated!</p>
        <p>Your email address: {{ email }}</p>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        email: ''
      }
    },
    created() {
      this.$http.get('/user/full-info/', {headers: {"Authorization": `Bearer ${JWTToken}`}})
        .then(res => {
          // console.log(res);
          const data = res.data.results;
          // console.log(data);
        })
        .catch(error => console.log(error))
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
