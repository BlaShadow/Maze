#! config file

import util

config = {
	"img":"truck.png",
	"maze":{ 
			"width":600,
			"height":600,
			"item":30,
			"space": util.parse_file('ground') 
		}
}

