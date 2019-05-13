var express 	= require('express'),
	app 		= express(),
	https 		= require('https'),
	http 		= require('http'),
	config 		= require('./configAndConstant/Config'),
	bodyParser	= require('body-parser');

// Setup server
app.use(express.static('public', config.optionServer))
app.set('view engine','ejs');
app.set('views', './views')

// Start server
http.createServer(app).listen(3000, function () {
	console.log("Start server HTTP: http://localhost:3000");
});

// Setup DB
require('./db/ConnectDatabase');
// Setup body parser
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
// config logger https://github.com/log4js-node/log4js-node

// Route
app.use('/', require('./routes/Home'));
app.use('/script', require('./routes/ProcessScript'));
app.use('/upload', require('./routes/ProcessUpload'));
app.use('/textToSound', require('./routes/ProcessAudio'));

// app.use('/user', require('./routes/ProcessUser'));
