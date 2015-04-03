# do_calc
database: [obis](../)  
schema: [jcleary](jcleary)  

    
    
    /* Calculate indices
    */
    
    	declare
    		retvar varchar(255); -- return variable
    		starttime timestamp with time zone;
    		endtime timestamp with time zone;
    		esx integer; -- constant specifying the number of specimens to use for es() calculation
    		sqlstr varchar(1024);
    		cslength integer;
    		
    	begin
    		set search_path to jcleary, public;
    		esx:=50;
    	
    		raise notice 'doing table %', tablename;
    		cslength:=case when resolname='5d' then 6 else 8 end;
    		raise notice 'create temp tables';
    		drop table if exists t1 cascade;
    		sqlstr:='create table t1 as 
    			select t0.valid_id, substring(cs6m from 1 for '
    			||cslength||') as cscode, count(*) as ni 
    			from t0 inner join obis.tnames on t0.valid_id=tnames.id ' 
    			||joinstr||' where coalesce(coordinateprecision,0)<50000 '
    			||wherestr||' group by t0.valid_id, cscode;';
    		raise notice E'query:\n %', sqlstr;
    		execute sqlstr;
    
    		create index ix_cscode_t1 on t1 using btree (cscode);
    		create index ix_valid_id_t1 on t1 using btree (valid_id);
    
    		drop table if exists t2 cascade;
    		create table t2 as select cscode, sum(ni) as n from t1 group by cscode;
    		create index ix_cscode_t2 on t2 using btree (cscode);
    
    		drop table if exists t3 cascade;
    		create table t3 (valid_id integer, -- taxon
    			cscode character varying(12), -- map unit
    			n integer, -- number of species
    			hi real, -- term forsummation to calculate shannon and hill numbers
    			si real, -- term forsummation to calculate simpson
    			qi real, -- term forsummation to calculate hill_inf
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
    
    		execute 'truncate '||tablename||resolname;
    
    		execute 'insert into '||tablename||resolname||'(cscode, n, s, shannon, simpson, 
    				es, hill_1, hill_2, hill_inf, geom) 
    			select t4.cscode, n, s, shannon, simpson, es, 
    				exp(shannon), 1/simpson, 1/max_p,
    				geom 
    			from t4 inner join t5 on t4.cscode=t5.cscode
    				inner join jcleary.b_cs'||resolname||' on t4.cscode=b_cs'||resolname||'.cscode;';
    
    	endtime:=clock_timestamp();
    	retvar:='do_calc finished in '||endtime-starttime;
    	return retvar;
    	end;
