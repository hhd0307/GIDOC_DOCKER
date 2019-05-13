var express = require('express'),
	router = express.Router(),
	multer = require('multer'),
	diskStorage = require('../configAndConstant/Config.js'),
	upload = multer({ dest: 'uploads/', storage: diskStorage.storage }),
	exceljs = require('exceljs'),
	scriptDB = require('../db/Script'),
	async = require("async");

/*
router.post("/", upload.single('file', 3), function(req,res){	
	if (req.file == undefined || req.file.originalname != 'script.xlsx') {
		res.send("<h1>Upload file khong thanh cong</h1>")
	} else {
	    var workbook = new exceljs.Workbook();
		var response = true;
		async.waterfall([
				function(callback) {
	    			var listScript = [];
				    workbook.xlsx.readFile(process.cwd() +"\\"+ req.file.path).then(function() {
						var worksheet = workbook.getWorksheet(1)
						var col = worksheet.getColumn(1);
						col.eachCell(function(cell, colNumber) {
							listScript.push(cell.value);
						    if (worksheet.rowCount == colNumber) {
								callback(null, listScript);
						    }
						});
					});
				},
				function(listScript, cb) {
					async.each(listScript, function(script, callback) {
						var newScript = new scriptDB({
							script: script
						});

						scriptDB.saveScript(newScript, function(err, docs) {
							if(err) {
								callback(err);
							} else {
								callback(null);
							}
						});
					}, function(err) {
						if( err ) {
							console.log('A script failed to process');
							cb(err);
						} else {
							console.log('All script have been processed successfully');
							cb(null);
						}
					});
				},
				function(callback) {
					if (response) {
						res.redirect('/');
						response = false;
					}
				}
			], function (err, result) {
				if (response) {
					res.send(err);
					response = false;
				}
			});
		setTimeout(() => {
			if (response) {
				res.send('<h1>File need to be formatted</h1>');
				response = false;
			}
		}, 10000);
	}
})
*/

router.get("/", (req, res) => {
	async.waterfall([
		function (cb) {
			scriptDB.getLength((err, count) => {
				if (err) {
					cb(err);
				} else {
					cb(null, count);
				}
			});
		},
		function (count, cb) {
			var skip = Math.floor(Math.random() * (count - 1));
			scriptDB.getRandom(skip, 1, function (err, docs) {
				if (err) {
					cb(err);
				} else {
					res.send({
						status: 200,
						message: docs
					});
				}
			})
		}
	], function (err) {
		res.send({ status: 400, message: err });
	})
})

router.get("/page", (req, res) => {
	res.render('uploadScript')
})

module.exports = router;