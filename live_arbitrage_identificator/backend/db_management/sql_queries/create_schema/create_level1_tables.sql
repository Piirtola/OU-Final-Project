SET search_path TO DB_UNI;


CREATE TABLE IF NOT EXISTS pre_scrap_metadata (
    id SERIAL PRIMARY KEY,
    scraper_type_id SERIAL NOT NULL REFERENCES scraper_type(id),
    url TEXT UNIQUE NOT NULL,
    sport_type_id INTEGER NOT NULL REFERENCES sport_type(id),
    game_status_id INTEGER NOT NULL REFERENCES status_option(id),
    fetch_timestamp TIMESTAMP,
    match_date DATE NOT NULL,
    match_time TIME WITH TIME ZONE,
    number_of_bookmakers INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    country_id INTEGER NOT NULL REFERENCES countries(id)
);

CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_id INTEGER NOT NULL REFERENCES countries(id)
);

CREATE TABLE IF NOT EXISTS tournaments
(
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    country_id    INTEGER      NOT NULL REFERENCES countries (id),
    sport_type_id INTEGER      NOT NULL REFERENCES sport_type (id),
    year          INTEGER,
    details       JSONB
);

CREATE TABLE IF NOT EXISTS bookmaker_details (
    id SERIAL PRIMARY KEY,
    bookmaker_id INTEGER NOT NULL REFERENCES bookmakers(id),
    normal_bet_cost DECIMAL,
    max_bet DECIMAL,
    min_bet DECIMAL,
    other_details JSONB
);
