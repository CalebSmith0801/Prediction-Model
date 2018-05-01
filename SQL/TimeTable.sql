use cargo;

#can take a while to run depending on number of locations and table length, 
#make sure your preferences time out setting is high enough; current time to run (166 seconds)

create view status_times as (
	select o.id as OrderID, o.location_id as location_id, os.created_at as created_at, os.status as status from orders o join order_statuses os ON o.id = os.order_id);


/*creates separate columns for submitted, Processing,..etc with their respective created_at time*/
/*Results in columns that have lots of nulls*/
create view status_times_extended as (
  select
    status_times.*,
    case when status = "submitted" then created_at end as Submitted, 
    case when status = "processing" then created_at end as Processing,
    case when status = "requesting" then created_at end as Requesting,
    case when status = "accepted" then created_at end as Accepted,
    case when status = "arrived" then created_at end as Arrived,
    case when status = "delivering" then created_at end as Delivering,
    case when status = "delivered" then created_at end as Delivered
  from status_times
);


/*Cleans up status_times_extended view by removing the status and created_at columns as well as all the null
values from the Submitted, Processing,... columns*/    
create view status_times_pivot as (
    select * from(
		select
			OrderID, location_id, 
			min(Submitted) as Submitted, /*min can be used since there is only 1 value and 6 nulls*/
			min(Processing) as Processing,
			min(Requesting) as Requesting,
			min(Accepted) as Accepted,
			min(Arrived) as Arrived,
			min(Delivering) as Delivering,
			min(Delivered) as Delivered
		from status_times_extended
		group by OrderID 
	) t 
    
    where Processing is not null and Requesting is not null and  /*some early orders don't have any data in some columns*/
	Accepted is not null and Arrived is not null and 
	Delivering is not null and Delivered is not null 
	
    and Requesting < Accepted and Accepted < Arrived and 
	Arrived < Delivering and Delivering < Delivered /*necessary because some data is messed up (EX order#27818)*/
);


create table time as(
	select *, Submitted_Time + Processing_Time as Time_Till_Driver_Needed,           /*didn't include requested_time because that is just the small window where*/
			  Accepted_Time + Arrived_Time + Delivery_Time as Time_Till_Driver_Back, /*the restaraunt has finished the order and is waiting for a driver*/
              Submitted_Time + Processing_Time + Requesting_Time + Accepted_Time + Arrived_Time + Delivery_Time as Total from (
		select location_id, 
			AVG(TIME_TO_SEC(TIMEDIFF(Processing, Submitted))) as 'Submitted_Time', 
			AVG(TIME_TO_SEC(TIMEDIFF(Requesting, Processing))) as 'Processing_Time',
			AVG(TIME_TO_SEC(TIMEDIFF(Accepted, Requesting))) as 'Requesting_Time',
			AVG(TIME_TO_SEC(TIMEDIFF(Arrived, Accepted))) as 'Accepted_Time',
			AVG(TIME_TO_SEC(TIMEDIFF(Delivering, Arrived))) as 'Arrived_Time',
			AVG(TIME_TO_SEC(TIMEDIFF(Delivered, Delivering))) as 'Delivery_Time'
			from status_times_pivot 
            
            where TIME_TO_SEC(TIMEDIFF(Delivered, Submitted)) < 3600 /*Ignore orders that took longer than 1 hour (outliers)*/
            group by location_id) t);


/*default restaurant time if location_id is not in table*/
insert into `time` 
	(location_id, Submitted_Time, Processing_Time, Requesting_Time, Accepted_Time, Arrived_Time, 
    Delivery_Time, Time_Till_Driver_Needed, Time_Till_Driver_Back, Total) 
    
	VALUES (-1, (select avg(Submitted_Time) from (Select * from time) t), 
    (select avg(Processing_Time) from (Select * from time) t), 
    (Select avg(Requesting_Time) from (Select * from time) t), 
    (select avg(Accepted_Time) from (Select * from time) t), 
    (select avg(Arrived_Time) from (Select * from time) t), 
    (select avg(Delivery_Time) from (Select * from time) t),
    (select avg(Time_Till_Driver_Needed) from (Select * from time) t), 
    (select avg(Time_Till_Driver_Back) from (Select * from time) t), 
    (select avg(Total) from (Select * from time) t));
    
drop view status_times;
drop view status_times_extended;
drop view status_times_pivot;