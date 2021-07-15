<template>
  <div id="stock">
    <h1>{{ ticker }}</h1>
    <h3>{{ info.longName }}</h3>
  </div>
</template>

<script>
export default {
  name: "Stock",
  props: ["ticker"],
  data() {
    return {
      info: {},
      history: {},
    };
  },
  mounted() {
    this.$nextTick(() => {
      let data = require("../data/aapl.json");
      this.info = data.info;
      this.history = data.history;
    });
  },
};
</script>

<style scoped></style>
