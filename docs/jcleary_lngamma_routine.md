# lngamma
database: [obis](../)  
schema: [jcleary](jcleary)  

    
    declare
        r double precision;
        c0 double precision;
        c1 double precision;
        c2 double precision;
        c3 double precision;
        c4 double precision;
        c5 double precision;
        y double precision;
        tmp double precision;
        ser double precision;
    begin
        c0 := 76.1800917294715;
        c1 := -86.5053203294168;
        c2 := 24.0140982408309;
        c3 := -1.23173957245015;
        c4 := 1.20865097386618E-03;
        c5 := -5.395239384953E-06;
    
        if x<=0
        then r:=null;
        else
            if x=2
            then r:=0;
            else
                y := x;
                tmp := x + 5.5 - (x + 0.5) * Ln(x + 5.5);
                ser := 1.00000000019001;
                y:=y+1; ser:=ser+c0/y;
                y:=y+1; ser:=ser+c1/y;
                y:=y+1; ser:=ser+c2/y;
                y:=y+1; ser:=ser+c3/y;
                y:=y+1; ser:=ser+c4/y;
                y:=y+1; ser:=ser+c5/y;
                r:=Ln(2.506628274631*ser/x)-tmp;
            end if;
        end if;
        return r;
    end;
    
