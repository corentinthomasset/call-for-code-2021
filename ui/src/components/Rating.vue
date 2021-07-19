<template>
  <ul class="rating">
    <li v-for="index in 5" :key="index">
      <img class="leaf" :src="leaf(index)" alt="leaf" />
    </li>
  </ul>
</template>

<script>
export default {
  name: "Rating",
  props: ["rating", "max"],
  computed: {
    leafCount() {
      return Math.floor((this.rating / this.max) * 5);
    },
  },
  methods: {
    leaf(index) {
      if (index <= this.leafCount) {
        return require("@/assets/leaf.svg");
      } else {
        return require("@/assets/leaf-grey.svg");
      }
    },
  },
};
</script>

<style scoped>
.rating {
  margin: 0 auto;
  list-style: none;
  display: flex;
  justify-content: space-between;
  width: 200px;
  background: var(--foreground);
  padding: 5px 30px;
  border-radius: 15px;
  box-shadow: var(--shadow);
  box-sizing: border-box;
}

.leaf {
  height: 20px;
}
</style>
