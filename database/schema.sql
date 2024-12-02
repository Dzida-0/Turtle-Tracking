CREATE TABLE IF NOT EXISTS Turtles (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        last_position TEXT,
                        active_turtle BOOLEAN,
                        turtle_sex TEXT,
                        turtle_age TEXT,
                        length INT,
                        length_type TEXT,
                        width INT,
                        width_type TEXT,
                        project_name TEXT,
                        biography TEXT,
                        description TEXT
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
