<template>
  <div id="app">
    <router-view/>
    <div style="position:fixed;text-align:center;bottom:0;margin: 0 auto;width:100%;">
    <a>Wangcr's Bookkeeping since 2022.</a>
    <a href="https://beian.miit.gov.cn/" target="_blank"
    >吉ICP备20001761号</a
    >
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
}
window.onload = function() {
  document.addEventListener('touchstart', function(event) {
    if (event.touches.length > 1) {
      event.preventDefault()
    }
  })
  document.addEventListener('gesturestart', function(event) {
    event.preventDefault()
  })
}
</script>

<style>
/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
