Possible Concurrency Control Issues:


## Case 1: Dirty Read

**Scenario:**
Two users are interacting with the database. User A is uploading a new song and User B is searching for songs by the same artist at the same time.

### Sequence Diagram
```
User A                         Database                        User B
   |                               |                              |
   |----- Start Transaction A ---->|                              |
   |                               |                              |
   |--- Insert new song data ----->|                              |
   |                               |                              |
   |                               |<---- Start Transaction B ----|
   |                               |                              |
   |                               |---- Search songs by artist -->|
   |                               |                              |
   |                               |<---- Return results ---------|
   |                               |                              |
   |----- Commit Transaction A --->|                              |
   |                               |                              |
```

### Issue
User B may see the new song added by User A before User A commits the transaction. If User A later rolls back the transaction, User B would have read data that was never actually committed.

### Solution
Use **READ COMMITTED** isolation level to prevent dirty reads. This ensures that any data read by User B is committed by User A.

<br/> <br/>

## Case 2: Non-Repeatable Read

**Scenario:**
User A is viewing the details of an album while User B updates the album's details.

### Sequence Diagram
```
User A                         Database                        User B
   |                               |                              |
   |----- Start Transaction A ---->|                              |
   |                               |                              |
   |---- Read album details -----> |                              |
   |                               |                              |
   |                               |<----- Start Transaction B ---|
   |                               |                              |
   |                               |<----- Update album details --|
   |                               |                              |
   |----- Read album details ----->|                              |
   |                               |                              |
   |----- Detect change ---------->|                              |
   |                               |                              |
   |----- Commit Transaction A --->|                              |
   |                               |                              |
```

### Issue
User A might see different data if they read the album details again within the same transaction due to User B’s update.

### Solution
Use **REPEATABLE READ** isolation level to prevent non-repeatable reads. This ensures that User A will see the same album details throughout their transaction.


<br/> <br/>
## Case 3: Phantom Read

**Scenario:**
User A is checking the list of trending songs while User B adds a new song that becomes a trending song during the process.

### Sequence Diagram
```
User A                         Database                        User B
   |                               |                              |
   |----- Start Transaction A ---->|                              |
   |                               |                              |
   |--- Get trending songs list -->|                              |
   |                               |                              |
   |                               |<----- Start Transaction B ---|
   |                               |                              |
   |                               |<----- Add new song ----------|
   |                               |                              |
   |                               |<----- Update trending list --|
   |                               |                              |
   |--- Get trending songs list -->|                              |
   |                               |                              |
   |----- Detect new song -------->|                              |
   |                               |                              |
   |----- Commit Transaction A --->|                              |
   |                               |                              |
```

### Issue
User A might see different sets of trending songs when they query the trending list again within the same transaction due to the new song added by User B.

### Solution
Use **SERIALIZABLE** isolation level to prevent phantom reads. This ensures that User A will see a consistent set of trending songs throughout their transaction.

