import React from 'react';
import { ScrollView, TouchableOpacity, Text, StyleSheet } from 'react-native';
import { colors, CATEGORIES } from '../theme/colors';

interface Props {
  active: string;
  onChange: (key: string) => void;
}

export function CategoryTabs({ active, onChange }: Props) {
  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      style={styles.bar}
      contentContainerStyle={styles.content}
    >
      {CATEGORIES.map(cat => (
        <TouchableOpacity
          key={cat.key}
          onPress={() => onChange(cat.key)}
          style={[styles.tab, active === cat.key && styles.tabActive]}
        >
          <Text style={[styles.label, active === cat.key && styles.labelActive]}>
            {cat.label}
          </Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  bar:         { borderBottomWidth: 0.5, borderColor: colors.border },
  content:     { paddingHorizontal: 16, gap: 4 },
  tab:         { paddingHorizontal: 14, paddingVertical: 10, borderBottomWidth: 2, borderBottomColor: 'transparent' },
  tabActive:   { borderBottomColor: colors.primary },
  label:       { fontSize: 13, color: colors.textMuted },
  labelActive: { color: colors.primary, fontWeight: '500' },
});
