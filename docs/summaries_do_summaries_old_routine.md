# do_summaries_old
database: [obis](../)  
schema: [summaries](summaries)  

    
    
    /* Create summary tables
    evberghe 2010-06-01
    */
    
    	declare
    		retvar varchar(255); -- return variable
    		ranks record;
    		cellsizename record;
    		sqlstring varchar(10000);
    		
    	begin
    	set search_path to summaries;
    	raise notice 'create temporary tables';
    
    	-- first create a help table with unique combinations of cs6m and resource
    	-- join with positions table to create only cs6m squares with data in them
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
    			group by _tmp1.id, valid_id;
    	CREATE INDEX ix_tmp2_cr ON _tmp2 (cr_id);
    	CREATE INDEX ix_tmp2_valid ON _tmp2 (valid_id);
    
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
    
    	raise notice 'now trucate results tables, and re-populate them';
    
    	raise notice 'cs6m';
    	truncate cs6m_res_valids;
    	insert into cs6m_res_valids(cscode, resource_id, valid_id, nexcl, nincl, geom)
    		select cs6m, resource_id, valid_id, nexcl, nincl,
    			public.st_geomfromtext(geo.get_wkt_from_csquare(cs6m),4326)
    		from _tmp2 inner join _tmp1 on _tmp2.cr_id=_tmp1.id;
    	truncate cs6m_valids;
    	insert into cs6m_valids(cscode, valid_id, nexcl, nincl, geom)
    		select cscode, valid_id, sum(nexcl), sum(nincl), geom 
    		from cs6m_res_valids group by cscode, valid_id, geom;
    
    	raise notice 'cs30m';
    	truncate cs30m_res_valids;
    	insert into cs30m_res_valids(cscode, resource_id, valid_id, nexcl, nincl, geom)
    		select substring(cs6m_res_valids.cscode from 1 for 10), resource_id, valid_id, sum(nexcl), sum(nincl), cs30m.geom
    		from cs6m_res_valids inner join geo.cs30m on substring(cs6m_res_valids.cscode from 1 for 10)=cs30m.cscode
    		group by substring(cs6m_res_valids.cscode from 1 for 10),resource_id, valid_id, cs30m.geom;
    	truncate cs30m_valids;
    	insert into cs30m_valids(cscode, valid_id, nexcl, nincl, geom)
    		select cscode, valid_id, sum(nexcl), sum(nincl), geom 
    		from cs30m_res_valids group by cscode, valid_id, geom;
    
    	raise notice 'cs1d';
    	truncate cs1d_res_valids;
    	insert into cs1d_res_valids(cscode, resource_id, valid_id, nexcl, nincl, geom)
    		select substring(cs30m_res_valids.cscode from 1 for 8), resource_id, valid_id, sum(nexcl), sum(nincl), cs1d.geom 
    		from cs30m_res_valids inner join geo.cs1d on substring(cs30m_res_valids.cscode from 1 for 8)=cs1d.cscode 
    		group by substring(cs30m_res_valids.cscode from 1 for 8), resource_id, valid_id, cs1d.geom;
    	truncate cs1d_valids;
    	insert into cs1d_valids(cscode, valid_id, nexcl, nincl, geom)
    		select cscode, valid_id, sum(nexcl), sum(nincl), geom 
    		from cs1d_res_valids group by cscode, valid_id, geom;
    	
    	raise notice 'cs5d';
    	truncate cs5d_res_valids;
    	insert into cs5d_res_valids(cscode, resource_id, valid_id, nexcl, nincl, geom)
    		select substring(cs1d_res_valids.cscode from 1 for 6), resource_id, valid_id, sum(nexcl), sum(nincl), cs5d.geom 
    		from cs1d_res_valids inner join geo.cs5d on substring(cs1d_res_valids.cscode from 1 for 6)=cs5d.cscode
    		group by substring(cs1d_res_valids.cscode from 1 for 6), resource_id, valid_id, cs5d.geom;
    	truncate cs5d_valids;
    	insert into cs5d_valids(cscode, valid_id, nexcl, nincl, geom)
    		select cscode, valid_id, sum(nexcl), sum(nincl), geom 
    		from cs5d_res_valids group by cscode, valid_id, geom;
    
    	raise notice 'cs10d';
    	truncate cs10d_res_valids;
    	insert into cs10d_res_valids(cscode, resource_id, valid_id, nexcl, nincl, geom)
    		select substring(cs5d_res_valids.cscode from 1 for 4), resource_id, valid_id, sum(nexcl), sum(nincl), cs10d.geom 
    		from cs5d_res_valids inner join geo.cs10d on substring(cs5d_res_valids.cscode from 1 for 4)=cs10d.cscode
    		group by substring(cs5d_res_valids.cscode from 1 for 4), resource_id, valid_id, cs10d.geom;
    	truncate cs10d_valids;
    	insert into cs10d_valids(cscode, valid_id, nexcl, nincl, geom)
    		select cscode, valid_id, sum(nexcl), sum(nincl), geom 
    		from cs10d_res_valids group by cscode, valid_id, geom;
    	
    	raise notice 'global counts';
    	truncate global_res_valids;
    	insert into global_res_valids(resource_id, valid_id, nexcl, nincl)
    		select resource_id, valid_id, sum(nexcl), sum(nincl) 
    		from cs10d_res_valids group by resource_id, valid_id;
    
    	truncate global_valids;
    	insert into global_valids(valid_id, nexcl, nincl)
    		select valid_id, sum(nexcl), sum(nincl) 
    		from global_res_valids group by valid_id;
    	
    	retvar:='Return string: '||invar;
    	return retvar;
    	end;
