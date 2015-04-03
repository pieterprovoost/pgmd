# overview
database: [obis](../)  
schema: [jcleary](jcleary)  

    
    declare
    begin
    	set search_path to jcleary, public;
    
    	-- make the intersection between boundary and 1d and 5d squares
    	truncate b_cs1d;
    	insert into b_cs1d(cscode, geom) select cs1d.cscode, st_intersection(boundary.the_geom, cs1d.geom)  
    		from boundary, geo.cs1d
    		where st_intersects(boundary.the_geom, cs1d.geom);
    	truncate b_cs5d;
    	insert into b_cs5d(cscode, geom) select cs5d.cscode, st_intersection(boundary.the_geom, cs5d.geom)  
    		from boundary, geo.cs5d
    		where st_intersects(boundary.the_geom, cs5d.geom);
    	-- extract the relevant data
    	execute extract_regionaldata('');
    	-- calculate all tables
    	execute do_calcthemall('');
    	-- and copy them to the /mnt drive
    	
    	-- JC - not doing this anymore, will just connect ArcGIS to the DB to get the data
    	-- JC - left in some sample code below just in case
    	-- copy all1d to '/pgdata/resultsets/jcleary/all1d.csv' delimiter ',' csv header quote '"';
    	-- copy all5d to '/pgdata/resultsets/jcleary/all5d.csv' delimiter ',' csv header quote '"';
    
       return '';
    
    end;
    
