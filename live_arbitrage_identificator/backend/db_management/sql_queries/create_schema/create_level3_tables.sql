SET search_path TO DB_UNI;


CREATE TABLE IF NOT EXISTS odds_snapshot (
    id SERIAL PRIMARY KEY,
    game_id SERIAL NOT NULL REFERENCES games(id),
    bookmaker_id INTEGER NOT NULL REFERENCES bookmakers(id),
    side1_odds DECIMAL,
    side2_odds DECIMAL,
    timestamp TIMESTAMP,
    odds_url_id INTEGER NOT NULL REFERENCES odds_url(id)
);



CREATE TABLE IF NOT EXISTS participants (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    player_pair_id INTEGER REFERENCES player_pairs(id),
    team_id INTEGER REFERENCES teams(id),
    participant_type_id INTEGER NOT NULL REFERENCES participant_type(id)
);


CREATE TABLE IF NOT EXISTS game_scraper_details (
    id SERIAL PRIMARY KEY,
    game_id SERIAL NOT NULL REFERENCES games(id),
    scraper_type_id SERIAL NOT NULL REFERENCES scraper_type(id),
    url TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS game_score (
    id SERIAL PRIMARY KEY,
    game_id SERIAL NOT NULL REFERENCES games(id),
    tennis_score_id INTEGER REFERENCES tennis_score(id),
    basketball_score_id INTEGER REFERENCES basketball_score(id),
    table_tennis_score_id INTEGER REFERENCES table_tennis_score(id)
);

CREATE TABLE IF NOT EXISTS game_outcome (
    id SERIAL PRIMARY KEY,
    game_id SERIAL NOT NULL REFERENCES games(id),
    side1_won BOOLEAN,
    side2_won BOOLEAN,
    outcome_reason_id INTEGER NOT NULL REFERENCES outcome_reason(id),
    timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS post_scrap_metadata (
    id SERIAL PRIMARY KEY,
    game_id SERIAL NOT NULL REFERENCES games(id),
    pre_scrap_metadata_id INTEGER NOT NULL REFERENCES pre_scrap_metadata(id)
);