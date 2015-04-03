# download_requests
database: [obis](../)  
schema: [portal](portal)  

|Column|Type|Constraint|
|:---|:---|:---|
|request_id|character varying|download_requests_pkey |
|user_name|character varying||
|ip_address|character varying||
|email|character varying||
|sql|text||
|date_requested|timestamp without time zone||
|num_records|bigint||
|status|character varying||
|date_updated|timestamp without time zone||
|date_downloaded|timestamp without time zone||
|oid|integer||
|download_url|character varying||
|format|character varying||
|data_type|character varying||
|params_json|text||
