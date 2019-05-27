var ERROR = {
	'QUERY_DB_ERROR': {
		code: 1,
		message: "x"
	},
	'USERID_INVALID': {
		code: 2,
		message: "x"
	},
	'USER_UNDEFINED': {
		code: 3,
		message: "x"
	},
	'SCRIPTID_INVALID': {
		code: 4,
		message: "Script ID invalid"
	}
};

module.exports.ERROR = ERROR;

var SCRIPT_ERROR = {
	'SCRIPTID_INVALID': {
		code: 4,
		message: "Script ID invalid"
	}
};
module.exports.SCRIPT_ERROR = SCRIPT_ERROR;

var SCRIPT_TYPE_ERROR = {
	'SCRIPTID_TYPE_INVALID': {
		code: 8,
		message: "Script ID invalid"
	}
};
module.exports.SCRIPT_TYPE_ERROR = SCRIPT_TYPE_ERROR;

var USER_ERROR = {
	'REQ_INFO_WRONG': {
		code: 5,
		message: "Request with wrong info"
	},
	'USER_EXIST': {
		code: 7,
		message: "User with email is exist"
	},
	'QUERY_DB_ERROR': {
		code: 1,
		message: "x"
	}
}
module.exports.USER_ERROR = USER_ERROR;

var REGION_ERROR = {
	'QUERY_DB_ERROR': {
		code: 1,
		message: "x"
	},
	'REGION_ID_INVALID': {
		code: 6,
		message: "Region ID invalid"
	}
}
module.exports.REGION_ERROR = REGION_ERROR;