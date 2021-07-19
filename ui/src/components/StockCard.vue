<template>
  <div class="stock-card">
    <div class="stock-card-header">
      <div>
        <h1>aapl</h1>
        <h3>Apple Inc.</h3>
      </div>
      <div>
        <span class="stock-perf">+10%</span>
      </div>
    </div>
    <apexchart :height="250" :options="chartOptions" :series="series" />
  </div>
</template>

<script>
export default {
  name: "StockCard",
  props: ["stock"],
  data() {
    return {
      series: [
        {
          data: [31, 40, 28, 51, 42, 109, 100],
        },
      ],
      chartOptions: {
        chart: {
          type: "area",
          sparkline: {
            enabled: true,
          },
        },
        colors: ["#2CC705", "#4951fd"],
        fill: {
          type: "gradient",
          gradient: {
            type: "vertical",
            inverseColors: false,
            opacityFrom: 0.6,
            opacityTo: 0.3,
          },
        },
        stroke: {
          curve: "smooth",
        },
        tooltip: {
          enabled: false,
        },
      },
    };
  },
};
</script>

<style scoped>
.stock-card {
  background: #fff;
  border-radius: 20px;
  box-shadow: var(--shadow);
  margin: 15px;
  box-sizing: border-box;
  height: 300px;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
}

.stock-card-header {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 20px;
  z-index: 10;
  text-align: left;
}

.stock-card h1 {
  font-weight: 400;
  text-transform: uppercase;
}

.stock-card h3 {
  margin-top: -10px;
}

.stock-perf {
  background: #edf3fa;
  padding: 4px 5px;
  border-radius: 10px;
  font-weight: 600;
}
</style>
