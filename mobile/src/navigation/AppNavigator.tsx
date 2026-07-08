import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Text } from 'react-native';
import { HomeFeedScreen }  from '../screens/HomeFeedScreen';
import { SegmentsScreen }  from '../screens/SegmentsScreen';
import { colors }          from '../theme/colors';

const Tab = createBottomTabNavigator();

const icon = (emoji: string, focused: boolean) => (
  <Text style={{ fontSize: 20, opacity: focused ? 1 : 0.45 }}>{emoji}</Text>
);

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          headerShown: false,
          tabBarActiveTintColor:   colors.primary,
          tabBarInactiveTintColor: colors.textMuted,
          tabBarStyle: { borderTopColor: colors.border, borderTopWidth: 0.5 },
          tabBarLabelStyle: { fontSize: 11 },
        }}
      >
        <Tab.Screen
          name="Home"
          component={HomeFeedScreen}
          options={{ tabBarIcon: ({ focused }) => icon('🏠', focused) }}
        />
        <Tab.Screen
          name="Segments"
          component={SegmentsScreen}
          options={{ tabBarIcon: ({ focused }) => icon('🏭', focused) }}
        />
        <Tab.Screen
          name="Search"
          component={HomeFeedScreen}
          options={{ tabBarIcon: ({ focused }) => icon('🔍', focused) }}
        />
        <Tab.Screen
          name="Saved"
          component={HomeFeedScreen}
          options={{ tabBarIcon: ({ focused }) => icon('🔖', focused) }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
