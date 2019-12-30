module.exports = {
  lintOnSave: false,
  devServer: {
    proxy: {
      '^/socket.io/': {
        //target: 'http://flask:5000/',
        target: 'http://192.168.1.160:5000/',
        ws: true
      }
    }
  }
}
