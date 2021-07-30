<template>
  <div
    id="stock"
    class="view"
    v-if="info && info.shortName"
    @click.capture="showContextual = false"
  >
    <ul class="stock-nav">
      <li>
        <router-link to="/"><unicon name="times" fill="#4951fd"/></router-link>
      </li>
      <li @click="showContextual = true">
        <unicon name="ellipsis-v" fill="#4951fd" />
      </li>
    </ul>
    <transition name="drawer">
      <div class="contextual-menu" v-if="showContextual">
        <ul class="action-list">
          <li v-if="showAdd" @click="addToPortfolio">
            Add {{ info.symbol }} to portfolio
            <unicon name="plus" fill="#4951fd" />
          </li>
          <li v-if="showReplace" @click="replaceInPortfolio">
            <span
              >Replace
              <span style="text-transform: uppercase">{{ ticker }}</span> by
              {{ info.symbol }}</span
            >
            <unicon name="sync" fill="#4951fd" />
          </li>
          <li v-if="showDelete" @click="deleteFromPortfolio">
            Delete {{ info.symbol }} from portfolio
            <unicon name="trash" fill="#4951fd" />
          </li>
        </ul>
      </div>
    </transition>
    <div class="section header">
      <h1>
        {{ info.shortName.slice(0, 15)
        }}<template v-if="info.shortName.length > 15">...</template>
      </h1>
      <h3>{{ info.industry }}</h3>
    </div>
    <EnvironmentalScore :score="ratings.environment_score"
      >environmental score</EnvironmentalScore
    >
    <div class="section stock-market-trend">
      <h2>Market trend</h2>
      <hooper
        :centerMode="true"
        :itemsToShow="1.2"
        style="height: 350px"
        @slide="slideHandler"
      >
        <slide v-for="stock in stocks" :key="stock.info.symbol">
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
    <ESGRatings :ratings="ratings" />
  </div>
  <Spinner v-else />
</template>

