# do_simplify_fao
database: [obis](../)  
schema: [geo](geo)  

    
    /* expexts to find a table geo.fao, with the original fao fishing areas
       will reduce them to themain fishing areas, aggregating everything below the main areas
       and correct someof themistakes caused by the aggregation;
       afterwards get rid of all points falling on straight lines.
       table fao will be replaced with the simplified version, old version is preserved in fao_complete
    */
    	declare
    		s varchar(255); -- return variable
    		
    	begin
    		drop table if exists geo.fao2;
    
    		create table geo.fao2 as
    		select f_area::integer as id, st_union(geom) as geom from geo.fao group by f_area;
    
    		update geo.fao2 set id=-1 where id is null; -- -1 are landlocked areas
    		ALTER TABLE geo.fao2 ADD CONSTRAINT pk_fao2 PRIMARY KEY(id);
    		CREATE INDEX ix_fao_geom ON geo.fao2 USING gist (geom);
    
    		update geo.fao2 set geom=st_makepolygon(st_exteriorring(geom)) where geometrytype(geom)='POLYGON';
    
    		update geo.fao2 set geom=g.geom3 from (
    			select id, st_union(geom2) as geom3 from (
    				select id, st_makepolygon(st_exteriorring((st_dump(geom)).geom)) as geom2 
    				from geo.fao2 where geometrytype(geom)='MULTIPOLYGON'
    			) f group by id
    		) g where fao2.id=g.id;
    
    		update geo.fao2 set geom=h.geom from (
    			select st_union(g.geom) as geom from (
    				select geom from (
    					select (st_dump(geom)).geom from geo.fao2 
    					where id=-1
    				) f where st_disjoint(f.geom, st_geomfromtext('POLYGON((100 14,150 14, 150 -7,100 -7, 100 14))',4326))
    			) g 
    		) h where fao2.id=-1;
    
    		update geo.fao2 set geom=st_simplifypreservetopology(geom, 0.0001);
    
    		alter table geo.fao rename to fao_complete;
    		alter table geo.fao2 rename to fao;
    		s:='Return string: '||i||'.';
    		return s;
    	end;
