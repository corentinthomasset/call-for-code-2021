<template>
  <div id="stock" class="view" v-if="info.shortName">
    <div class="section stock-header">
      <h1>{{ info.shortName }}</h1>
      <h3>{{ info.industry }}</h3>
    </div>
    <div class="section stock-environmental-rating">
      <div class="environmental-score">
        <h1>
          <ICountUp :delai="1000" :endVal="ratings.environment_score" />
        </h1>
        <h3>/500</h3>
      </div>
      <Rating :rating="ratings.environment_score" :max="500" />
      <h3>environmental grade</h3>
    </div>
    <div class="section stock-market-trend">
      <h2>Market trend</h2>
      <h3>
        Swipe left to show greener stocks<br />
        with similar market trends
      </h3>
      <hooper :centerMode="true" :itemsToShow="1.2" style="height: 350px">
        <slide>
          <StockCard />
        </slide>
        <slide>
          <StockCard />
        </slide>
        <pagination slot="hooper-addons"></pagination>
      </hooper>
    </div>
    <div class="section stock-info">
      <h2>About</h2>
      <ul>
        <li><b>Name</b> {{ info.longName }}</li>
        <li><b>Ticker</b> {{ info.symbol }}</li>
        <li><b>Sector</b> {{ info.sector }}</li>
        <li><b>Industry</b> {{ info.industry }}</li>
        <li><b>Country</b> {{ info.country }}</li>
      </ul>
      <p>
        <b>Summary</b><br />
        {{ summary }}<template v-if="!showFullSummary">...</template>
      </p>
      <a
        href="#"
        @click.prevent="showFullSummary = true"
        v-if="!showFullSummary"
        class="button"
        >Show more</a
      >
    </div>
    <div class="section stock-esg-rating">
      <h2>ESG Ratings</h2>
      <h3>Environmental, Social & Governance practices</h3>
      <div class="ratings-wrapper flex-wrapper">
        <div class="esg-ratings">
          <h1>{{ ratings.total_grade }}</h1>
          <h3>ESG Rating</h3>
        </div>
        <ul class="esg-details">
          <li>Environmental <b>{{ ratings.environment_grade }}</b></li>
          <li>Social <b>{{ ratings.social_grade }}</b></li>
          <li>Governance <b>{{ ratings.governance_grade }}</b></li>
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
  </div>
</template>

<script>
import { Hooper, Slide, Pagination } from "hooper";
import "hooper/dist/hooper.css";
import ICountUp from "vue-countup-v2";
import Rating from "@/components/Rating";
import StockCard from "@/components/StockCard";
export default {
  name: "Stock",
  props: ["ticker"],
  components: {
    Rating,
    StockCard,
    Hooper,
    Pagination,
    Slide,
    ICountUp,
  },
  data() {
    return {
      info: {},
      ratings: {},
      trend: {},
      showFullSummary: false,
      series: [
        {
          name: "Microsoft Corp.",
          data: [250, 100, 235, 100, 195, 100],
        },
        {
          name: "Apple Inc",
          data: [210, 100, 205, 100, 205, 100],
        },
      ],
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
    summary() {
      if (this.showFullSummary) {
        return this.info.longBusinessSummary;
      } else {
        return this.info.longBusinessSummary.slice(0, 200);
      }
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.$http.get(`/catchall/${this.ticker}`).then(response=>{
        this.info = response.data.info
        this.ratings = response.data.ratings[0]
      }).catch(err=>{
        console.log(err);
      })
    });
  },
};
</script>

<style scoped>
.stock-header {
  margin-top: 30px;
}

.stock-header h1 {
  font-weight: 400;
}

.stock-header h3 {
  margin-top: -5px;
}

.environmental-score {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  margin: 5px;
}

.environmental-score h1 {
  font-size: 4em;
  font-weight: 900;
  line-height: 50px;
}

.environmental-score h3 {
  font-size: 1.1em;
}

.stock-market-trend h3 {
  font-size: 0.8em;
}

.stock-info ul {
  padding: 0 20px;
  list-style: none;
  opacity: 0.5;
  text-align: left;
}

.stock-info p {
  text-align: justify;
  padding: 0 20px;
  opacity: 0.5;
  margin: 0;
}

.ratings-wrapper {
  padding: 20px;
}

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
