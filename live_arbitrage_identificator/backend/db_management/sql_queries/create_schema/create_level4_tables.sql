SET search_path TO DB_UNI;

CREATE TABLE IF NOT EXISTS game_participants (
    id SERIAL PRIMARY KEY,
    game_id SERIAL NOT NULL REFERENCES games(id),
    participant_id INTEGER NOT NULL REFERENCES participants(id),
    is_side1 BOOLEAN,
    is_side2 BOOLEAN
);

CREATE TABLE IF NOT EXISTS outcome_detail (
    id SERIAL PRIMARY KEY,
    game_outcome_id INTEGER NOT NULL REFERENCES game_outcome(id),
    details JSONB
);