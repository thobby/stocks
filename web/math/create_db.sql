
drop table exchanges;
create table exchanges (id integer primary key, name text, unique (name));

drop table tickers;
create table tickers (id integer primary key, exchange integer, name text, unique (exchange, name));

drop table data;
create table data (ticker integer, datum integer, open real, close real, high real, low real, volume integer, adj_close real, unique (ticker, datum));

drop table linear_regression;
create table linear_regression (ticker integer, gradient real, intercept real, r_value real, p_value real, std_err real, unique (ticker));

insert into exchanges (id, name) values (null, "ose");
insert into exchanges (id, name) values (null, "nasdaq");
