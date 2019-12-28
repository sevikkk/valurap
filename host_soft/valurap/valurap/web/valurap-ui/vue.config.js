module.exports = {
  lintOnSave: false,
  devServer: {
    proxy: {
      '^/socket.io/': {
        target: 'http://flask:5000/',
        ws: true
      }
    }
  }
}
