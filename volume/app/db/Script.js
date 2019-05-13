var mongoose= require('mongoose'),
	error	= require('../configAndConstant/Error').SCRIPT_ERROR;

var scriptSch= mongoose.Schema({
	script: {
		type: String,
		default: ''
	}
});

var script = module.exports= mongoose.model('script', scriptSch);

module.exports.saveScript= function(scr, callback){
  	scr.save(callback);
}

module.exports.findInListId= function(id1, callback){
	script.find({'_id': { $in: [
		mongoose.Types.ObjectId(id1),
	]}}, function(err, docs){
		if (docs == null) {
			callback(error.SCRIPT_ERROR);
		} else {
			callback(error.null);
		}
	});
}

module.exports.findById= function(id, callback){
	console.log(id)
	script.find({'_id':
		mongoose.Types.ObjectId(id)
	}, function(err, data){
		if(err){
			console.log(err, null);
		}
	
		if(data.length == 0) {
			callback("No record found", null)
		}
	
		console.log(data[0].script);
		callback(null, data)
	});
}

module.exports.getLength = function(callback) {
	script.countDocuments({}, callback)
}

module.exports.getRandom = function(skip, limit, callback) {
	script.find().skip(skip).limit(limit).exec(callback);
}