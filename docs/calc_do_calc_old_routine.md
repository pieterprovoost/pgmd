# do_calc_old
database: [obis](../)  
schema: [calc](calc)  

    
    
    /* Calculate indices
    evberghe 2010-06-01
    turned into function 2010-07-03
    */
    
    	declare
    		retvar varchar(255); -- return variable
    		ranks record;
    		cellsizename record;
    		sqlstring varchar(10000);
    		
    	begin
    		set search_path to calc, public;
    
    		raise notice 'create temp tables';
    		drop table if exists nis cascade;
    		create table nis as 
    			select cs6m_valids.valid_id, cscode, nincl as ni 
    			from summaries.cs6m_valids inner join obis.tnames on cs6m_valids.valid_id=tnames.id
    			where coalesce(tnames.display,'1')='1' and rank_id=220; -- same set of indices can be calculated on other ranks
    
    		drop table if exists ns cascade;
    		create table ns as select cscode, sum(ni) as n from nis group by cscode;
    
    		raise notice 'calculations for 6x6m';
    		drop table if exists t1 cascade;
    		create table t1 as select * from nis;
    		CREATE INDEX ix_t1_cscode ON t1 USING btree (cscode);
    		CREATE INDEX ix_t1_valid_id ON t1 USING btree (valid_id);
    
    		drop table if exists t2 cascade;
    		create table t2 as select * from ns;
    		CREATE INDEX ix_t2_cscode ON t2 USING btree (cscode);
    
    		drop table if exists t3 cascade;
    		create table t3 as select valid_id, t1.cscode, n,
    			-(1.0*ni/n*ln(1.0*ni/n)) as hi,
    			(1.0*ni/n)^2 as si,
    			1.0*ni/n as qi,
    			case 
    				when n-ni>=50 then 1-exp(lngamma(n-ni+1)+lngamma(n-50+1)-lngamma(n-ni-50+1)-lngamma(n+1))
    				when n>=50 then 1
    				else null
    			end as esi
    		from t1 inner join t2 on t1.cscode=t2.cscode;
    		CREATE INDEX ix_t3_cscode ON t3 USING btree (cscode);
    
    		drop table if exists t4 cascade;
    		create table t4 as select cscode, n, sum(hi) as shannon, sum(si) as simpson, 
    			max(qi) as max_p, sum(esi) as es 
    			from t3 group by cscode, n;
    		CREATE INDEX ix_t4_cscode ON t4 USING btree (cscode);
    
    		drop table if exists t5 cascade;
    		create table t5 as select cscode, count(1) as s from t1 group by cscode;
    		CREATE INDEX ix_t5_cscode ON t5 USING btree (cscode);
    
    		drop table if exists map6m cascade;
    		create table map6m  as select t4.cscode, n, s, shannon, simpson, es, 
    			exp(shannon) as hill_1, 1/simpson as hill_2, 1/max_p as hill_inf
    			from t4 inner join t5 on t4.cscode=t5.cscode;
    
    		truncate table t1;
    		truncate table t2;
    		truncate table t3;
    		truncate table t4;
    		truncate table t5;
    
    		raise notice 'calculations for 30x30m';
    		insert into t1 select valid_id, substring(cscode from 1 for 10) as cscode, sum(ni) as ni
    			from nis
    			group by valid_id, substring(cscode from 1 for 10);
    		insert into t2 select substring(cscode from 1 for 10) as cscode, sum(n) as n
    			from ns
    			group by substring(cscode from 1 for 10);
    		insert into t3 select valid_id, t1.cscode, n,
    			-(1.0*ni/n*ln(1.0*ni/n)) as hi,
    			(1.0*ni/n)^2 as si,
    			1.0*ni/n as qi,
    			case 
    				when n-ni>=50 then 1-exp(lngamma(n-ni+1)+lngamma(n-50+1)-lngamma(n-ni-50+1)-lngamma(n+1))
    				when n>=50 then 1
    				else null
    			end as esi
    		from t1 inner join t2 on t1.cscode=t2.cscode;
    		insert into t4 select cscode, n, sum(hi), sum(si), max(qi), sum(esi) 
    			from t3 
    			group by cscode, n;
    		insert into t5 select cscode, count(1) as s
    			from t1 
    			group by cscode;
    
    		drop table if exists map30m cascade;
    		create table map30m as select t4.cscode, n, s, shannon, simpson, es, 
    			exp(shannon) as hill_1, 1/simpson as hill_2, 1/max_p as hill_inf
    			from t4 inner join t5 on t4.cscode=t5.cscode;
    
    		drop table nis; alter table t1 rename to nis;
    		drop table ns; alter table t2 rename to ns;
    		truncate table t3;
    		truncate table t4;
    		truncate table t5;
    
    
    		raise notice 'calculations for 1x1d';
    		create table t1 as select valid_id, substring(cscode from 1 for 8) as cscode, sum(ni) as ni
    			from nis
    			group by valid_id, substring(cscode from 1 for 8);
    		create table t2 as select substring(cscode from 1 for 8) as cscode, sum(n) as n
    			from ns
    			group by substring(cscode from 1 for 8);
    		insert into t3 select valid_id, t1.cscode, n,
    			-(1.0*ni/n*ln(1.0*ni/n)) as hi,
    			(1.0*ni/n)^2 as si,
    			1.0*ni/n as qi,
    			case 
    				when n-ni>=50 then 1-exp(lngamma(n-ni+1)+lngamma(n-50+1)-lngamma(n-ni-50+1)-lngamma(n+1))
    				when n>=50 then 1
    				else null
    			end as esi
    		from t1 inner join t2 on t1.cscode=t2.cscode;
    		insert into t4 select cscode, n, sum(hi), sum(si), max(qi), sum(esi) 
    			from t3 
    			group by cscode, n;
    		insert into t5 select cscode, count(1) as s
    			from t1 
    			group by cscode;
    
    		drop table if exists map1d cascade;
    		create table map1d as select t4.cscode, n, s, shannon, simpson, es, 
    			exp(shannon) as hill_1, 1/simpson as hill_2, 1/max_p as hill_inf
    			from t4 inner join t5 on t4.cscode=t5.cscode;
    
    		drop table nis; alter table t1 rename to nis;
    		drop table ns; alter table t2 rename to ns;
    		truncate table t3;
    		truncate table t4;
    		truncate table t5;
    
    		raise notice 'calculations for 5x5d';
    		create table t1 as select valid_id, substring(cscode from 1 for 6) as cscode, sum(ni) as ni
    			from nis
    			group by valid_id, substring(cscode from 1 for 6);
    		create table t2 as select substring(cscode from 1 for 6) as cscode, sum(n) as n
    			from ns
    			group by substring(cscode from 1 for 6);
    		insert into t3 select valid_id, t1.cscode, n,
    			-(1.0*ni/n*ln(1.0*ni/n)) as hi,
    			(1.0*ni/n)^2 as si,
    			1.0*ni/n as qi,
    			case 
    				when n-ni>=50 then 1-exp(lngamma(n-ni+1)+lngamma(n-50+1)-lngamma(n-ni-50+1)-lngamma(n+1))
    				when n>=50 then 1
    				else null
    			end as esi
    		from t1 inner join t2 on t1.cscode=t2.cscode;
    		insert into t4 select cscode, n, sum(hi), sum(si), max(qi), sum(esi) 
    			from t3 
    			group by cscode, n;
    		insert into t5 select cscode, count(1) as s
    			from t1 
    			group by cscode;
    
    		drop table if exists map5d cascade;
    		create table map5d as select t4.cscode, n, s, shannon, simpson, es, 
    			exp(shannon) as hill_1, 1/simpson as hill_2, 1/max_p as hill_inf
    			from t4 inner join t5 on t4.cscode=t5.cscode;
    
    		drop table nis; alter table t1 rename to nis;
    		drop table ns; alter table t2 rename to ns;
    		truncate table t3;
    		truncate table t4;
    		truncate table t5;
    
    		raise notice 'calculations for 10x10d';
    		create table t1 as select valid_id, substring(cscode from 1 for 4) as cscode, sum(ni) as ni
    			from nis
    			group by valid_id, substring(cscode from 1 for 4);
    		create table t2 as select substring(cscode from 1 for 4) as cscode, sum(n) as n
    			from ns
    			group by substring(cscode from 1 for 4);
    		insert into t3 select valid_id, t1.cscode, n,
    			-(1.0*ni/n*ln(1.0*ni/n)) as hi,
    			(1.0*ni/n)^2 as si,
    			1.0*ni/n as qi,
    			case 
    				when n-ni>=50 then 1-exp(lngamma(n-ni+1)+lngamma(n-50+1)-lngamma(n-ni-50+1)-lngamma(n+1))
    				when n>=50 then 1
    				else null
    			end as esi
    		from t1 inner join t2 on t1.cscode=t2.cscode;
    		insert into t4 select cscode, n, sum(hi), sum(si), max(qi), sum(esi) 
    			from t3 
    			group by cscode, n;
    		insert into t5 select cscode, count(1) as s
    			from t1 
    			group by cscode;
    
    		drop table if exists map10d cascade;
    		create table map10d as select t4.cscode, n, s, shannon, simpson, es, 
    			exp(shannon) as hill_1, 1/simpson as hill_2, 1/max_p as hill_inf
    			from t4 inner join t5 on t4.cscode=t5.cscode;
    
    		drop table nis; alter table t1 rename to nis;
    		drop table ns; alter table t2 rename to ns;
    		drop table t3;
    		drop table t4;
    		drop table t5;
    
    		raise notice 'calculations for globe';
    		create table t1 as select valid_id, sum(ni) as ni from nis group by valid_id;
    		create table t2 as select sum(n) as n from ns; -- t2 has a single row
    		create table t3 as select valid_id, n,
    			-(1.0*ni/n*ln(1.0*ni/n)) as hi,
    			(1.0*ni/n)^2 as si,
    			1.0*ni/n as qi,
    			case 
    				when n-ni>=50 then 1-exp(lngamma(n-ni+1)+lngamma(n-50+1)-lngamma(n-ni-50+1)-lngamma(n+1))
    				when n>=50 then 1
    				else null
    			end as esi
    		from t1, t2;
    		create table t4 as select n, sum(hi) as shannon, sum(si) as simpson, max(qi) as max_p, sum(esi) as es from t3 group by n;
    		create table t5 as select count(1) as s from t1; -- t5 has a single row
    
    		drop table if exists mapglobal cascade;
    		create table mapglobal as select n, s, shannon, simpson, es, 
    			exp(shannon) as hill_1, 1/simpson as hill_2, 1/max_p as hill_inf
    			from t4, t5;
    
    		drop table nis; drop table t1;
    		drop table ns; drop table t2;
    		drop table t3;
    		drop table t4;
    		drop table t5;
    
    		ALTER TABLE calc.map10d ALTER n TYPE integer;
    		ALTER TABLE calc.map10d ALTER s TYPE integer;
    		ALTER TABLE calc.map5d ALTER n TYPE integer;
    		ALTER TABLE calc.map5d ALTER s TYPE integer;
    		ALTER TABLE calc.map1d ALTER n TYPE integer;
    		ALTER TABLE calc.map1d ALTER s TYPE integer;
    		ALTER TABLE calc.map30m ALTER n TYPE integer;
    		ALTER TABLE calc.map30m ALTER s TYPE integer;
    		ALTER TABLE calc.map6m ALTER n TYPE integer;
    		ALTER TABLE calc.map6m ALTER s TYPE integer;
    		ALTER TABLE calc.mapglobal ALTER n TYPE integer;
    		ALTER TABLE calc.mapglobal ALTER s TYPE integer;
    
    	retvar:='Return string: '||invar;
    	return retvar;
    	end;
