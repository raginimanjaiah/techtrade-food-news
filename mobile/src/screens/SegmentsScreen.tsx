import React, { useEffect, useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity,
  StyleSheet, SafeAreaView, ActivityIndicator, RefreshControl,
} from 'react-native';
import { colors } from '../theme/colors';
import { Article } from '../hooks/useFeed';
import { NewsItem } from '../components/NewsItem';
import { FeaturedCard } from '../components/FeaturedCard';

const API_BASE = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

interface Segment {
  key:   string;
  label: string;
  icon:  string;
  count: number;
}

export function SegmentsScreen() {
  const [segments,    setSegments]    = useState<Segment[]>([]);
  const [active,      setActive]      = useState<Segment | null>(null);
  const [articles,    setArticles]    = useState<Article[]>([]);
  const [loading,     setLoading]     = useState(false);
  const [refreshing,  setRefreshing]  = useState(false);
  const [page,        setPage]        = useState(1);
  const [hasMore,     setHasMore]     = useState(true);

  useEffect(() => { fetchSegments(); }, []);

  const fetchSegments = async () => {
    try {
      const res  = await fetch(`${API_BASE}/api/segments`);
      const data = await res.json();
      setSegments(data);
    } catch (e) {
      console.error('Segments fetch error:', e);
    }
  };

  const openSegment = async (seg: Segment, p = 1, replace = false) => {
    if (p === 1) { setActive(seg); setLoading(true); }
    try {
      const res  = await fetch(`${API_BASE}/api/segments/${seg.key}?page=${p}&limit=20`);
      const data = await res.json();
      const incoming: Article[] = data.articles ?? [];
      setArticles(prev => replace ? incoming : [...prev, ...incoming]);
      setPage(p);
      setHasMore(incoming.length === 20);
    } catch (e) {
      console.error('Segment feed error:', e);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const goBack = () => {
    setActive(null);
    setArticles([]);
    setPage(1);
  };

  const loadMore = () => {
    if (!loading && hasMore && active) openSegment(active, page + 1);
  };

  const refresh = () => {
    if (active) { setRefreshing(true); openSegment(active, 1, true); }
  };

  if (active) {
    return (
      <SafeAreaView style={styles.safe}>
        <View style={styles.segHeader}>
          <TouchableOpacity onPress={goBack} style={styles.backBtn}>
            <Text style={styles.backText}>← Back</Text>
          </TouchableOpacity>
          <Text style={styles.segTitle}>{active.icon}  {active.label}</Text>
        </View>
        {loading && articles.length === 0 ? (
          <ActivityIndicator color={colors.primary} style={{ marginTop: 40 }} />
        ) : (
          <FlatList
            data={articles}
            keyExtractor={item => item.id}
            renderItem={({ item, index }) =>
              index === 0 ? <FeaturedCard article={item} /> : <NewsItem article={item} />
            }
            onEndReached={loadMore}
            onEndReachedThreshold={0.4}
            refreshControl={
              <RefreshControl refreshing={refreshing} onRefresh={refresh} tintColor={colors.primary} />
            }
            ListFooterComponent={loading ? <ActivityIndicator color={colors.primary} style={{ margin: 20 }} /> : null}
            ListEmptyComponent={
              <Text style={styles.empty}>No articles in this segment yet</Text>
            }
            contentContainerStyle={styles.list}
          />
        )}
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.navbar}>
        <Text style={styles.logo}>
          Tech<Text style={styles.logoAccent}>Trade</Text>.Food
        </Text>
        <Text style={styles.navSub}>by market segment</Text>
      </View>

      <FlatList
        data={segments}
        keyExtractor={item => item.key}
        numColumns={2}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.segCard}
            onPress={() => openSegment(item, 1, true)}
            activeOpacity={0.8}
          >
            <Text style={styles.segIcon}>{item.icon}</Text>
            <Text style={styles.segLabel}>{item.label}</Text>
            <Text style={styles.segCount}>{item.count} articles</Text>
          </TouchableOpacity>
        )}
        contentContainerStyle={styles.grid}
        ListHeaderComponent={
          <Text style={styles.gridTitle}>Browse by food processing sector</Text>
        }
        ListEmptyComponent={
          <ActivityIndicator color={colors.primary} style={{ marginTop: 60 }} />
        }
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={fetchSegments} tintColor={colors.primary} />
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe:       { flex: 1, backgroundColor: colors.bg },
  navbar:     { flexDirection: 'row', alignItems: 'baseline', justifyContent: 'space-between', paddingHorizontal: 16, paddingVertical: 12 },
  logo:       { fontSize: 18, fontWeight: '600', color: colors.text },
  logoAccent: { color: colors.primary },
  navSub:     { fontSize: 12, color: colors.textMuted },
  gridTitle:  { fontSize: 13, color: colors.textMuted, paddingHorizontal: 16, paddingBottom: 12 },
  grid:       { paddingHorizontal: 10, paddingBottom: 80 },
  segCard:    {
    flex: 1, margin: 6, padding: 16,
    backgroundColor: colors.bg,
    borderRadius: 12,
    borderWidth: 0.5, borderColor: colors.border,
    minHeight: 110,
    justifyContent: 'space-between',
  },
  segIcon:    { fontSize: 28, marginBottom: 8 },
  segLabel:   { fontSize: 13, fontWeight: '500', color: colors.text, marginBottom: 4 },
  segCount:   { fontSize: 11, color: colors.textMuted },
  segHeader:  { flexDirection: 'row', alignItems: 'center', gap: 12, paddingHorizontal: 16, paddingVertical: 10, borderBottomWidth: 0.5, borderColor: colors.border },
  backBtn:    { paddingVertical: 6, paddingHorizontal: 10, borderRadius: 8, borderWidth: 0.5, borderColor: colors.border },
  backText:   { fontSize: 13, color: colors.textMuted },
  segTitle:   { fontSize: 15, fontWeight: '500', color: colors.text },
  list:       { paddingHorizontal: 16, paddingBottom: 80 },
  empty:      { textAlign: 'center', color: colors.textMuted, marginTop: 60, fontSize: 14 },
});
