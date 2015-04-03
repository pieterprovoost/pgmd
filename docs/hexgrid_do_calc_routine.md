# do_calc
database: [obis](../)  
schema: [hexgrid](hexgrid)  

    
    
    /* Calculate indices on hexgrids
    evberghe 2011-07-07
    */
    
    	declare
    		retvar varchar(255); -- return variable
    		sqlstring varchar(10000);
    		starttime timestamp with time zone;
    		endtime timestamp with time zone;
    		csn varchar(18)[];
    		csl integer[];
    		esx integer; -- constant specifying the number of specimens to use for es() calculation
    		
    	begin
    		set search_path to hexgrid, public;
    		starttime:=clock_timestamp();
    		raise notice 'start function do_calc at %', starttime;
    		csn[1]:='calc_hexgrid5'; 
    /*		csn[2]:='map30m'; 
    		csn[3]:='map1d'; 
    		csn[4]:='map5d'; 
    		csn[5]:='map10d';
    */
    		esx:=50;
    	
    		raise notice 'create temp tables';
    		drop table if exists t1 cascade;
    		create table t1 as -- simplistic version - we're not integrating over the taxonomic hierarchy
    			select hex_id, drs.valid_id, count(*) as ni
    			from pos_hexgrid5 inner join obis.drs on pos_hexgrid5.pos_id=drs.position_id
    				inner join obis.tnames on drs.valid_id=tnames.id
    			where coalesce(drs.display, '1')='1' and rank_id=220
    			group by hex_id, drs.valid_id;
    		create index ix_hex_t1 on t1 using btree (hex_id);
    		create index ix_valid_t1 on t1 using btree (valid_id);
    
    		drop table if exists t2 cascade;
    		create table t2 as select hex_id, sum(ni) as n from t1 group by hex_id;
    		create index ix_hex_t2 on t2 using btree (hex_id);
    
    		drop table if exists t3 cascade;
    		create table t3 (valid_id integer, -- taxon
    			hex_id integer, -- map unit
    			n integer, -- number of records
    			hi real, -- term for summation to calculate shannon and hill numbers
    			si real, -- term for summation to calculate simpson
    			qi real, -- term for summation to calculate ...
    			esi real -- term for summation to calculate es(esx)
    		);
    		create index ix_hex_t3 ON t3 USING btree (hex_id);
    		
    		drop table if exists t4 cascade;
    		create table t4 (hex_id integer, 
    			n integer, 
    			shannon real, 
    			simpson real, 
    			max_p real, 
    			es real
    		); 
    		create index ix_hex_t4 ON t4 USING btree (hex_id);
    
    		drop table if exists t5 cascade;
    		create table t5 (hex_id integer, s integer);
    		create index ix_hex_t5 ON t5 USING btree (hex_id);
    
    		for i in 1..1 loop
    			raise notice 'calculations for %', csn[i];
    			execute 'insert into t3 
    				select valid_id, t1.hex_id, n,
    					-(1.0*ni/n*ln(1.0*ni/n)) as hi, (1.0*ni/n)^2 as si,
    					1.0*ni/n as qi,
    					case 
    						when n-ni>='||esx||' 
    							then 1-exp(lngamma(n-ni+1)+lngamma(n-'||esx||'+1)
    								-lngamma(n-ni-'||esx||'+1)-lngamma(n+1))
    						when n>='||esx||' then 1
    						else null
    					end as esi
    				from t1 inner join t2 on t1.hex_id=t2.hex_id;';
    
    			insert into t4 select hex_id, n, sum(hi) as shannon, sum(si) as simpson, 
    				max(qi) as max_p, sum(esi) as es 
    				from t3 group by hex_id, n;
    
    			insert into t5 select hex_id, count(*) from t1 group by hex_id;
    
    			execute 'truncate '||csn[i];
    
    			if i<6 then
    
    			-- assemble all the indices in the maps table
    			-- collect the geom from the geo schema
    				execute 'insert into '||csn[i]||'(hex_id, n, s, shannon, simpson, 
    						es, hill_1, hill_2, hill_inf, geom) 
    					select t4.hex_id, n, s, shannon, simpson, es, 
    						exp(shannon), 1/simpson, 1/max_p,
    						geom 
    					from t4 inner join t5 on t4.hex_id=t5.hex_id
    						--inner join hexgrid.'||regexp_replace(csn[i],'map','cs')||'
    						inner join hexgrid.hexgrid5
    							on t4.hex_id=hexgrid5.id;';
    				drop table t1; drop table t2; drop table t3; 
    				drop table t4; drop table t5;
    			end if;
    		end loop;
    
    	endtime:=clock_timestamp();
    	retvar:='do_calc finished in '||endtime-starttime;
    	return retvar;
    	end;
