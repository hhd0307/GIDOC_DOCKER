var mongoose= require('mongoose');
var ObjectId = mongoose.Schema.Types.ObjectId;

var fileSch= mongoose.Schema({
	userId: ObjectId,
	scripId: ObjectId,
	fileInfo: {
		type: String,
		default: ''
	},
	duration: {
		type: Number,
		default: 0
	},
	projectRate: {
		type: Number,
		default: 0
	},
	snr: {
		type: Number,
		default: 0
	}
});

var file = module.exports= mongoose.model('file', fileSch);

module.exports.saveFile= function(scr, callback){
  scr.save(callback);
}

module.exports.saveFiles= function(files, callback){
	file.insertMany(files, callback);
}

module.exports.getAllInfo= function(callback){
	file.aggregate([
	    {
	        $lookup: {
	            "from": "users",
	            "localField": "userId",
	            "foreignField": "_id",
	            "as": "user"
	        }
	    },
	    {
	        $unwind: "$user"
	    },
	    {
	        $project: {
	            _id: 1,
	            fileInfo: 1,
	            scripId: 1,
	            duration: 1,
	            projectRate: 1,
	            snr: 1,
	            userId: 1,
	            ageId: "$user.ageId",
	            sexId: "$user.sexId",
	            regionId: "$user.regionId"
	        }
	    },
	    {
	        $lookup: {
	            "from": "regions",
	            "localField": "regionId",
	            "foreignField": "_id",
	            "as": "region"
	        }
	    },
	    {
	        $unwind: "$region"
	    },
	    {
	        $project: {
	            _id: 1,
	            fileInfo: 1,
	            scripId: 1,
	            duration: 1,
	            projectRate: 1,
	            snr: 1,
	            userId: 1,
	            ageId : 1,
	            sexId : 1,
	            region : "$region.region"
	        }
	    },
	    {
	        $lookup: {
	            "from": "scripts",
	            "localField": "scripId",
	            "foreignField": "_id",
	            "as": "script"
	        }
	    },
	    {
	        $unwind: "$script"
	    },
	    {
	        $project: {
	            _id: 1,
	            fileInfo: 1,
	            duration: 1,
	            projectRate: 1,
	            snr: 1,
	            userId: 1,
	            ageId: 1,
	            sexId: 1,
	            region: 1,
	            script: "$script.script"
	        }
	    }
	], callback);
}