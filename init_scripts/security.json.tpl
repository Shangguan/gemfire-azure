 {
   "roles": [
     {
       "name": "admin",
       "operationsAllowed": [
         "CLUSTER:READ",
         "CLUSTER:WRITE",
         "CLUSTER:MANAGE",
         "DATA:READ",
         "DATA:WRITE",
         "DATA:MANAGE"
       ]
     },
     {
       "name": "app",
       "operationsAllowed": [
         "DATA:READ",
	        "DATA:WRITE",
          "DATA:MANAGE"
       ]
     }
   ],
   "users": [
     {
       "name": "gfadmin",
       "password": "{{ GFAdminPassword }}",
       "roles": ["admin"]
     }
   ]
 }
