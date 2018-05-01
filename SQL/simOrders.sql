#creates a simulation table for prophet to calculate a prediction for 4/17/2018
#so we can test it with the actual data of 4/17/2018

create table simOrders as(
	select * from (
		select * from orders where submitted_at < '2018-04-16 07:00:00' order by submitted_at desc) t);