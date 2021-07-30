<template>
  <div id="app">
    <transition :name="$route.meta.transition" mode="out-in">
      <router-view
        @error="toggleError"
        @info="toggleInfo"
        @loading="toggleLoading"
      />
    </transition>
    <transition name="toast">
      <div class="error toast" v-if="showError">
        <ul>
          <li @click="showError = false">
            {{ errorMsg }}
            <unicon name="exclamation-triangle" fill="#fff" />
          </li>
        </ul>
      </div>
      <div class="info toast" v-if="showInfo">
        <ul>
          <li @click="showInfo = false">
            {{ infoMsg }}
            <unicon name="info-circle" fill="#fff" />
          </li>
        </ul>
      </div>
      <div class="loading toast" v-if="showLoading">
        <ul>
          <li>
            Loading suggestions
            <div class="spinner"></div>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showError: false,
      errorMsg: "Error",
      showInfo: false,
      infoMsg: "Info",
      showLoading: false,
    };
  },
  methods: {
    toggleError(msg) {
      this.errorMsg = msg;
      this.showError = true;
      setTimeout(() => {
        this.showError = false;
      }, 5000);
    },
    toggleInfo(msg) {
      this.infoMsg = msg;
      this.showInfo = true;
      setTimeout(() => {
        this.showInfo = false;
      }, 5000);
    },
    toggleLoading(bool) {
      this.showLoading = bool;
    },
  },
};
</script>

<style>
:root {
  --foreground: #ffffff;
  --background: #edf3fa;
  --text: #2c3e50;
  --shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  --purlpe: #4951fd;
  --green: #2cc705;
  --error: #ff0033;
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

.contextual-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
  background: var(--foreground);
  border-radius: 0 0 20px 20px;
  color: var(--purlpe);
  box-shadow: var(--shadow);
}

.contextual-menu .close-contextual-menu {
  position: absolute;
  top: 20px;
  right: 20px;
}

.contextual-menu .action-list {
  list-style: none;
  padding: 0 10px;
}

.contextual-menu .action-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  margin: 10px;
}

.drawer-enter-active {
  animation: drawer 0.5s ease;
}
.drawer-leave-to {
  animation: drawer 0.5s ease reverse;
}

.toast {
  position: fixed;
  bottom: 10px;
  left: 10px;
  right: 10px;
  z-index: 999;
  border-radius: 20px;
  color: var(--foreground);
  box-shadow: var(--shadow);
}

.toast-enter-active {
  animation: toast 0.5s ease;
}
.toast-leave-to {
  animation: toast 0.5s ease reverse;
}

.toast.info {
  background: var(--purlpe);
}

.toast.error {
  background: var(--error);
}

.toast.loading {
  background: var(--foreground);
  color: var(--purlpe);
}

.toast ul {
  list-style: none;
  padding: 0 10px;
}

.toast ul li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
  margin: 10px;
}

.toast.loading .spinner,
.toast.loading .spinner:after {
  border-radius: 50%;
  width: 20px;
  height: 20px;
}
.toast.loading .spinner {
  margin: 0;
  position: relative;
  border-top: 5px solid rgba(73, 81, 253, 0.2);
  border-right: 5px solid rgba(73, 81, 253, 0.2);
  border-bottom: 5px solid rgba(73, 81, 253, 0.2);
  border-left: 5px solid var(--purlpe);
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-animation: load8 0.8s infinite linear;
  animation: load8 0.8s infinite linear;
}
@-webkit-keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

.portfolio-enter-active {
  animation: route-right 0.4s ease;
}
.portfolio-leave-active {
  animation: route-left 0.4s ease reverse;
}

.portfolio-leave-active .stock-nav {
  opacity: 0;
}

.stock-enter-active {
  animation: none;
}
.stock-leave-active {
  animation: route-right 0.4s ease reverse;
}

/* Change the white to any color */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
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

@keyframes toast {
  0% {
    transform: translateY(200px);
    opacity: 0;
  }
  100% {
    transform: translateY(0px);
    opacity: 1;
  }
}

@keyframes drawer {
  0% {
    transform: translateY(-200px);
    opacity: 0;
  }
  100% {
    transform: translateY(0px);
    opacity: 1;
  }
}

@keyframes route-left {
  0% {
    transform: translateX(200px);
    opacity: 0;
  }
  100% {
    transform: translateX(0px);
    opacity: 1;
  }
}

@keyframes route-right {
  0% {
    transform: translateX(-200px);
    opacity: 0;
  }
  100% {
    transform: translateX(0px);
    opacity: 1;
  }
}
</style>
