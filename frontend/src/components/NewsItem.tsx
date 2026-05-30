import React from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet, Linking } from 'react-native';
import { Article } from '../hooks/useFeed';
import { colors } from '../theme/colors';

interface Props { article: Article }

const CATEGORY_LABELS: Record<string, string> = {
  industry:    'Industry',
  market_news: 'Markets',
  technology:  'Technology',
  regulatory:  'Regulatory',
  exhibition:  'Exhibition',
};

export function NewsItem({ article }: Props) {
  return (
    <TouchableOpacity style={styles.row} onPress={() => Linking.openURL(article.url)} activeOpacity={0.8}>
      {article.image_url ? (
        <Image source={{ uri: article.image_url }} style={styles.thumb} resizeMode="cover" />
      ) : (
        <View style={styles.thumbPlaceholder} />
      )}
      <View style={styles.content}>
        <Text style={styles.title} numberOfLines={2}>{article.title}</Text>
        <View style={styles.meta}>
          <View style={styles.tag}>
            <Text style={styles.tagText}>{CATEGORY_LABELS[article.category ?? ''] ?? 'News'}</Text>
          </View>
          <Text style={styles.source}>{article.source}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  row:              { flexDirection: 'row', gap: 12, paddingVertical: 12, borderBottomWidth: 0.5, borderColor: colors.border },
  thumb:            { width: 72, height: 72, borderRadius: 8, backgroundColor: colors.bgSecond },
  thumbPlaceholder: { width: 72, height: 72, borderRadius: 8, backgroundColor: colors.bgSecond },
  content:          { flex: 1, justifyContent: 'space-between' },
  title:            { fontSize: 13, fontWeight: '500', color: colors.text, lineHeight: 19 },
  meta:             { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 6 },
  tag:              { backgroundColor: colors.bgSecond, paddingHorizontal: 7, paddingVertical: 2, borderRadius: 4 },
  tagText:          { fontSize: 11, color: colors.textMuted },
  source:           { fontSize: 11, color: colors.textHint },
});