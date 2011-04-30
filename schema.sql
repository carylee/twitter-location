create table status (
  id integer primary key,
  created_at text,
  user_id integer,
  favorited tinyint(1),
  in_reply_to_screen_name text,
  in_reply_to_user_id integer,
  in_reply_to_status_id integer,
  truncated tinyint(1),
  source text,
  text text,
  location text,
  relative_created_at text,
  user text,
  geo text,
  place_id text,
  coordinates text,
  foreign key (place_id) references places(id),
  foreign key (user_id) references users(id)
);

create table entity_types (
  name text primary key
);

create table places (
  id text primary key,
  country_code text,
  name text,
  full_name text,
  street_address text,
  url text,
  country text,
  place_type text
);

create table entities (
  id integer primary key,
  entity_type text,
  data text,
  status_id integer,
  foreign key (status_id) references status(id),
  foreign key (entity_type) references entity_types(from pysqlite3 import ~/twitter-location/twitter as sqlite name)
);

create table users (
  id integer primary key,
  name text,
  created_at text,
  location text,
  description text,
  geo_enabled tinyint(1),
  friends_count integer,
  statuses_count integer,
  screen_name text,
  time_zone text,
  url text,
  utc_offset integer,
  lang en
);

insert into entity_types VALUES ('url');
insert into entity_types VALUES ('hashtag');
insert into entity_types VALUES ('user_mention');
