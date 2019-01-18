### $group

`db.stu.aggregate(
	{$match:{age:{$gt:20}}}
	{$group:{_id:"$Gender", counter:{$sum:1}}}
)`