CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS articles (
    id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    url_hash     TEXT        UNIQUE NOT NULL,
    title        TEXT        NOT NULL,
    summary      TEXT,
    url          TEXT        NOT NULL,
    image_url    TEXT,
    source       TEXT,
    category     TEXT        DEFAULT 'industry',
    is_breaking  BOOLEAN     DEFAULT false,
    published_at TIMESTAMPTZ DEFAULT NOW(),
    ingested_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_articles_published ON articles (published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_category  ON articles (category);
CREATE INDEX IF NOT EXISTS idx_articles_breaking  ON articles (is_breaking) WHERE is_breaking = true;
