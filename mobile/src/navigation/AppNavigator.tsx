import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { HomeFeedScreen } from '../screens/HomeFeedScreen';
import { colors } from '../theme/colors';
import { Text } from 'react-native';

const Tab = createBottomTabNavigator();

const icon = (name: string, focused: boolean) => (
  <Text style={{ fontSize: 20, color: focused ? colors.primary : colors.textMuted }}>
    {name}
  </Text>
);

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          headerShown: false,
          tabBarActiveTintColor: colors.primary,
          tabBarInactiveTintColor: colors.textMuted,
          tabBarStyle: { borderTopColor: colors.border, borderTopWidth: 0.5 },
        }}
      >
        <Tab.Screen name="Home"   component={HomeFeedScreen} options={{ tabBarIcon: ({ focused }) => icon('⌂', focused) }} />
        <Tab.Screen name="Events" component={HomeFeedScreen} options={{ tabBarIcon: ({ focused }) => icon('◷', focused) }} />
        <Tab.Screen name="Search" component={HomeFeedScreen} options={{ tabBarIcon: ({ focused }) => icon('⌕', focused) }} />
        <Tab.Screen name="Saved"  component={HomeFeedScreen} options={{ tabBarIcon: ({ focused }) => icon('♡', focused) }} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
