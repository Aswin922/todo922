DROP TABLE IF EXISTS user cascade;
DROP TABLE IF EXISTS tasks;


create table user(
       id serial primary key,
       username text unique not null,
       password text not null       
);
  
create table tasks(      
      id serial primary key,
      task_name text not null,
      due_date date not null,
      overdue varchar(1),
      task_rec integer references user(id)      
 );
