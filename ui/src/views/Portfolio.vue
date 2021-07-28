<template>
  <div id="portfolio">
    <div class="portfolio-header section">
      <EnvironmentalScore :score="avg"> portfolio average </EnvironmentalScore>
    </div>
    <div class="portfolio-stock-list">
      <form @submit.prevent="search" class="section">
        <span class="search-input">
          <input
            id="search"
            type="text"
            v-model="ticker"
            placeholder="Search stocks"
          />
          <label for="search">
            <unicon name="search" fill="#2c3e50" />
          </label>
        </span>
      </form>
      <ul class="stock-list card-container">
        <PortfolioCard
          :ticker="symbol"
          :short-name="stock.shortName"
          :rating="stock.environment_score"
          v-for="(stock, symbol, i) in stocks"
          :key="symbol"
          :style="animationStyle(i)"
          @click.native="stockClickHandler(symbol)"
        />
      </ul>
    </div>
    <ESGRatings class="portfolio-esg-ratings" :ratings="ratings" />
  </div>
</template>

<script>
import PortfolioCard from "@/components/PortfolioCard";
import EnvironmentalScore from "@/components/EnvironmentalScore";
import ESGRatings from "@/components/ESGRatings";

export default {
  name: "Portfolio",
  components: { ESGRatings, EnvironmentalScore, PortfolioCard },
  data() {
    return {
      ticker: "",
    };
  },
  computed: {
    stocks() {
      if (localStorage.stockList) {
        let stocks = JSON.parse(localStorage.stockList);
        if (Object.keys(stocks).length > 0) {
          return stocks;
        }
      }
      let defaultPortfolio = {
        aapl: {
          shortName: "Apple Inc.",
          total_grade: "B",
          environment_grade: "B",
          social_grade: "B",
          governance_grade: "B",
          total_score: 620,
          environment_score: 210,
          social_score: 205,
          governance_score: 205,
        },
        msft: {
          shortName: "Microsoft Corporation",
          total_grade: "B",
          environment_grade: "BBB",
          social_grade: "B",
          governance_grade: "B",
          total_score: 715,
          environment_score: 315,
          social_score: 200,
          governance_score: 200,
        },
        v: {
          shortName: "Visa Inc.",
          total_grade: "BBB",
          environment_grade: "A",
          social_grade: "BBB",
          governance_grade: "BBB",
          total_score: 1050,
          environment_score: 446,
          social_score: 300,
          governance_score: 304,
        },
      };
      localStorage.stockList = JSON.stringify(defaultPortfolio);
      return defaultPortfolio;
    },
    ratings() {
      let ratings = {
        total_grade: "B",
        environment_grade: "B",
        social_grade: "B",
        governance_grade: "B",
        total_score: 0,
        environment_score: 0,
        social_score: 0,
        governance_score: 0,
      };
      Object.keys(this.stocks).forEach((stock) => {
        ratings.total_score += this.stocks[stock].total_score;
        ratings.environment_score += this.stocks[stock].environment_score;
        ratings.social_score += this.stocks[stock].social_score;
        ratings.governance_score += this.stocks[stock].governance_score;
      });
      ratings.total_score = Math.floor(
        ratings.total_score / Object.keys(this.stocks).length
      );
      ratings.environment_score = Math.floor(
        ratings.environment_score / Object.keys(this.stocks).length
      );
      ratings.social_score = Math.floor(
        ratings.social_score / Object.keys(this.stocks).length
      );
      ratings.governance_score = Math.floor(
        ratings.governance_score / Object.keys(this.stocks).length
      );
      return ratings;
    },
    avg() {
      let avg = 0;
      Object.keys(this.stocks).forEach((stock) => {
        avg += this.stocks[stock].environment_score;
      });
      return Math.floor(avg / Object.keys(this.stocks).length);
    },
  },
  methods: {
    animationStyle(index) {
      return `animation-delay: ${index * 50}ms`;
    },
    search() {
      this.$router.push(`/${this.ticker}`);
    },
    stockClickHandler(ticker) {
      this.$router.push(`/${ticker}`);
    },
  },
};
</script>

<style scoped>
.portfolio-header {
  margin-top: 75px;
}

.portfolio-stock-list {
  margin: 75px 0;
}

form {
  margin: 20px 0;
}

.search-input {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5em;
  text-align: center;
}

input[type="text"] {
  border: none;
  outline: none;
  padding: 15px 20px;
  border-radius: 20px 0 0 20px;
  box-shadow: var(--shadow);
  background: var(--foreground);
  height: 50px;
  box-sizing: border-box;
}

label {
  padding: 15px 20px;
  border-radius: 0 20px 20px 0;
  box-shadow: var(--shadow);
  background: var(--foreground);
  height: 50px;
  box-sizing: border-box;
}

.card-container {
  padding: 0;
  margin: 0;
  list-style: none;
}

.portfolio-esg-ratings {
  margin-top: 50px;
}
</style>
