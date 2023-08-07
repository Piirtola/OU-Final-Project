SET search_path TO DB_UNI;

CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    start_time TIME,
    end_time TIME,
    start_date TIMESTAMP,
    tournament_id INTEGER NOT NULL REFERENCES tournaments(id),
    status_id INTEGER NOT NULL REFERENCES status_option(id)
);

CREATE TABLE IF NOT EXISTS player_pairs (
    id SERIAL PRIMARY KEY,
    player1_id INTEGER NOT NULL REFERENCES players(id),
    player2_id INTEGER NOT NULL REFERENCES players(id)
);



