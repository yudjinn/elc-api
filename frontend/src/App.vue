<template>
  <div id="app">
    <h1> API </h1>
    {{msg}}
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'app',
  data() {
    return {
      msg: ''
    }
  },
  async created() {
    try {
      const res = await axios.get('http://localhost:5000')

      this.msg = res.data;
    } catch(e) {
      console.error(e)
    }
  }
}
axios.defaults.baseUrl = process.env.VUE_APP_BASE_URL
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
