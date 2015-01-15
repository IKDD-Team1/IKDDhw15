# IKDDhw15
Compare the insert time and query time between MongoDB with PostgreSQL 

Download the data of GeoLife GPS Trajectories.

+ A folder represent a user (ex.000,001).
+ A file in user folder represent a day of user trajectories

## Requirement
+ Output the insert time with PostgreSQL and MongoDB
+ Output the query time with PostgreSQL and MongoDB (Query 003 user 2008-11-19 trajectories and sort by time)
+ Remember to use multi-thread

## Dateset
[GeoLife GPS Trajectories] (http://research.microsoft.com/en-us/downloads/b16d359d-d164-469e-9fd4-daa38f2b2e13/)

## Database Version
+ postgres: v9.4
+ mongodb: v2.6.6

## Insert

**Insert Time**
+ postgres - Time: 98.2643408775 s
+ mongo - Time: 407.198955059 s

## Query

**Command**

```sql
    SELECT * from test_table WHERE user_id='003' AND date='2008-11-19' ORDER BY time DESC;
```
```javascript
    db.test_collection.find({user:"003", date: "2008-11-19"}).sort({time:1})
```
**Query Time**

+ postgres - Time: 185.560 ms
+ mongo - Time: 672ms
