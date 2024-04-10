DROP TABLE IF EXISTS votes;

CREATE TABLE votes (
    PRIMARY KEY (id),
    id         INT GENERATED ALWAYS AS IDENTITY,
    story_id   INT NOT NULL,
               FOREIGN KEY (story_id)
               REFERENCES stories(id),
    vote       CHAR(1) NOT NULL CHECK (vote = 'u' OR vote = 'd'),
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()::timestamp,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()::timestamp
);