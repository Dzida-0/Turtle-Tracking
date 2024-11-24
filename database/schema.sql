CREATE TABLE IF NOT EXISTS Turtles (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        species TEXT,
                        last_move_datetime TEXT,
                        distance_from_release TEXT,
                        avg_speed_from_release TEXT,
                        time_from_release TEXT,
                        time_from_last_move TEXT,
                        time_tracked TEXT,
                        description TEXT,
                        project TEXT,
                        biography TEXT
                        );

CREATE TABLE IF NOT EXISTS Positions (
            id INTEGER PRIMARY KEY,
             latitude DOUBLE,
             longitude DOUBLE,
             distance DOUBLE,
             duration DOUBLE,
             direction TEXT,
             time TEXT
             );
