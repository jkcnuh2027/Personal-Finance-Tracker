CREATE DATABASE finance_db;

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    amount NUMERIC NOT NULL,
    description TEXT
);
