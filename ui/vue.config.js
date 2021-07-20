module.exports = {
  devServer: {
    proxy: "http://169.57.99.144:31544",
  },
  publicPath: process.env.NODE_ENV === 'production'
      ? '/call-for-code/'
      : '/'
};
