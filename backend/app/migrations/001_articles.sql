-- MySQL version
CREATE TABLE IF NOT EXISTS articles (
    id           CHAR(36)        PRIMARY KEY DEFAULT (UUID()),
    url_hash     VARCHAR(32)     UNIQUE NOT NULL,
    title        TEXT            NOT NULL,
    summary      TEXT,
    url          TEXT            NOT NULL,
    image_url    TEXT,
    source       VARCHAR(255),
    category     VARCHAR(50)     DEFAULT 'industry',
    is_breaking  BOOLEAN         DEFAULT FALSE,
    published_at DATETIME        DEFAULT CURRENT_TIMESTAMP,
    ingested_at  DATETIME        DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_articles_published ON articles (published_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_category  ON articles (category);
CREATE INDEX IF NOT EXISTS idx_articles_breaking  ON articles (is_breaking);
