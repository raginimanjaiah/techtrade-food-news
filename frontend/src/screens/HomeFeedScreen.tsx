import React, { useState } from 'react';
import {
  View, FlatList, ActivityIndicator,
  RefreshControl, StyleSheet, Text, SafeAreaView,
} from 'react-native';
import { FeaturedCard }  from '../components/FeaturedCard';
import { NewsItem }      from '../components/NewsItem';
import { CategoryTabs }  from '../components/CategoryTabs';
import { useFeed, Article } from '../hooks/useFeed';
import { colors }        from '../theme/colors';

export function HomeFeedScreen() {
  const [category, setCategory] = useState('all');
  const { articles, loading, refreshing, loadMore, refresh } = useFeed(category);

  const renderItem = ({ item, index }: { item: Article; index: number }) =>
    index === 0
      ? <FeaturedCard article={item} />
      : <NewsItem article={item} />;

  return (
    <SafeAreaView style={styles.safe}>
      <View style={styles.navbar}>
        <Text style={styles.logo}>Tech<Text style={styles.logoAccent}>Trade</Text>.Food</Text>
      </View>
      <CategoryTabs active={category} onChange={setCategory} />
      <FlatList
        data={articles}
        keyExtractor={item => item.id}
        renderItem={renderItem}
        onEndReached={loadMore}
        onEndReachedThreshold={0.4}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={refresh} tintColor={colors.primary} />}
        ListFooterComponent={loading ? <ActivityIndicator color={colors.primary} style={{ marginVertical: 20 }} /> : null}
        ListEmptyComponent={!loading ? <Text style={styles.empty}>No articles yet — pull to refresh</Text> : null}
        contentContainerStyle={styles.list}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe:       { flex: 1, backgroundColor: colors.bg },
  navbar:     { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingVertical: 12 },
  logo:       { fontSize: 18, fontWeight: '600', color: colors.text },
  logoAccent: { color: colors.primary },
  list:       { paddingHorizontal: 16, paddingBottom: 80 },
  empty:      { textAlign: 'center', color: colors.textMuted, marginTop: 60, fontSize: 14 },
});