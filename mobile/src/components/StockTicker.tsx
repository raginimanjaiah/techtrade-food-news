import React, { useEffect, useState, useRef } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import { colors } from '../theme/colors';

const API_BASE = process.env.EXPO_PUBLIC_API_URL ?? 'http://localhost:8000';

interface Stock {
  symbol:     string;
  name:       string;
  price:      number;
  change:     number;
  change_pct: number;
  up:         boolean;
}

export function StockTicker() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const scrollX = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    fetchStocks();
    const interval = setInterval(fetchStocks, 300000); // refresh every 5 min
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (stocks.length === 0) return;
    Animated.loop(
      Animated.timing(scrollX, {
        toValue: -1500,
        duration: 20000,
        useNativeDriver: true,
      })
    ).start();
  }, [stocks]);

  const fetchStocks = async () => {
    try {
      const res  = await fetch(`${API_BASE}/api/stocks`);
      const data = await res.json();
      setStocks(data.stocks ?? []);
    } catch (e) {
      console.error('Stock fetch error:', e);
    }
  };

  if (stocks.length === 0) return null;

  const tickerContent = [...stocks, ...stocks]; // duplicate for seamless loop

  return (
    <View style={styles.bar}>
      <View style={styles.label}>
        <Text style={styles.labelText}>LIVE</Text>
      </View>
      <View style={styles.tickerWrap}>
        <Animated.View
          style={[styles.ticker, { transform: [{ translateX: scrollX }] }]}
        >
          {tickerContent.map((stock, i) => (
            <View key={`${stock.symbol}-${i}`} style={styles.item}>
              <Text style={styles.symbol}>{stock.symbol}</Text>
              <Text style={styles.price}>${stock.price}</Text>
              <Text style={[styles.change, stock.up ? styles.up : styles.down]}>
                {stock.up ? '▲' : '▼'} {Math.abs(stock.change_pct)}%
              </Text>
              <Text style={styles.sep}>  |  </Text>
            </View>
          ))}
        </Animated.View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  bar:        { flexDirection: 'row', backgroundColor: '#0F1F17', height: 36, alignItems: 'center', overflow: 'hidden' },
  label:      { backgroundColor: '#1D9E75', paddingHorizontal: 10, height: '100%', justifyContent: 'center', flexShrink: 0 },
  labelText:  { color: '#fff', fontSize: 11, fontWeight: '700', letterSpacing: 1 },
  tickerWrap: { flex: 1, overflow: 'hidden' },
  ticker:     { flexDirection: 'row', alignItems: 'center' },
  item:       { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, gap: 6 },
  symbol:     { color: '#fff', fontSize: 12, fontWeight: '600' },
  price:      { color: '#E8E8E4', fontSize: 12 },
  change:     { fontSize: 12, fontWeight: '500' },
  up:         { color: '#4ADE80' },
  down:       { color: '#F87171' },
  sep:        { color: '#333', fontSize: 12 },
});
