create table product (
       id serial primary key,
       product varchar(128),
       retailer varchar(128),
       acquired timestamptz,
       url text,
       price numeric,
       weight numeric --in kilos
       );