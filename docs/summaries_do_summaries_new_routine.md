# do_summaries_new
database: [obis](../)  
schema: [summaries](summaries)  

    
    
    /* Create summary tables
    evberghe 2010-06-01, 2011-06-04
    Summary tables integrate number of records over the taxonomic classification - with and without keeping datasets separate
    Summaries are done for the various size grid cells, and for the globe. 
    added 2011-06-04: previously the function started with the smallest size square - now start with points.
    */
    
    	declare
    		retvar varchar(255); -- return variable
    		ranks record;
    		csn varchar(18)[];
    		csl integer[];
    		sqlstring varchar(10000);
    		
    	begin
    
    	set search_path to summaries;
    
    	-- first create a help table with unique combinations of position_id and resource
    	raise notice 'drop temporary tables and recreate';
    	drop table if exists _tmp1;
    	create table _tmp1(id serial, position_id integer, resource_id integer);
    	insert into _tmp1(position_id, resource_id) select distinct position_id, resource_id from obis.drs;
    	CREATE INDEX ix_tmp1_position ON _tmp1 (position_id);
    	CREATE INDEX ix_tmp1_resource ON _tmp1 (resource_id);
    
    	-- now create a second help table to capture the results of the calculations, as we push sums up the tax hierarchy
    	drop table if exists _tmp2;
    	create table _tmp2(pr_id integer, valid_id integer, nexcl integer, nincl integer);
    
    	--seed the table with the counts; both nexcl and nincl set to the number of records identified to the taxon
    	insert into _tmp2(pr_id, valid_id, nexcl, nincl)
    		select _tmp1.id, valid_id, count(*), count(*)
    			from obis.drs inner join _tmp1 using(position_id, resource_id)
    			group by _tmp1.id, valid_id;
    	CREATE INDEX ix_tmp2_cr ON _tmp2 (pr_id);
    	CREATE INDEX ix_tmp2_valid ON _tmp2 (valid_id);
    	ALTER TABLE summaries._tmp2 ADD CONSTRAINT pk_tmp2 PRIMARY KEY(pr_id, valid_id);
    
    	for ranks in select distinct rank_id from obis.tnames where rank_id is not null and rank_id>0 order by rank_id desc loop
    		raise notice 'doing rank %', ranks.rank_id;
    
    		-- first update existing records in _tmp2
    		update _tmp2 set nincl=_tmp2.nincl+f.s from 
    			(select p.pr_id, p.valid_id, sum(c.nincl) as s from _tmp2 p, _tmp2 c, obis.tnames, obis.tnames pnames
    				where p.pr_id=c.pr_id 
    					and c.valid_id=tnames.id and p.valid_id=pnames.valid_id
    					and tnames.parent_id=pnames.id
    					and tnames.rank_id=ranks.rank_id 
    					and tnames.parent_id is not null
    				group by p.pr_id, p.valid_id
    			) f
    		where f.pr_id=_tmp2.pr_id and f.valid_id=_tmp2.valid_id;
    
    		-- then create new records in _tmp2 where needed
    		insert into _tmp2(pr_id, valid_id, nexcl, nincl)
    		select c.pr_id, pnames.valid_id, 0, sum(c.nincl)
    		from _tmp2 c inner join obis.tnames on c.valid_id=tnames.id
    			inner join obis.tnames pnames on tnames.parent_id=pnames.id
    			left join _tmp2 p on c.pr_id=p.pr_id and p.valid_id=pnames.valid_id
    			where p.pr_id is null and tnames.rank_id=ranks.rank_id and tnames.parent_id is not null
    		group by c.pr_id, pnames.valid_id;
    
    	end loop;
    
    	raise notice 'now truncate results tables, and re-populate them';
    	csn[0]:='points'; csl[0]=12;
    	csn[1]:='ds6m'; csl[1]=12;
    	csn[2]:='ds30m'; csl[2]=10;
    	csn[3]:='ds1d'; csl[3]=8;
    	csn[4]:='ds5d'; csl[4]=6;
    	csn[5]:='ds10d'; csl[5]=4;
    /*	
    	raise notice E'doing points %', csn[0];
    	execute 'truncate points_res_valids';
    	execute 'truncate points_valids';
    	execute 'insert into points_res_valids(cscode, position_id, resource_id, valid_id, nexcl, nincl, geom)
    		select cs6m, position_id, resource_id, valid_id, nexcl, nincl, positions.geom
    		from _tmp2 inner join _tmp1 on _tmp2.pr_id=_tmp1.id
    			inner join obis.positions on _tmp1.position_id=positions.id';
    	execute 'insert into points_valids(cscode, position_id, valid_id, nexcl, nincl, geom)
    		select cscode, position_id, valid_id, sum(nexcl), sum(nincl), geom 
    		from points_res_valids group by cscode, position_id, valid_id, geom';
    		
    	for i in 1..5 loop
    		raise notice E'doing squares %', csn[i];
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
    	truncate hlobal_res_valids;
    	truncate hlobal_valids;
    	insert into hlobal_res_valids(resource_id, valid_id, nexcl, nincl)
    		select resource_id, valid_id, sum(nexcl), sum(nincl) 
    		from ds10d_res_valids group by resource_id, valid_id;
    	insert into hlobal_valids(valid_id, nexcl, nincl)
    		select valid_id, sum(nexcl), sum(nincl) 
    		from hlobal_res_valids group by valid_id;
    */	
    	retvar:='Return string: '||invar;
    	return retvar;
    	end;
