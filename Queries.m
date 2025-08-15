let
    PGServer = "your-pg-hostname",
    PGDatabase = "your-db-name",
    PGUser = "your-user",
    PGPassword = "your-password",
    Txn = PostgreSQL.Database(PGServer, [Database=PGDatabase, Query="select * from txn"]),
    Budget = PostgreSQL.Database(PGServer, [Database=PGDatabase, Query="select * from budget"]),
    Merchant = PostgreSQL.Database(PGServer, [Database=PGDatabase, Query="select * from merchant"])
in
    [Txn=Txn, Budget=Budget, Merchant=Merchant]
