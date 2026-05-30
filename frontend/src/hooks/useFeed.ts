import { useState, useEffect, useCallback } from 'react';

const API_BASE = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

export interface Article {
  id:            string;
  title:         string;
  summary?:      string;
  url:           string;
  image_url?:    string;
  source?:       string;
  category?:     string;
  is_breaking:   boolean;
  published_at?: string;
}

export function useFeed(category: string) {
  const [articles, setArticles]     = useState<Article[]>([]);
  const [page, setPage]             = useState(1);
  const [loading, setLoading]       = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [hasMore, setHasMore]       = useState(true);

  const fetchFeed = useCallback(async (p = 1, replace = false) => {
    setLoading(true);
    try {
      const res  = await fetch(`${API_BASE}/api/feed?category=${category}&page=${p}&limit=20`);
      const data = await res.json();
      const incoming: Article[] = data.articles ?? [];
      setArticles(prev => replace ? incoming : [...prev, ...incoming]);
      setPage(p);
      setHasMore(incoming.length === 20);
    } catch (e) {
      console.error('Feed fetch error:', e);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [category]);

  useEffect(() => {
    setArticles([]);
    setPage(1);
    fetchFeed(1, true);
  }, [category]);

  const loadMore = useCallback(() => { if (!loading && hasMore) fetchFeed(page + 1); }, [page, loading, hasMore, fetchFeed]);
  const refresh  = useCallback(() => { setRefreshing(true); fetchFeed(1, true); }, [fetchFeed]);

  return { articles, loading, refreshing, loadMore, refresh };
}