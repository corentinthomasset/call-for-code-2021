<template>
  <div class="section environmental-score">
    <div class="environmental-grade">
      <h1>
        <ICountUp :delai="1000" :endVal="score" />
      </h1>
      <h3>/1000</h3>
    </div>
    <Rating :rating="score" :max="1000" />
    <h3><slot></slot></h3>
  </div>
</template>

<script>
import ICountUp from "vue-countup-v2";
import Rating from "@/components/Rating";
export default {
  name: "EnvironmentalScore",
  props: ["score"],
  components: { Rating, ICountUp },
};
</script>

<style scoped>
.environmental-grade {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  margin: 5px;
}

.environmental-grade h1 {
  font-size: 4em;
  font-weight: 900;
  line-height: 50px;
}

.environmental-grade h3 {
  font-size: 1.1em;
}
</style>
