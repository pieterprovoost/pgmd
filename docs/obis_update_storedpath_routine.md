# update_storedpath
database: [obis](../)  
schema: [obis](obis)  

    
    
    /* 
    recalculate stored path for the whole tnames table 
    
    */
    
    	declare
    		f_starttime timestamp with time zone;
    		f_endtime timestamp with time zone;
    		rcount integer;
    		done boolean;
    		retvar character varying(255);
    		
    	begin
    		f_starttime:=clock_timestamp();
    		raise notice 'start function load_addtnames at %', f_starttime;
    		
    		set search_path to obis;
    
    		raise notice 'clearing stored path';
    		update tnames set storedpath=null;
    
    		raise notice 'constructing new storedpaths';
    		update tnames set storedpath='x' where tname='Biota';
    		done:=false;
    		while not done loop
    			update tnames set storedpath=parents.storedpath||parents.id||'x'
    			from tnames parents
    			where tnames.parent_id=parents.id 
    				and parents.storedpath is not null and tnames.storedpath is null;
    			get diagnostics rcount=row_count;
    			raise notice 'number of records updated: %', rcount;
    			done=not found;
    		end loop;
    		
    		f_endtime:=clock_timestamp();
    		retvar:='updating stored path finished in '||f_endtime-f_starttime;
    	return retvar;
    	end;
