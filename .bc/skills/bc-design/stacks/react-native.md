# BC Design System for React Native

Mobile architecture for **iOS & Android** using Expo or React Native CLI.

---

## 1. Native Design Tokens (`constants/theme.ts`)

```ts
export const BCDesignColors = {
  light: {
    background: '#FAF9F5',
    surface: '#FFFFFF',
    text: '#1F1E1B',
    muted: '#6B6760',
    border: 'rgba(31, 30, 27, 0.08)',
    accent: '#D97757',
    accentHover: '#C15F3E',
  },
  dark: {
    background: '#181816',
    surface: '#242421',
    text: '#FAF9F5',
    muted: '#A39E93',
    border: 'rgba(250, 249, 245, 0.09)',
    accent: '#E28466',
    accentHover: '#EA967B',
  },
};
```

---

## 2. Floating Prompt Box with KeyboardAvoidingView

```tsx
import React, { useState } from 'react';
import { View, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform, StyleSheet } from 'react-native';
import { useColorScheme } from 'react-native';
import { BCDesignColors } from '../constants/theme';

export function BCDesignPromptInput({ onSend }: { onSend: (text: string) => void }) {
  const [text, setText] = useState('');
  const scheme = useColorScheme() ?? 'dark';
  const colors = BCDesignColors[scheme];

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={80}
    >
      <View style={[styles.container, { backgroundColor: colors.surface, borderColor: colors.border }]}>
        <TextInput
          value={text}
          onChangeText={setText}
          placeholder="Reply to BC Design..."
          placeholderTextColor={colors.muted}
          multiline
          style={[styles.input, { color: colors.text }]}
        />
        <View style={styles.footer}>
          <TouchableOpacity
            onPress={() => {
              if (text.trim()) {
                onSend(text);
                setText('');
              }
            }}
            style={[styles.sendBtn, { backgroundColor: colors.accent }]}
          >
            <View style={styles.arrowIcon} />
          </TouchableOpacity>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    borderWidth: 1,
    borderRadius: 20,
    padding: 14,
    marginHorizontal: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 4,
  },
  input: {
    fontSize: 16,
    minHeight: 40,
    maxHeight: 120,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginTop: 8,
  },
  sendBtn: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  arrowIcon: {
    width: 0,
    height: 0,
    borderLeftWidth: 5,
    borderRightWidth: 5,
    borderBottomWidth: 8,
    borderStyle: 'solid',
    borderLeftColor: 'transparent',
    borderRightColor: 'transparent',
    borderBottomColor: '#FFF',
  }
});
```
