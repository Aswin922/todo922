drop table if exists people cascade;
drop table if exists task;

 create table people (
       id serial primary key,
       email text not null,
       password text not null       
);
  
create table task(
      
      id serial primary key,
      taskname text not null,
      duedate text not null,
      overdue varchar(1),
      taskrec integer references people(id)
       
 );
