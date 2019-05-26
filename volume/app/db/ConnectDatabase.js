var mongoose = require('mongoose')

// mongoose.connect('mongodb://admin:123456@mongodb:27017/gidoc', { useNewUrlParser: true })
mongoose.connect('mongodb://localhost/duc', { useNewUrlParser: true })

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'Connection error:'));
db.once('open', function () {
  console.log("Connect database success")
});

require('./UserInfo');


// User = mongoose.model('user');
// user = User();
// user.email = 'b@b.com';
// user.save(function(err, rs) {
//   console.log(err, rs)
// });