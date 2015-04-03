# feedback
database: [obis](../)  
schema: [portal](portal)  

|Column|Type|Constraint|
|:---|:---|:---|
|id|integer|pk_feedback |
|sid|character varying||
|full_name|character varying||
|affiliation|character varying||
|email|character varying||
|feedback_on|character varying||
|feedback|text||
|dr_id|integer||
|query|text||
|status|character varying||
|date_requested|date||
|date_responded|date||
|releasedflag|boolean||
