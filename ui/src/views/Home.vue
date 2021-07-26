<template>
  <div id="home">
    <div>
      <img src="@/assets/logo.png" alt="logo" class="logo" />
      <form @submit.prevent="search">
        <span class="search-input">
          <input id="search" type="text" v-model="ticker"/>
          <label for="search">
            <unicon name="search" fill="#2c3e50" />
          </label>
        </span>
      </form>
      <p><b>Invest in a brigther future, back companies that do the most to preserve our planet.</b> Search for stocks by symbol. Get suggestions with better environmental ratings and similar market trends.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      ticker: "",
    };
  },
  methods: {
    search() {
      this.$router.push(`/${this.ticker}`)
    },
  },
};
</script>

<style scoped>
#home {
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.logo {
  width: 80%;
  display: block;
  margin: auto;
}

form{
  margin: 50px 0;
}

.search-input{
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5em;
  text-align: center;
}

input[type=text]{
  border: none;
  outline: none;
  padding: 15px 20px;
  border-radius: 20px 0 0 20px;
  box-shadow: var(--shadow);
  background: var(--foreground);
  height: 50px;
  box-sizing: border-box;
}

label{
  padding: 15px 20px;
  border-radius: 0 20px 20px 0;
  box-shadow: var(--shadow);
  background: var(--foreground);
  height: 50px;
  box-sizing: border-box;
}
</style>
