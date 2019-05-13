var mongoose= require('mongoose'),
	error	= require('../configAndConstant/Error').ERROR,
	errorUser= require('../configAndConstant/Error').USER_ERROR;

var userSch= mongoose.Schema({
	email: {
		type: String,
        required: true,
		default: ''
	},
	region: {
		type: String,
		required: true,
	},
	age: {
		type: String,
		required: true,
	},
	sex: {
		type: String,
		required: true
	},
	regionCode: {
		type: String,
		required: true
	},
	nativeLand: {
		type: String,
		required: true
	},
});

user = module.exports= mongoose.model('user', userSch);

module.exports.saveUser = function(scr, cb){
	scr.save(cb);
};

module.exports.findUser= function(userID, callback) {
	if (!mongoose.Types.ObjectId.isValid(userID)) {
		callback(error.USERID_INVALID);
	}
	user.findById(userID, function(err, user) {
		if (err) {
			callback(error.QUERY_DB_ERROR);
		} else {
			if (user == null) {
				callback(error.USER_UNDEFINED);
			} else {
				callback(null);
			}
		}
	})
};

module.exports.findUserByEmail= function(email, callback) {
	user.findOne({email: email}, function(err, user) {
		if (err) {
			callback(errorUser.QUERY_DB_ERROR, null);
		} else {
			if (user == null) {
				callback(null, null);
			} else {
				callback(null, user._id);
			}
		}
	})
};

module.exports.findUserByProp= function(sex, age, region, regionCode, nativeLand, callback) {
	user.findOne( { region: region,	age: age, sex: sex, regionCode: regionCode, nativeLand: nativeLand}, function(err, user) {
		if (err) {
			callback(errorUser.QUERY_DB_ERROR, null);
		} else {
			if (user == null) {
				callback(null, user);
			} else {
				callback(null, null);
			}
		}
	})
};
