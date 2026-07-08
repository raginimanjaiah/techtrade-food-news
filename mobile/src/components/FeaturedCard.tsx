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

export function FeaturedCard({ article }: Props) {
  return (
    <TouchableOpacity
      style={styles.card}
      onPress={() => Linking.openURL(article.url)}
      activeOpacity={0.85}
    >
      {article.is_breaking && (
        <View style={styles.breakingBadge}>
          <Text style={styles.breakingText}>Breaking</Text>
        </View>
      )}
      {article.image_url ? (
        <Image
          source={{ uri: article.image_url }}
          style={styles.image}
          resizeMode="cover"
        />
      ) : null}
      <View style={styles.body}>
        <Text style={styles.category}>
          {CATEGORY_LABELS[article.category ?? ''] ?? 'News'}
        </Text>
        <Text style={styles.title} numberOfLines={3}>
          {article.title}
        </Text>
        <Text style={styles.meta}>
          {article.source} · {article.published_at
            ? new Date(article.published_at).toLocaleDateString()
            : ''}
        </Text>
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.bg,
    borderRadius:    12,
    overflow:        'hidden',
    marginBottom:    12,
    borderWidth:     0.5,
    borderColor:     colors.border,
  },
  breakingBadge: {
    position:        'absolute',
    top:             10,
    left:            10,
    zIndex:          1,
    backgroundColor: colors.breakingBg,
    paddingHorizontal: 8,
    paddingVertical:   3,
    borderRadius:    4,
  },
  breakingText: {
    fontSize:   11,
    fontWeight: '600',
    color:      colors.breaking,
  },
  image: {
    width:           '100%',
    height:          180,
    backgroundColor: colors.primaryBg,
  },
  body: {
    padding: 14,
  },
  category: {
    fontSize:      11,
    fontWeight:    '600',
    color:         colors.primary,
    letterSpacing: 0.5,
    marginBottom:  6,
  },
  title: {
    fontSize:     16,
    fontWeight:   '500',
    color:        colors.text,
    lineHeight:   22,
    marginBottom: 8,
  },
  meta: {
    fontSize: 12,
    color:    colors.textMuted,
  },
});
