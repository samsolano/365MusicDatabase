# API Specification for Music Database

## 1. User Streaming

The API calls are made in this squence when 
1. Get Streams
2. Get Top 3 Streamed
3. 
4.
5.
6.
7.
8.

1) Get Streams -
Gets total number of streams logged
Response
[
    {
        "streamNum": "integer"
    }
]

2) Streams by Artist
    Gets streams specific to an artist that the user asks for
Request
[
    {
        "artistName": "string"
    }
]
Response
[
    {
        "artistName": "string",
        "streamNum": "integer"
    }
]


## 3. CARLOSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

The API calls are made in this sequence when the bottler comes:
1. `Get Bottle Plan`
2. `Deliver Bottles`

### 2.1. Get Bottle Plan - `/bottler/plan` (POST)

Gets the plan for bottling potions.

**Response**:

```json
[
    {
        "potion_type": [r, g, b, d],
        "quantity": "integer"
    }
]
```

### 2.2. Deliver Bottles - `/bottler/deliver/{order_id}` (POST)

Posts delivery of potions. order_id is a unique value representing
a single delivery. 

**Request**:

```json
[
  {
    "potion_type": [r, g, b, d],
    "quantity": "integer"
  }
]
```

## 4. CARLOSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

The API calls are made in this sequence when the bottler comes:
1. `Get Bottle Plan`
2. `Deliver Bottles`

### 2.1. Get Bottle Plan - `/bottler/plan` (POST)

Gets the plan for bottling potions.

**Response**:

```json
[
    {
        "potion_type": [r, g, b, d],
        "quantity": "integer"
    }
]
```

### 2.2. Deliver Bottles - `/bottler/deliver/{order_id}` (POST)

Posts delivery of potions. order_id is a unique value representing
a single delivery. 

**Request**:

```json
[
  {
    "potion_type": [r, g, b, d],
    "quantity": "integer"
  }
]
```

5)

6)

7)

8)