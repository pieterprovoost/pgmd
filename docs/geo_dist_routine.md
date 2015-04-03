# dist
database: [obis](../)  
schema: [geo](geo)  

    
    	declare 
    		d float;
    		x1 float;
    		x2 float;
    		y1 float;
    		y2 float;
    		pi float = 2*acos(0);
    	begin
    		y1:=lat1*pi/180;
    		x1:=lon1*pi/180;
    		y2:=lat2*pi/180;
    		x2:=lon2*pi/180;
    		d:=cos(y1)*cos(x1)*cos(y2)*cos(x2)
    			+cos(y1)*sin(x1)*cos(y2)*sin(x2)
    			+sin(y1)*sin(y2);
    		return 6370986*acos(d);
    	end;
    
