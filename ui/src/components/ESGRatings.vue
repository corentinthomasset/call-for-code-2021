<template>
  <div class="section stock-esg-rating">
    <h2>ESG Ratings</h2>
    <h3>Environmental, Social & Governance practices</h3>
    <div class="ratings-wrapper flex-wrapper">
      <div class="esg-ratings">
        <h1>{{ ratings.total_grade }}</h1>
        <h3>ESG Rating</h3>
      </div>
      <ul class="esg-details">
        <li>
          Environmental <b>{{ ratings.environment_grade }}</b>
        </li>
        <li>
          Social <b>{{ ratings.social_grade }}</b>
        </li>
        <li>
          Governance <b>{{ ratings.governance_grade }}</b>
        </li>
      </ul>
    </div>
    <apexchart
      type="radar"
      height="300"
      :options="chartOptions"
      :series="series"
      class="radar"
    ></apexchart>
  </div>
</template>

<script>
export default {
  name: "ESGRatings",
  props: ["ratings"],
  data() {
    return {
      chartOptions: {
        chart: {
          type: "radar",
          toolbar: {
            show: false,
          },
        },
        colors: ["#2CC705", "#4951fd"],
        stroke: {
          width: 3,
        },
        fill: {
          opacity: 0.1,
        },
        markers: {
          size: 0,
        },
        xaxis: {
          categories: ["Environmental", "", "Governance", "", "Social", ""],
        },
      },
    };
  },
  computed: {
    series() {
      let data = [];
      data[0] = this.ratings.environment_score;
      data[1] = Math.floor(
        Math.sqrt(
          Math.pow(this.ratings.environment_score / 2, 2) +
            Math.pow(this.ratings.governance_score / 2, 2)
        ) * 0.68
      );
      data[2] = this.ratings.governance_score;
      data[3] = Math.floor(
        Math.sqrt(
          Math.pow(this.ratings.social_score / 2, 2) +
            Math.pow(this.ratings.governance_score / 2, 2)
        ) * 0.68
      );
      data[4] = this.ratings.social_score;
      data[5] = Math.floor(
        Math.sqrt(
          Math.pow(this.ratings.environment_score / 2, 2) +
            Math.pow(this.ratings.social_score / 2, 2)
        ) * 0.68
      );
      return [
        {
          data: data,
        },
      ];
    },
  },
};
</script>

<style scoped>
.esg-ratings {
  background: var(--foreground);
  box-shadow: var(--shadow);
  border-radius: 15px;
  padding: 10px;
}

.esg-details {
  list-style: none;
  text-align: left;
  opacity: 0.5;
  padding: 20px;
}

.radar {
  margin: -50px;
}
</style>
