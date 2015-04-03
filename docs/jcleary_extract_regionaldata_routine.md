# extract_regionaldata
database: [obis](../)  
schema: [jcleary](jcleary)  

    
    declare
    begin
    set search_path to jcleary, public;
    drop table if exists t0;
    create table t0 as 
    	select valid_id, position_id, coordinateprecision, cs6m, depth 
    	from obis.drs, b_cs5d, obis.positions
    	where coalesce(display,'1')='1' and positions.id=position_id and substring(cs6m from 1 for 6)=cscode
    	and (st_area(b_cs5d.geom)=25 or (st_area(b_cs5d.geom)<25 and st_intersects(positions.geom, b_cs5d.geom)));
    
       return '';
    end;
    
