# create_support_tables
database: [obis](../)  
schema: [portal](portal)  

    
    declare
    	table_name character varying;
    	msg character varying;
    	status_b boolean;
    	num_found integer;
    begin
    	raise notice 'Create support tables: start of the function'; 
    	
    	status_b := true;
    	
    	table_name := 'zone layers in geo';
    	raise notice 'Checking zone layers in geo'; 
    	num_found := (SELECT count(*)::int FROM pg_class WHERE relname in ('eezs', 'iho', 'lme', 'meow', 'mwhs'));
        if num_found <  5 then
    		status_b := false;
    	    msg := table_name || ' not found (only ' || num_found || ' found)';
        end if;
    
    	if not status_b then
    		return msg;
    	end if;
    	
    		
    	set search_path to portal;
    	
    	raise notice 'Start creating download_requests table...'; 
    	
    	-- copied from create_download_requests.sql
    	DROP TABLE IF EXISTS download_requests CASCADE;
    	
    	CREATE TABLE download_requests
    	(
    	  request_id character varying(255) NOT NULL,
    	  user_name character varying(255),
    	  ip_address character varying(20),
    	  email character varying(255),
    	  sql text,
    	  date_requested timestamp without time zone DEFAULT ('now'::text)::timestamp(0) without time zone,
    	  num_records bigint,
    	  status character varying(255),
    	  date_updated timestamp without time zone,
    	  date_downloaded timestamp without time zone,
    	  oid serial NOT NULL,
    	  download_url character varying,
    	  format character varying DEFAULT 20,
    	  data_type character varying(20),
    	  params_json text,
    	  CONSTRAINT download_requests_pkey PRIMARY KEY (request_id)
    	)
    	WITH (
    	  OIDS=FALSE
    	);
    	
    	
    	raise notice 'Start creating create_feedback...'; 
    	-- copied from create_feedback.sql
    	DROP TABLE IF EXISTS feedback CASCADE;
    	
    	CREATE TABLE feedback
    	(
    	  id serial NOT NULL,
    	  sid character varying(255),		-- sid is unique per browser session
    	  full_name character varying(255),
    	  affiliation character varying(255),
    	  email character varying(255),
    	  feedback_on character varying(20),
    	  feedback text,
    	  dr_id integer,
    	  query text,
    	  status character varying(20),
    	  date_requested date, -- date the comment was entered by the web user
    	  date_responded date,
    	  releasedflag boolean NOT NULL DEFAULT false, -- Can the comment be made visibleon the web site? By default not - has to be turned on by data manager at iOBIS
    	  CONSTRAINT pk_feedback PRIMARY KEY (id)
    	)
    	WITH (
    	  OIDS=FALSE
    	);
    
    
    	raise notice 'Start importing zone layers...'; 
    	-- copied from import_zone_layers.sql
    	DROP TABLE IF EXISTS eezs CASCADE;
    	CREATE TABLE eezs AS
    	SELECT
    	*,
    	public.box2d(geom) as bbox,
    	public.st_xmin(public.box2d(geom))::text || ',' || public.st_ymin(public.box2d(geom))::text || ',' || public.st_xmax(public.box2d(geom))::text || ',' || public.st_ymax(public.box2d(geom))::text as bbox_str
    	FROM geo.eezlrs;
    	
    	CREATE INDEX idx_eezs_geom
    	  ON eezs
    	  USING gist
    	  (geom);
    	
    	
    	DROP TABLE IF EXISTS iho CASCADE;
    	CREATE TABLE iho AS
    	SELECT
    	*,
    	public.box2d(geom) as bbox,
    	public.st_xmin(public.box2d(geom))::text || ',' || public.st_ymin(public.box2d(geom))::text || ',' || public.st_xmax(public.box2d(geom))::text || ',' || public.st_ymax(public.box2d(geom))::text as bbox_str
    	FROM geo.iho;
    	
    	CREATE INDEX idx_iho_geom
    	  ON iho
    	  USING gist
    	  (geom);
    	
    	
    	DROP TABLE IF EXISTS lme CASCADE;  
    	CREATE TABLE lme AS
    	SELECT
    	*,
    	public.box2d(geom) as bbox,
    	public.st_xmin(public.box2d(geom))::text || ',' || public.st_ymin(public.box2d(geom))::text || ',' || public.st_xmax(public.box2d(geom))::text || ',' || public.st_ymax(public.box2d(geom))::text as bbox_str
    	FROM geo.lme;
    	
    	CREATE INDEX idx_lme_geom
    	  ON lme
    	  USING gist
    	  (geom);
    	
    	
    	DROP TABLE IF EXISTS meow CASCADE;
    	CREATE TABLE meow AS
    	SELECT
    	*,
    	public.box2d(geom) as bbox,
    	public.st_xmin(public.box2d(geom))::text || ',' || public.st_ymin(public.box2d(geom))::text || ',' || public.st_xmax(public.box2d(geom))::text || ',' || public.st_ymax(public.box2d(geom))::text as bbox_str
    	FROM geo.meow;
    	
    	CREATE INDEX idx_meow_geom
    	  ON meow
    	  USING gist
    	  (geom);
    
    	DROP TABLE IF EXISTS mwhs CASCADE;  
    	CREATE TABLE mwhs AS
    	SELECT
    	ogc_fid as id, refid, site_name, country, refid2, mrgi, year, wkb_geometry as geom,
    	public.box2d(wkb_geometry) as bbox,
    	public.st_xmin(public.box2d(wkb_geometry))::text || ',' || public.st_ymin(public.box2d(wkb_geometry))::text || ',' || public.st_xmax(public.box2d(wkb_geometry))::text || ',' || public.st_ymax(public.box2d(wkb_geometry))::text as bbox_str
    	FROM geo.mwhs;
    	
    	
    	msg := 'Success!';
    	
    	raise notice 'End of the function'; 
    	return msg;
    		
    end;
