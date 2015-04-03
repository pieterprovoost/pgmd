# get_wkt_from_csquare
database: [obis](../)  
schema: [geo](geo)  

    
    
    -- input: csquare string
    -- returns null in case csquare string was not valid
    
    	declare
    		c varchar(255); -- csquare string 
    		s varchar(255); -- return variable
    		lat real; -- latitude of corner point closest to 0,0
    		lon real; -- longitude of corner point closest to 0,0
    		las real; -- step of latitude
    		los real; -- step of longitude
    	begin
    		c:=i;
    -- calculate first character
    		if substring(c from 1 for 1)='1' then begin las:=10;los:=10; end; end if; 
    		if substring(c from 1 for 1)='3' then begin las:=-10;los:=10; end; end if; 
    		if substring(c from 1 for 1)='5' then begin las:=-10;los:=-10; end; end if; 
    		if substring(c from 1 for 1)='7' then begin las:=10;los:=-10; end; end if; 
    -- calculate characters 2 to 4
    		lat:=las*substring(c from 2 for 1)::real; -- rest of calculations mirrored over Equator
    		lon:=los*substring(c from 3 for 2)::real; -- rest of calculations mirrored over Greenwich
    -- more characters to parse
    		while char_length(c)>4 loop
    			c:=regexp_replace(c, '^.*?:',''); las:=las/10;los:=los/10;
    			if char_length(c)=1
    			then
    				begin
    				las:=las*5;los:=los*5;
    				if c='2' or c='4' then lon:=lon+los; end if; 
    				if c='3' or c='4' then lat:=lat+las; end if; 
    				end;
    			else
    				begin
    				lat:=lat+las*substring(c from 2 for 1)::real;
    				lon:=lon+los*substring(c from 3 for 1)::real;
    				end;
    			end if;
    		end loop;
    		s:='POLYGON(('||lon||' '||lat||', ';
    		if las*los>0 -- make sure orientation of polygon is always clockwise
    		then
    			s:=s||lon||' '||lat+las||', '||lon+los||' '||lat+las||', '
    				||lon+los||' '||lat||', '||lon||' '||lat;
    		else
    			s:=s||lon+los||' '||lat||', '||lon+los||' '||lat+las||', '
    				||lon||' '||lat+las||', '||lon||' '||lat;
    		end if;
    		s:=s||'))';
    	return s;
    	end;
