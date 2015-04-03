# do_summaries
database: [obis](../)  
schema: [summaries](summaries)  

    
    
    /* Create summary tables
    evberghe 2010-06-01
    */
    
    	declare
    		retvar varchar(255); -- return variable
    		ranks record;
    		csn varchar(18)[];
    		csl integer[];
    		sqlstring varchar(10000);
    		
    	begin
    
    	set search_path to summaries;
    
    	-- first create a help table with unique combinations of cs6m and resource
    	-- join with positions table to create only cs6m squares with data in them
    	raise notice 'drop temporary tables and recreate';
    	drop table if exists _tmp1;
    	create table _tmp1(id serial, cs6m character varying(12), resource_id integer);
    	insert into _tmp1(cs6m, resource_id) 
    		select distinct cs6m, resource_id from obis.drs 
    		inner join obis.positions on drs.position_id=positions.id;
    	CREATE INDEX ix_tmp1_cscode ON _tmp1 (cs6m);
    	CREATE INDEX ix_tmp1_resource ON _tmp1 (resource_id);
    
    	-- now create a second help table to capture the results of the calculations, as we push sums up the tax hierarchy
    	drop table if exists _tmp2;
    	create table _tmp2(cr_id integer, valid_id integer, nexcl integer, nincl integer);
    
    	--seed the table with the counts; both nexcl and nincl set to the number of records identified to the taxon
    	insert into _tmp2(cr_id, valid_id, nexcl, nincl)
    		select _tmp1.id, valid_id, count(*), count(*)
    			from obis.drs inner join obis.positions on drs.position_id=positions.id
    				inner join _tmp1 on _tmp1.cs6m=positions.cs6m and _tmp1.resource_id=drs.resource_id
    			where coalesce(display,'1')='1'
    			group by _tmp1.id, valid_id;
    	CREATE INDEX ix_tmp2_cr ON _tmp2 (cr_id);
    	CREATE INDEX ix_tmp2_valid ON _tmp2 (valid_id);
    	ALTER TABLE summaries._tmp2 ADD CONSTRAINT pk_tmp2 PRIMARY KEY(cr_id, valid_id);
    
    	for ranks in select distinct rank_id from obis.tnames where rank_id is not null and rank_id>0 order by rank_id desc loop
    		raise notice 'doing rank %', ranks.rank_id;
    
    		-- first update existing records in _tmp2
    		update _tmp2 set nincl=_tmp2.nincl+f.s from 
    			(select p.cr_id, p.valid_id, sum(c.nincl) as s from _tmp2 p, _tmp2 c, obis.tnames, obis.tnames pnames
    				where p.cr_id=c.cr_id 
    					and c.valid_id=tnames.id and p.valid_id=pnames.valid_id
    					and tnames.parent_id=pnames.id
    					and tnames.rank_id=ranks.rank_id and tnames.parent_id is not null
    				group by p.cr_id, p.valid_id
    			) f
    		where f.cr_id=_tmp2.cr_id and f.valid_id=_tmp2.valid_id;
    
    		-- then create new records in _tmp2 where needed
    		insert into _tmp2(cr_id, valid_id, nexcl, nincl)
    		select c.cr_id, pnames.valid_id, 0, sum(c.nincl)
    		from _tmp2 c inner join obis.tnames on c.valid_id=tnames.id
    			inner join obis.tnames pnames on tnames.parent_id=pnames.id
    			left join _tmp2 p on c.cr_id=p.cr_id and p.valid_id=pnames.valid_id
    			where p.cr_id is null and tnames.rank_id=ranks.rank_id and tnames.parent_id is not null
    		group by c.cr_id, pnames.valid_id;
    
    	end loop;
    
    	raise notice 'now truncate results tables, and re-populate them';
    	csn[1]:='cs6m'; csl[1]=12;
    	csn[2]:='cs30m'; csl[2]=10;
    	csn[3]:='cs1d'; csl[3]=8;
    	csn[4]:='cs5d'; csl[4]=6;
    	csn[5]:='cs10d'; csl[5]=4;
    	
    	raise notice E'doing squares % \n', csn[1];
    	execute 'truncate '||csn[1]||'_res_valids';
    	execute 'truncate '||csn[1]||'_valids';
    	execute 'insert into '||csn[1]||'_res_valids(cscode, resource_id, valid_id, nexcl, nincl, geom)
    		select _tmp1.'||csn[1]||', resource_id, valid_id, nexcl, nincl, '||csn[1]||'.geom
    		from _tmp2 inner join _tmp1 on _tmp2.cr_id=_tmp1.id
    			inner join geo.'||csn[1]||' on _tmp1.'||csn[1]||'='||csn[1]||'.cscode';
    	execute 'insert into '||csn[1]||'_valids(cscode, valid_id, nexcl, nincl, geom)
    		select cscode, valid_id, sum(nexcl), sum(nincl), geom 
    		from '||csn[1]||'_res_valids group by cscode, valid_id, geom';
    		
    	for i in 2..5 loop
    		raise notice E'doing squares % \n', csn[i];
    		execute 'truncate '||csn[i]||'_res_valids';
    		execute 'truncate '||csn[i]||'_valids';
    		execute 'insert into '||csn[i]||'_res_valids(cscode, resource_id, valid_id, nexcl, nincl, geom)
    			select substring('||csn[i-1]||'_res_valids.cscode from 1 for '||csl[i]||'), 
    				resource_id, valid_id, sum(nexcl), sum(nincl), '||csn[i]||'.geom
    			from '||csn[i-1]||'_res_valids inner join geo.'||csn[i]||' 
    				on substring('||csn[i-1]||'_res_valids.cscode from 1 for '||csl[i]||')='||csn[i]||'.cscode
    			group by substring('||csn[i-1]||'_res_valids.cscode from 1 for '||csl[i]||'),resource_id, valid_id, '||csn[i]||'.geom';
    		execute 'insert into '||csn[i]||'_valids(cscode, valid_id, nexcl, nincl, geom)
    			select cscode, valid_id, sum(nexcl), sum(nincl), geom 
    			from '||csn[i]||'_res_valids group by cscode, valid_id, geom';
    	end loop;
    
    	raise notice 'global counts';
    	truncate global_res_valids;
    	truncate global_valids;
    	insert into global_res_valids(resource_id, valid_id, nexcl, nincl)
    		select resource_id, valid_id, sum(nexcl), sum(nincl) 
    		from cs10d_res_valids group by resource_id, valid_id;
    	insert into global_valids(valid_id, nexcl, nincl)
    		select valid_id, sum(nexcl), sum(nincl) 
    		from global_res_valids group by valid_id;
    	
    	retvar:='Return string: '||invar;
    	return retvar;
    	end;
