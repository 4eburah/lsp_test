delete from cyclones_history 
where date_from = to_date('*load_date*', 'YYYYMMDD');

update cyclones_history 
set date_to = date_to - 1 
where date_to = to_date('*load_date*', 'YYYYMMDD');

merge into cyclones_history ch
using cyclones_stage s
on ch.id = s.id and ch.status = s.status and ch.date_to = s.dt - 1
when matched
	then update set date_to = s.dt
when not matched
	then insert (date_from, date_to, id, status) values(s.dt, s.dt, s.id, s.status);

