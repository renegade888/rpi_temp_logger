CREATE TABLE sensor_data( id           integer primary key autoincrement not null
                        , timestamp    datetime default current_timestamp not null
                        , sensor_id    integer not null
                        , value        real not null);
/*
CREATE TABLE sensors( sensor_id        integer primary key
                    , sensor_name      text not null);
*/
