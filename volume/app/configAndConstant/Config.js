var multer  	= require('multer'),
	path	 	= require('path');

// Config upload folder
var storage = multer.diskStorage({
	destination: function( req, file,cb){
		cb(null,"./uploads")
	},
	filename: function(req, file, cb){
		cb(null, file.fieldname + Date.now() + '-' + Math.floor(Math.random()*1000) + path.extname(file.originalname))
	}
});

module.exports.storage = storage;

// Config server
var options = {
	dotfiles: 'ignore',
	etag: false,
	extensions: ['htm', 'html'],
	index: false,
	maxAge: '1d',
	redirect: false,
	setHeaders: function (res, path, stat) {
		res.set('x-timestamp', Date.now())
	}
}

module.exports.optionServer = options;