<script>
import { Hooper, Slide, Pagination } from "hooper";
import "hooper/dist/hooper.css";
import StockCard from "@/components/StockCard";
import ESGRatings from "@/components/ESGRatings";
import EnvironmentalScore from "@/components/EnvironmentalScore";
import Spinner from "@/components/Spinner";
export default {
  name: "Stock",
  props: ["ticker"],
  components: {
    Spinner,
    EnvironmentalScore,
    ESGRatings,
    StockCard,
    Hooper,
    Pagination,
    Slide,
  },
  data() {
    return {
      index: 0,
      stocks: [],
      showFullSummary: false,
      showContextual: false,
      mounted: false,
      get portfolio() {
        return JSON.parse(localStorage.getItem("stockList")) || {};
      },
      // eslint-disable-next-line
      set portfolio(value) {
        localStorage.setItem("stockList", value);
      },
    };
  },
  computed: {
    info() {
      return this.stocks[this.index]?.info;
    },
    ratings() {
      return this.stocks[this.index]?.ratings;
    },
    summary() {
      if (this.showFullSummary) {
        return this.info.longBusinessSummary;
      } else {
        return this.info.longBusinessSummary.slice(0, 200);
      }
    },
    showAdd() {
      return !this.portfolio[this.info.symbol.toLowerCase()];
    },
    showReplace() {
      return (
        !!this.portfolio[this.ticker.toLowerCase()] &&
        !this.portfolio[this.info.symbol.toLowerCase()]
      );
    },
    showDelete() {
      return !!this.portfolio[this.info.symbol.toLowerCase()];
    },
  },
  methods: {
    slideHandler(payload) {
      this.index = payload.currentSlide;
    },
    addToPortfolio() {
      let current = JSON.parse(localStorage.stockList) || {};
      current[this.info.symbol.toLowerCase()] = {
        shortName: this.info.shortName,
        total_grade: this.ratings.total_grade,
        environment_grade: this.ratings.environment_grade,
        social_grade: this.ratings.social_grade,
        governance_grade: this.ratings.governance_grade,
        total_score: this.ratings.total_score,
        environment_score: this.ratings.environment_score,
        social_score: this.ratings.social_score,
        governance_score: this.ratings.governance_score,
      };
      this.portfolio = JSON.stringify(current);
      this.$emit("info", `${this.info.symbol} has been added to portfolio`);
    },
    deleteFromPortfolio() {
      let current = JSON.parse(localStorage.stockList) || {};
      delete current[this.info.symbol.toLowerCase()];
      this.portfolio = JSON.stringify(current);
      this.$emit("info", `${this.info.symbol} has been deleted from portfolio`);
    },
    replaceInPortfolio() {
      let current = JSON.parse(localStorage.stockList) || {};
      current[this.info.symbol.toLowerCase()] = {
        shortName: this.info.shortName,
        total_grade: this.ratings.total_grade,
        environment_grade: this.ratings.environment_grade,
        social_grade: this.ratings.social_grade,
        governance_grade: this.ratings.governance_grade,
        total_score: this.ratings.total_score,
        environment_score: this.ratings.environment_score,
        social_score: this.ratings.social_score,
        governance_score: this.ratings.governance_score,
      };
      delete current[this.ticker];
      this.portfolio = JSON.stringify(current);
      this.$emit(
        "info",
        `${this.ticker.toUpperCase()} has been replaced by ${
          this.info.symbol
        } in portfolio`
      );
    },
    getStockInfo(ticker) {
      return new Promise((resolve, reject) => {
        this.$http
          .get(`http://52.117.182.214:31587/info/${ticker}`)
          .then((response) => {
            let stock = response.data[0];
            this.$http
              .get(`http://52.117.182.214:31587/ratings/${ticker}`)
              .then((response) => {
                stock.ratings = response.data[0];
                resolve(stock);
              })
              .catch((err) => {
                reject(err);
              });
          })
          .catch((err) => {
            reject(err);
          });
      });
    },
    getCorrelationInfo(index, correlations) {
      this.$http
        .get(`http://52.117.182.214:31587/ratings/${correlations[index]}`)
        .then((response) => {
          let ratings = response.data[0];
          if (ratings.environment_score > this.ratings.environment_score) {
            this.$http
              .get(`http://52.117.182.214:31587/info/${correlations[index]}`)
              .then((response) => {
                let stock = response.data[0];
                stock.ratings = ratings;
                this.stocks.push(stock);
              })
              .catch((err) => {
                console.log(err);
              });
          }
          if (
            this.stocks.length < 5 &&
            index + 1 < correlations.length &&
            this.mounted
          ) {
            setTimeout(() => {
              this.getCorrelationInfo(index + 1, correlations);
            }, 0);
          } else {
            this.$emit("loading", false);
            if (this.stocks.length < 2) {
              this.$emit(
                "info",
                `No suggestion for ${this.ticker.toUpperCase()}`
              );
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted() {
    this.$nextTick(() => {
      this.mounted = true;
      this.getStockInfo(this.ticker)
        .then((stock) => {
          this.$set(this.stocks, 0, stock);
          this.$emit("loading", true);
          this.$http
            .get(`http://52.117.182.214:31587/correlation/${this.ticker}`)
            .then((response) => {
              let correlations = Object.keys(response.data.correlation);
              let i = 0;
              this.getCorrelationInfo(i, correlations);
            })
            .catch((err) => {
              console.log(err);
            });
        })
        .catch(() => {
          this.$emit("error", `No data found for ${this.ticker}`);
          this.$router.push("/");
        });
    });
  },
  beforeDestroy() {
    this.$emit("loading", false);
    this.mounted = false;
  },
};
</script>

<style scoped>
.stock-nav {
  padding: 20px;
  margin: 0;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  box-sizing: border-box;
}

.header {
  margin-top: 75px;
  animation: slide-in-bottom 0.4s ease both;
}

.stock-market-trend {
  animation: slide-in-bottom 0.4s ease 0.2s both;
}

.stock-market-trend h3 {
  font-size: 0.8em;
}

.stock-info {
  animation: slide-in-bottom 0.4s ease 0.4s both;
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
</style>
