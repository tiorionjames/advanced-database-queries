-- read into psql with:
-- \i data/journal.sql
DROP TABLE IF EXISTS entry;

CREATE TABLE entry (
    id SERIAL PRIMARY KEY,
    posted_date DATE NOT NULL DEFAULT NOW(),
    title VARCHAR(255) NOT NULL DEFAULT '',
    body TEXT NOT NULL
);

INSERT INTO entry (posted_date, title, body)
VALUES
    ('2025-03-01', 'a title', 'bunch of stuff 1'),
    ('2025-03-02', '', 'bunch of stuff 2'),
    ('2025-03-03', 'happy day', 'bunch of stuff 3'),
    ('2025-03-04', 'cloudy', 'bunch of stuff 4');