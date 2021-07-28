<template>
  <li class="portfolio-card">
    <span>
      <h2>{{ ticker }}</h2>
      <h3>
        {{ shortName.slice(0, 15)
        }}<template v-if="shortName.length > 15">...</template>
      </h3>
    </span>
    <Rating :rating="rating" :max="500" />
  </li>
</template>

<script>
import Rating from "@/components/Rating";
export default {
  name: "PortfolioCard",
  components: { Rating },
  props: ["ticker", "shortName", "rating"],
};
</script>

<style scoped>
.portfolio-card {
  background: var(--foreground);
  border-radius: 20px;
  box-shadow: var(--shadow);
  padding: 10px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 20px;
  animation: slide-in-bottom 0.2s ease both;
  text-align: left;
}

.portfolio-card .ratings {
  background: none;
  box-shadow: none;
}

h2 {
  text-transform: uppercase;
}
</style>
