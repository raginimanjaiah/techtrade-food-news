ALTER TABLE articles ADD COLUMN IF NOT EXISTS segment VARCHAR(50) DEFAULT NULL;
CREATE INDEX IF NOT EXISTS idx_articles_segment ON articles (segment);
