var express		= require('express'),
    router 		= express.Router(),
    objectId	= require('mongoose').Types.ObjectId,
	fileDB		= require('../db/FileInfo'),
	userDB		= require('../db/UserInfo'),
	scriptDB	= require('../db/Script'),
	// regionDB	= require('../db/Regions'),
	multer  	= require('multer'),
	async 		= require('async'),
	diskStorage = require('../configAndConstant/Config'),
	// constant 	= require('../configAndConstant/Constant'),
	childProcess= require("child_process"),
	upload 		= multer({dest: 'uploads/', storage: diskStorage.storage});

router.post('/aaa', function(req, res) {
	console.log(req.body)
	async.waterfall([
		function (cb) { // Check scriptid
			scriptDB.findById(
				req.body.idScript1,
				function (err, data) {
					if (err) {
						console.log("1")
						cb(err);
					} else {
						console.log("2")
						cb(null)
					}
				});
		},
	], function (err) {
		console.log(req.body)
		res.send({
			status: 400,
			message: err
		});
	}
	);

})

// router.post('/', upload.array("file"), function (req, res) {
// 	if (req.files[0] == undefined){
// 		console.log(req.files);
// 		console.log(req.body);
// 		res.send({
// 			status: 400,
// 			message: "upload failed"
// 		});
// 	}
// 	else{
// 		console.log(req.files)
// 		res.send({
// 			status: 200,
// 			message: "upload success"
// 		});
// 	}
// })

router.post("/", upload.fields(
	[
		{
			name: 'file1',
			maxCount: 1
		},
	]), function(req,res){
		console.log("begin	")
		console.log(req.files);
		console.log(req.body);
		let {sex, age, email, region, regionCode, nativeLand} = req.body
		// if (!objectId.isValid(req.body.idScript1) ||
		// 	req.files.file1 == undefined) {
		// 		console.log(req.body)
		// 		res.send({
		// 			status: 400,
		// 			message: "Sai thong tin"
		// 		});
		// } else {
			async.waterfall([
				function(cb) { // Check scriptid
					scriptDB.findInListId(
						req.body.idScript1,
						function(err) {
							if (err) {
								cb(err);
							} else {
								cb(null)
							}
						});
				},
				function(cb) { // Check email
					// var email = req.body.email;
					if (email) {
						userDB.findUserByEmail(email, function(err, user) {
							if (err) {
								cb(err.message);
							} else {
								checkUser(user, email, sex, age, region, regionCode, nativeLand, cb);
							}
						});
					} else {
						userDB.findUserByProp(sex, age, region, regionCode, nativeLand, function(err, user) {
							if (err) {
								cb(err.message);
							} else {
								checkUser(user, email, sex, age, region, regionCode, nativeLand, cb);
							}
						})
					}
				},
				function(id, cb) { // Get infor file
					console.log('Get infor file')
					var spawn = childProcess.spawn;
					var process = spawn('python3',
						["./python/SNRv2.py",
						req.files.file1[0].path], {detached: true});
					
					var timeout = setTimeout(() => {
						try {
							process.kill(-child.pid, 'SIGKILL');
						} catch (e) {
							console.log('Cannot kill process');
						}
					}, 15000);

					gotData = false
					process.on('error', err => console.log('Error:', err));
					process.on('exit', () => { clearTimeout(timeout); if (!gotData) {cb('Timeout', null);}});
					process.stdout.on('data', function(data) {
						console.log(data.toString())
						var wavInfo = JSON.parse(data.toString());
						gotData = true
						if (wavInfo.status) {
							cb(null, id, wavInfo.message)
						} else {
							cb('Python snr error')
						}
				    });
				},
				function(id, wavInfo, cb) {
					console.log(wavInfo)
					var files = [{
							userId		: id,
							scripId 	: req.body.idScript1,
							fileInfo 	: req.files.file1[0].filename,
							duration	: wavInfo.file1.dr,
							projectRate	: wavInfo.file1.rate,
							snr 		: wavInfo.file1.snr
						}];
					fileDB.saveFiles(files, function(err, docs) {
						if (err) {
							cb(err.message);
						} else {
							console.log({
								status: 200,
								message: files
							})
							res.send({
								status: 200,
								message: files
							})
						}
					})
				}], function(err) {
					res.send({
						status: 400,
						message: err
					});
				}
			);
		// }
	}
)

checkUser = function(user, email,sex, age, region, regionCode, nativeLand, callback) {
	if (user) { // had prop
		var id = user._id;
		if (email) {
			if (user.region != region || user.age != age || user.sex != sex || user.regionCode != regionCode || user.nativeLand != nativeLand) {
				user.region = region;
				user.age = age;
				user.sex = sex;
				user.regionCode = regionCode;
				user.nativeLand = nativeLand;
				userDB.updateOne({email: email}, {$set: {region: region, age: age, sex: sex, regionCode: regionCode, nativeLand: nativeLand}}, {}, function(err, user) {
					callback(null, id);
				});
			} else {
				callback(null, id);
			}
		} else {
			callback(null, id);
		}
	} else { // did not have prop
		var user = userDB({
			email	: email,
			region: region,
			age	: age,
			sex	: sex,
			regionCode: regionCode,
			nativeLand: nativeLand
		});
		userDB.saveUser(user, function(err, doc) {
			if (err) {
				callback(error.QUERY_DB_ERROR);
			} else {
				callback(null, doc._id)
			}
		})
	}
}

// router.get("/", function(req,res){
// 	res.render('upload');
// })

module.exports = router;