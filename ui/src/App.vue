<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
:root {
  --foreground: #ffffff;
  --background: #edf3fa;
  --text: #2c3e50;
  --shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  --purlpe: #4951fd;
  --green: #2cc705;
}

body {
  background: var(--background);
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text);
  text-align: center;
  width: 100vw;
  overflow: hidden;
  max-width: 500px;
  margin: auto;
}

h1,
h2,
h3,
h4,
h5 {
  margin: 0;
}

h2 {
  font-size: 1em;
}

h3 {
  font-size: 1em;
  opacity: 0.5;
  font-weight: 300;
}

p {
  text-align: justify;
  padding: 0 20px;
  opacity: 0.5;
  margin: 0;
  box-sizing: border-box;
  width: 100%;
}

.section {
  margin: 35px 0;
}

.button {
  color: var(--text);
  text-decoration: none;
  padding: 10px 20px;
  border: 1px solid var(--text);
  border-radius: 20px;
  display: inline-block;
  margin: 20px;
}

.hooper-indicator {
  height: 12px !important;
  border-radius: 50% !important;
  background-color: rgba(139, 151, 163, 0.2) !important;
}

.hooper-indicator.is-active {
  background-color: #4951fd !important;
}

.flex-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.header {
  margin-top: 30px;
}

.header h1 {
  font-weight: 400;
}

/* Change the white to any color */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active
{
  -webkit-box-shadow: 0 0 0 30px white inset !important;
}

@keyframes slide-in-bottom {
  0% {
    transform: translateY(50px);
    opacity: 0;
  }
  100% {
    transform: translateY(0px);
    opacity: 1;
  }
}

@keyframes slide-in-top {
  0% {
    transform: translateY(-200px);
    opacity: 0;
  }
  100% {
    transform: translateY(0px);
    opacity: 1;
  }
}
</style>
