# get_csquare
database: [obis](../)  
schema: [geo](geo)  

    
    
    -- input: latitude longitude pair; resolution
    -- resolution of csquare will be better (smaller) than parameter; at least 10d; 
    -- returns null in case no valid lat lon was given
    
    	declare
    		s varchar(255); -- return variable
    		lar double precision; -- latitude remainder
    		lor double precision; -- longitude remainder
    		curres real; -- attained resolution in loop
    	begin
    		if lat<-90 or lat>90 or lat is null
    			or lon<-180 or lon>180 or lon is null
    		then -- not a valid lat/lon pair
    			return null;
    		else
    			begin
    -- calculate first character
    			if lat>=0 then if lon>=0 then s:='1'; else s:='7'; end if;
    			else if lon>=0 then s:='3'; else s:='5'; end if;
    			end if;
    -- calculate characters 2 to 4
    			lar:=abs(lat); -- rest of calculations mirrored over Equator
    			if lar=90 then -- special case for lat=90
    				begin
    				s:=s||'8';
    				lar:=9.9999999999999;
    				end;
    			else -- calculate position 2
    				begin
    				s:=s||trunc(lar/10);
    				lar:=lar-10*trunc(lar/10);
    				end;
    			end if;
    			lor:=abs(lon); -- rest of calculations mirrored over Greenwich
    			if lor=180 then -- special case for longitude=180
    				begin
    				s:=s||'17';
    				lor:=9.9999999999999;
    				end;
    			else -- calculate position 3 and 4
    				begin
    				s:=s||substring('0'||trunc(lor/10) from '..$'); -- make sure there is a leading zero for values less than 10
    				lor:=lor-10*trunc(lor/10);
    				end;
    			end if;
    			if resolution>=10 
    			then return s;
    			else -- more characters needed
    				begin
    				curres:=5;
    				loop
    					s:=s||':'||case when trunc(lar)<5 then 
    						case when trunc(lor)<5 then '1' else '2' end
    						else case when trunc(lor)<5 then '3' else '4' end end;
    					if resolution>=curres 
    					then return s;
    					else
    						begin
    						curres:=curres/5;
    						s:=s||trunc(lar)||trunc(lor);
    						lar:=10*(lar-trunc(lar));
    						lor:=10*(lor-trunc(lor));
    						if resolution>=curres 
    						then return s;
    						else curres:=curres/2;
    						end if;
    						end;
    					end if;
    				end loop;
    				end;
    			end if;
    			end;
    		end if;
    	end;
