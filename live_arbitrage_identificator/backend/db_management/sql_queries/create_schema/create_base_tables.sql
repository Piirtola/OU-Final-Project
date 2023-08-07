-- This file is used to create the RDB tables that have no dependencies to other tables.
-- After this there are 4 scripts to run to sequentially create the other tables and their dependencies.

CREATE SCHEMA IF NOT EXISTS DB_UNI;
SET search_path TO DB_UNI;


CREATE TABLE IF NOT EXISTS sport_type (
    id SERIAL PRIMARY KEY,
    sport_type VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS status_option (
    id SERIAL PRIMARY KEY,
    status VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS scraper_type (
    id SERIAL PRIMARY KEY,
    scraper_type VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS participant_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS outcome_reason (
    id SERIAL PRIMARY KEY,
    reason VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    iso_code VARCHAR(3) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS bookmakers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    country_id INTEGER REFERENCES countries(id)
);

CREATE TABLE IF NOT EXISTS odds_url (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    live BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS tennis_score (
    id SERIAL PRIMARY KEY,
    side1_sets INTEGER,
    side2_sets INTEGER,
    side1_games INTEGER,
    side2_games INTEGER,
    side1_points INTEGER,
    side2_points INTEGER,
    side1_tiebreak_points INTEGER,
    side2_tiebreak_points INTEGER,
    current_set INTEGER,
    timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS basketball_score (
    id SERIAL PRIMARY KEY,
    side1_points INTEGER,
    side2_points INTEGER,
    current_quarter INTEGER,
    time_remaining_in_quarter TIME,
    timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS table_tennis_score (
    id SERIAL PRIMARY KEY,
    side1_sets INTEGER,
    side2_sets INTEGER,
    side1_points INTEGER,
    side2_points INTEGER,
    current_set INTEGER,
    timestamp TIMESTAMP
);