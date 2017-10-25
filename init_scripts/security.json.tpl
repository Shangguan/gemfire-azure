{
    "roles": [
      {
        "name": "admin",
        "operationsAllowed": [
          "CLUSTER:MANAGE",
          "CLUSTER:WRITE",
          "CLUSTER:READ",
          "DATA:MANAGE",
          "DATA:WRITE",
          "DATA:READ"
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
