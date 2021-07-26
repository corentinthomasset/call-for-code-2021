<template>
  <div id="stock" class="view" v-if="info && info.shortName">
    <div class="section stock-header">
      <h1>
        {{ info.shortName.slice(0, 20)
        }}<template v-if="info.shortName.length > 20">...</template>
      </h1>
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
      <hooper
        :centerMode="true"
        :itemsToShow="1.2"
        style="height: 350px"
        @slide="slideHandler"
      >
        <slide v-for="stock in stocks" :key="stock.details[0].info.symbol">
          <StockCard :stock="stock" />
        </slide>
        <pagination slot="hooper-addons"></pagination>
      </hooper>
    </div>
    <div class="section stock-info">
      <ul>
        <li><b>Name</b> {{ info.longName }}</li>
        <li><b>Ticker</b> {{ info.symbol }}</li>
        <li><b>Sector</b> {{ info.sector }}</li>
        <li><b>Industry</b> {{ info.industry }}</li>
        <li><b>Country</b> {{ info.country }}</li>
      </ul>
    </div>
    <div class="section stock-summary">
      <h2>Summary</h2>
      <p>{{ summary }}<template v-if="!showFullSummary">...</template></p>
      <a
        href="#"
        @click.prevent="showFullSummary = true"
        v-if="!showFullSummary"
        class="button"
        >Read more</a
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
  </div>
  <Spinner v-else/>
</template>

<script>
import { Hooper, Slide, Pagination } from "hooper";
import "hooper/dist/hooper.css";
import ICountUp from "vue-countup-v2";
import Rating from "@/components/Rating";
import StockCard from "@/components/StockCard";
import Spinner from "@/components/Spinner";
export default {
  name: "Stock",
  props: ["ticker"],
  components: {
    Spinner,
    Rating,
    StockCard,
    Hooper,
    Pagination,
    Slide,
    ICountUp,
  },
  data() {
    return {
      index: 0,
      stocks: [],
      showFullSummary: false,
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
    info() {
      return this.stocks[this.index]?.details[0].info;
    },
    ratings() {
      return this.stocks[this.index]?.ratings[0];
    },
    summary() {
      if (this.showFullSummary) {
        return this.info.longBusinessSummary;
      } else {
        return this.info.longBusinessSummary.slice(0, 200);
      }
    },
    series() {
      let data = [];
      data[0] = this.ratings.environment_score;
      data[1] = Math.floor(
        Math.sqrt(
          Math.pow(this.ratings.environment_score / 2, 2) +
            Math.pow(this.ratings.governance_score / 2, 2)
        )
      );
      data[2] = this.ratings.governance_score;
      data[3] = Math.floor(
        Math.sqrt(
          Math.pow(this.ratings.social_score / 2, 2) +
            Math.pow(this.ratings.governance_score / 2, 2)
        )
      );
      data[4] = this.ratings.social_score;
      data[5] = Math.floor(
        Math.sqrt(
          Math.pow(this.ratings.environment_score / 2, 2) +
            Math.pow(this.ratings.social_score / 2, 2)
        )
      );
      return [
        {
          data: data,
        },
      ];
    },
  },
  methods: {
    slideHandler(payload) {
      this.index = payload.currentSlide;
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.$http
        .get(`http://169.57.99.144:31544/catchall/${this.ticker}`)
        .then((response) => {
          this.stocks.push(response.data);
          this.stocks[0].correlations.forEach((correlated) => {
            if (correlated.ratings[0].total >= this.ratings.total) {
              if (this.stocks.length < 5) {
                this.stocks.push(correlated);
              }
            }
          });
        })
        .catch((err) => {
          console.log(err);
        });
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
