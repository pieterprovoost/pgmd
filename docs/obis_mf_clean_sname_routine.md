# mf_clean_sname
database: [obis](../)  
schema: [obis](obis)  

    
    DECLARE
       matches varchar[];
       regexp varchar(100);
       old_sname varchar(200);
    BEGIN
    
    
       matched := false; -- set flag
    
       if sname = '' then
    	return;
       end if;
    
      -- NOTE THAT THE ORDER OF THE REPLACEMENTS BELOW IS IMPORTANT
    
       old_sname := cleaned_sname; -- store the name before cleaning
       
       cleaned_sname := replace(cleaned_sname, CHR(13), ' ');
       cleaned_sname := replace(cleaned_sname, CHR(10), ' ');
       
       cleaned_sname := trim((sname)); -- assign in case there are no matches
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^([A-Z])([a-z]+)([A-Z])([a-z]+)$', E'\\1\\2 \\3\\4', 'g')));
    
       cleaned_sname := lower(cleaned_sname); -- assign in case there are no matches
    
       -- REPLACE SOME OF THE LONGER BAD STRINGS FIRST
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' spp. - antarctic$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' encrusting$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^encrusting$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^encrusting ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^total ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' filamentous$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^filamentous$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^filamentous ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' algae$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^algae$', ''))); -- do not replace this with plantae...
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^algae ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^null$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^n. det.$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^n.d.$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' nd$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^nd$', '')));
    
       -- SOME SAHFOS CPR SURVEY SPECIALS !!! ---
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^fish eggs with oil globules$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^fish eggs without oil globules$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^grainy fried$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^grainy fried egg[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^nematocyst[s]?$', '')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'holothurian wheel ossicles', '')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'wagon wheels', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'hydroid fragments', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'wagon wheels', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'microniscus larvae of isopod', 'microniscus')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'oceanic copepods', 'copepoda')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'miscellaneous', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'ostracoda fragments', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'other eyecount copepods', 'copepoda')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'prorocentrum spp. (''exuviaella'' type)', 'prorocentrum')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'adult pacific', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'adult atlantic', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'stellate body (land plant hair)', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'stones and rocks', ' ')));
    
    
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, 'pseudo nitzschia groupe des .*', 'pseudo nitzschia')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^unid ', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^unident ', '')));
       
       cleaned_sname := (select trim(replace(cleaned_sname, 'individuals per mass', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'marine invertebrata (ns)', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'pico /nanoplankton heterotrophic eucaryotic', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'pico /nanoplankton phototrophic eucaryotic', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, 'tubular agglutinants', ' ')));
    
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' fish egg[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^fish egg[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^fish egg[s]? ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' resting spore[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^resting spore[s]?$', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' spore$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^spore$', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' soft shelled$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^foreign articles,garbage$', '')));
       
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^plastic[s]?$', '')));
    
       cleaned_sname := (select trim(replace(cleaned_sname, '(antarctic)', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '(atlantic)', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '(north atlantic)', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '(pacific)', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '(major)', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '(arctic)', ' ')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' p$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' b$', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' [a-z] ', ' ', 'g')));
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' v ', ' ', 'g')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' cf ', ' ', 'g')));
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' c ', ' ', 'g')));
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' d ', ' ', 'g')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' gr ', ' ', 'g')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' ex ', ' ', 'g')));
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' o ', ' ', 'g')));
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' m ', ' ', 'g')));
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' j ', ' ', 'g')));
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' p ', ' ', 'g')));
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' s ', ' ', 'g')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' blocks$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' [a-z]$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^[a-z]$', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' nh$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' egg[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^egg[s]?$', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^discontinued ', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^cf ', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^colonial ', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' colonial ', ' ')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' colonial$', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^solitary ', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' solitary ', ' ')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' solitary$', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^upright ', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' upright ', ' ')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' upright$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^colourless ', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '["]+|[.]+|[(]+|[)]+|[=]+|[,]+|[>]+|[<]+', ' '))); -- replaces all of the following dodgy characters with a space >> " . ( ) - = ,
    
       cleaned_sname := (select trim(replace(cleaned_sname, '~', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '?', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '#', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '-', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '_', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, ']', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '[', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '*', ' ')));
       cleaned_sname := (select trim(replace(cleaned_sname, '÷', ' ')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, E'\\)$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, E'\\,$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '[+]?$', '', 'g')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '[&]?$', '', 'g')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' wih eye[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' no eye[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' pacific unidentified$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' atlantic fin hel glac$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' reworked per volume', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' traverse$', '')));   -- traverse is a SAHFOS CPR Survey Counting Methodology
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' trav$', '')));   -- traverse is a SAHFOS CPR Survey Counting Methodology
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' eyecount$', '')));   -- eyecount is a SAHFOS CPR Survey Counting Methodology
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' female[s]?$', '')));      -- removes the suffixes 'female' and 'females' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' male[s]?$', '')));        -- removes the suffixes 'male' and 'males' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' agg$', '')));          -- removes the suffix 'agg' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' juv[s]?$', '')));          -- removes the suffix 'juv' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' s[p]+$', '')));        -- removes the suffix 'sp' or 'spp' etc at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' species$', '')));        -- removes the suffix 'sp' or 'spp' etc at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' indet$', '')));        -- removes the suffix 'indet' at the end of a line
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' total[s]?$', ''))); -- removes the suffix 'total' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^total[s]?$', ''))); -- word only
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^total[s]? ', ''))); -- start of line
          
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' unident[i]?fied$', ''))); -- removes the suffix 'unidentified' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^unident[i]?fied$', ''))); 
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^unident[i]?fied ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' sample[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^sample[s]?$', ''))); 
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^sample[s]?$ ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' environmental$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^environmental$', ''))); 
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^environmental ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' unknown$', ''))); -- removes the suffix 'unknown' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^unknown$', ''))); 
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^unknown ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' unclassified$', ''))); -- removes the suffix 'unknown' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^unclassified$', ''))); 
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^unclassified ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' parasit[e|ic]+$', ''))); -- removes parasitic or parasite at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^parasit[e|ic]+$', ''))); -- removes word
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^parasit[e|ic]+ ', ''))); -- removes at the start of a line
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, 'non current code', '')));
    	cleaned_sname := (select trim(regexp_replace(cleaned_sname, 'sp. ', '')));
    	cleaned_sname := (select trim(regexp_replace(cleaned_sname, 'soviet fishery data', '')));
    	cleaned_sname := (select trim(regexp_replace(cleaned_sname, 'undifferentiated', '')));
    	cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^order ', '')));
    	cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^suborder ', '')));
    	cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^class ', '')));
    	cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^phylum ', '')));
    	cleaned_sname := (select trim(regexp_replace(cleaned_sname, 'cleveland list', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^acartia clausi or tonsa$', 'acartia'))); -- replace with the genera only as we do not know the species
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' group$', '')));        -- removes the suffix 'group' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' dam$', '')));          -- removes the suffix 'dam' at the end of a line
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' var ', ' ', 'g')));    -- replace all occurrences of the word 'var' with a space
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' sp[p]* ', ' ', 'g')));    -- replace all occurrences of the word 'sp' or 'spp' with a space
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' juv ', ' ', 'g')));    -- replace all occurrences of the word 'juv' with a space
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' average$', '')));      -- removes the suffix 'average'
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' post$', '')));         -- removes the suffixes 'post' e.g. in the case of 'post larva'
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' larva[e]?$', '')));    -- removes the suffixes 'larva and larvae'
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' trochophora$', '')));   -- removes the suffix
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' mass$', '')));         -- removes the suffix 'mass'
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' remains$', '')));         -- removes the suffix 'mass'
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^black$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' spine[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^black spine$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' cyst[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' cyst[s]? ', ' ')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' encysted$', ' ')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^all$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^all ', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' all$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^small ', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' small ', ' ')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' small$', '')));
    
          cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^other[s]? ', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' other[s]? ', ' ')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' other[s]?$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^other[s]?$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^damaged$', '')));
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' duck$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' genera$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^genera$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^genera ', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^pennate$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^roundness$', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^brown$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' mm$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' damaged$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' nauplii$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' megalopa$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' complex$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' type$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' zoea$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' var$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' med$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' incertae sedis$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' temporary$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' stn$', ''))); -- collecting station?
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' stage$', ''))); -- collecting station?
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' sponge$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^sponge[s]?$', 'porifera')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^bivalve[s]?$', 'bivalvia"')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^barnacle[s]?$', 'cirripedia')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^bryozoan[s]?$', 'bryozoa')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^nemertean$', 'nemertea')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^flatworm[s]?$', 'platyhelminthes')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^pteropod[s]?$', 'pteropoda')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^rotifer[s]?$', 'rotifera')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^centric diatom[s]?$', 'coscinodiscophyceae')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^copepod[s]?$', 'copepoda')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^gastropod[s]?$', 'gastropoda')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^nematod$', 'nematoda')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^tintinnid[en]*$', 'tintinnida')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^oligochaete[s]?$', 'oligochaeta')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^polyclad ', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^polyclad$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' polyclad$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^turbellarian$', 'turbellaria')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^tanaid[s]?$', 'tanaidacea')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^ophiuroida$', 'ophiuroidia')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^plathelminthes$', 'platyhelminthes')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^ciliate[s]?$', 'ciliophora')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^coccolithophorid[s]?$', 'coccolithophyceae')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^fish and invertebrate[s]?$', 'animalia')));
       
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' shell[s]?$', '')));  -- non living organism
       --cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' tissue$', '')));  -- non living organism
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' c1$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' c2$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' c3$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' c4$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' c5$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' c6$', '')));
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' [i]*$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' iv$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' v$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' vi$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' unstaged$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' civ$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' cvi$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' m$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' f$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' g$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' c$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' e$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' small$', '')));
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, ' large$', '')));
       
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '[0-9]', '', 'g')));     -- removes any numbers
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '^[a-z]+(?=an)$', 'a'))); -- remove "an" and the end of a single word with 'a' e.g. bryozoan to bryozoa
    
       -- did this pass through the function result in a change to the name?
       -- if it did we need to notify the calling function so that it can try to parse the name again
    
       cleaned_sname := (select trim(regexp_replace(cleaned_sname, '[ ]+', ' ', 'g')));
    
       -- split the word into an array and then compare words 2 and 3 - if they are the same then return only the first 2 words!!!
       -- this might need refinement with some edge cases such as when there are more than 3 words in the clean name
       cleaned_sname := (select case when ((select(regexp_split_to_array(cleaned_sname, E'\\s+')))[2] = (select(regexp_split_to_array(cleaned_sname, E'\\s+')))[3]) 
                                then (select(regexp_split_to_array(cleaned_sname, E'\\s+')))[1] || ' ' || (select(regexp_split_to_array(cleaned_sname, E'\\s+')))[2]
                                else cleaned_sname
                                end);
       
       if not (cleaned_sname = old_sname) then
    	matched := true;
       end if;
       
       return;
       
    END;
