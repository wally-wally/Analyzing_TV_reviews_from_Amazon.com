module.exports = {
  configureWebpack: {
    devServer: {
      proxy: {
          '/api': {
            target: 'http://localhost:5000',
          }
        }
    }
  }
}