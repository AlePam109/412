-- schema_pre.sql: Pre-population schema without constraints

CREATE TABLE business (
    business_id TEXT,           -- will be converted to PK
    name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    latitude FLOAT,
    longitude FLOAT,
    stars FLOAT,
    review_count INTEGER,
    is_open INTEGER,            -- will be converted to boolean
    attributes JSONB,
    categories TEXT[],
    hours JSONB,
    business_account_id INTEGER -- will be converted to nullable fk
);

CREATE TABLE review (
    review_id TEXT,             -- will be converted to PK
    user_id TEXT,
    business_id TEXT,
    stars INTEGER,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    text TEXT,
    date DATE                   -- YYYY-MM-DD
);

CREATE TABLE yelp_user (
    user_id TEXT,               -- will be converted to pk
    name TEXT,
    yelping_since DATE,         -- YYYY-MM-DD
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    compliment_useful INTEGER,  -- renamed, data from compliment_writer
    compliment_cool INTEGER,
    compliment_funny INTEGER,
    average_stars FLOAT,
    review_count INTEGER,
    username TEXT,
    password TEXT
);

CREATE TABLE tip (
    user_id TEXT,               -- will be converted to fk
    business_id TEXT,           -- will be converted to fk
    text TEXT,
    date DATE,                  -- YYYY-MM-DD
    praise_count INTEGER        -- renamed, data from compliment_count
);

CREATE TABLE business_account (
    account_id INTEGER,             -- will be converted to AUTO INT PK
    username TEXT,
    password TEXT,
    name TEXT,
    business_count INTEGER
);

