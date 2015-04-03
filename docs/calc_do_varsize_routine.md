# do_varsize
database: [obis](../)  
schema: [calc](calc)  

    
    
    /* Calculate variable size grid depending on the number of observations in the grid cell
    evberghe 20101204
    */
    
    	declare
    		retvar varchar(255); -- return variable
    		ranks record;
    		sqlstring varchar(10000);
    		minn integer;
    		
    	begin
    		set search_path to calc, public;
    		--minn:=100;
    
    		drop table if exists res;
    		create table res (
    			id serial,
    			cscode varchar(16),
    			n integer
    		);
    		insert into res(cscode, n) select cscode, n from map10d where n<100;  
    		insert into res(cscode, n) select map5d.cscode as c5d, map5d.n as n5d
    			from map10d inner join map5d on substring(map5d.cscode from 1 for 4)=map10d.cscode
    			where map10d.n>=100 and map5d.n<100;
    		insert into res(cscode, n) select map1d.cscode as c1d, map1d.n as n1d
    			from map5d inner join map1d on substring(map1d.cscode from 1 for 6)=map5d.cscode
    			where map5d.n>=100 and map1d.n<100;
    		insert into res(cscode, n) select map30m.cscode as c1d, map30m.n as n1d
    			from map1d inner join map30m on substring(map30m.cscode from 1 for 8)=map1d.cscode
    			where map1d.n>=100 and map30m.n<100;
    		insert into res(cscode, n) select map6m.cscode, map30m.n
    			from map30m inner join map6m on substring(map6m.cscode from 1 for 10)=map30m.cscode
    			where map30m.n>=100 and map6m.n<100;
    		
    
    	retvar:='Return string: '||invar;
    	return retvar;
    	end;
