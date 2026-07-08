ALTER TABLE articles ADD COLUMN segment VARCHAR(50) DEFAULT NULL;
CREATE INDEX idx_articles_segment ON articles (segment);
