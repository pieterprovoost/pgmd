# do_calc
database: [obis](../)  
schema: [calc](calc)  

    
    
    /* Calculate indices
    evberghe 2010-06-01
    turned into function 2010-07-03
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
    		set search_path to calc, public;
    		starttime:=clock_timestamp();
    		raise notice 'start function do_calc at %', starttime;
    		csn[1]:='map6m'; csl[1]=12;
    		csn[2]:='map30m'; csl[2]=10;
    		csn[3]:='map1d'; csl[3]=8;
    		csn[4]:='map5d'; csl[4]=6;
    		csn[5]:='map10d'; csl[5]=4;
    		csn[6]:='mapglobal';csl[6]=0;
    		esx:=50;
    	
    		raise notice 'create temp tables';
    		drop table if exists t1 cascade;
    		create table t1 as 
    			select cs6m_valids.valid_id, cscode, nincl as ni 
    			from summaries.cs6m_valids inner join obis.tnames on cs6m_valids.valid_id=tnames.id
    			where coalesce(tnames.display,'1')='1' and rank_id=220; -- same set of indices can be calculated on other ranks
    		create index ix_cscode_t1 on t1 using btree (cscode);
    		create index ix_valid_id_t1 on t1 using btree (valid_id);
    		drop table if exists t6 cascade;
    		create table t6 (valid_id integer, cscode character varying(12), ni integer);
    
    		drop table if exists t2 cascade;
    		create table t2 as select cscode, sum(ni) as n from t1 group by cscode;
    		create index ix_cscode_t2 on t2 using btree (cscode);
    		drop table if exists t7 cascade;
    
    		drop table if exists t3 cascade;
    		create table t3 (valid_id integer, -- taxon
    			cscode character varying(12), -- map unit
    			n integer, -- number of species
    			hi real, -- term forsummation to calculate shannon and hill numbers
    			si real, -- term forsummation to calculate simpson
    			qi real, -- term forsummation to calculate ...
    			esi real -- term for summation to calculate es(esx)
    		);
    		create index ix_cscode_t3 ON t3 USING btree (cscode);
    		
    		drop table if exists t4 cascade;
    		create table t4 (cscode character varying(12), 
    			n integer, 
    			shannon real, 
    			simpson real, 
    			max_p real, 
    			es real
    		); 
    		create index ix_cscode_t4 ON t4 USING btree (cscode);
    
    		drop table if exists t5 cascade;
    		create table t5 (cscode character varying(12), s integer);
    		create index ix_cscode_t5 ON t5 USING btree (cscode);
    
    		for i in 1..6 loop
    			raise notice 'calculations for %', csn[i];
    			execute 'insert into t3 
    				select valid_id, t1.cscode, n,
    					-(1.0*ni/n*ln(1.0*ni/n)) as hi, (1.0*ni/n)^2 as si,
    					1.0*ni/n as qi,
    					case 
    						when n-ni>='||esx||' 
    							then 1-exp(lngamma(n-ni+1)+lngamma(n-'||esx||'+1)
    								-lngamma(n-ni-'||esx||'+1)-lngamma(n+1))
    						when n>='||esx||' then 1
    						else null
    					end as esi
    				from t1 inner join t2 on t1.cscode=t2.cscode;';
    
    			insert into t4 select cscode, n, sum(hi) as shannon, sum(si) as simpson, 
    				max(qi) as max_p, sum(esi) as es 
    				from t3 group by cscode, n;
    
    			insert into t5 select cscode, count(*) from t1 group by cscode;
    
    			execute 'truncate '||csn[i];
    
    			if i<6 then
    
    			-- assemble all the indices in the maps table
    			-- collect the geom from he geo schema
    				execute 'insert into '||csn[i]||'(cscode, n, s, shannon, simpson, 
    						es, hill_1, hill_2, hill_inf, geom) 
    					select t4.cscode, n, s, shannon, simpson, es, 
    						exp(shannon), 1/simpson, 1/max_p,
    						geom 
    					from t4 inner join t5 on t4.cscode=t5.cscode
    						inner join geo.'||regexp_replace(csn[i],'map','cs')||'
    							on t4.cscode='||regexp_replace(csn[i],'map','cs')||'.cscode;';
    			-- get ready for the next resolution
    			-- aggregate number of records per taxon and per square in next greater size square
    			-- special case for global map has cscode=''
    				execute 'insert into t6 
    					select valid_id, 
    						substring(cscode from 1 for '||csl[i+1]||'), sum(ni) as ni 
    					from t1 
    					group by valid_id, substring(cscode from 1 for '||csl[i+1]||')';
    				truncate table t1; insert into t1 select * from t6;
    				
    				truncate table t2;
    				insert into t2 select cscode, sum(ni) as n from t1 group by cscode; 
    
    			-- rest of the tables are filled in in the statements above, 
    			-- should be emptied to start on new cycle
    				truncate table t3; truncate table t4;
    				truncate table t5; truncate table t6; 
    			else
    
    			-- special case globalmap, does not have id or cscode
    				execute 'insert into '||csn[i]||' 
    					select n, s, shannon, simpson, es, 
    						exp(shannon), 1/simpson, 1/max_p 
    					from t4 inner join t5 on t4.cscode=t5.cscode';
    				
    			-- cleaning up
    				drop table t1; drop table t2; drop table t3; 
    				drop table t4; drop table t5; drop table t6; 
    			end if;
    		end loop;
    
    	endtime:=clock_timestamp();
    	retvar:='do_calc finished in '||endtime-starttime;
    	return retvar;
    	end;
