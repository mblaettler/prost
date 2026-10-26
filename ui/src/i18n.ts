import { createI18n } from 'vue-i18n';
import en from './locales/en';
import de from './locales/de';

export type MessageSchema = typeof en;

const messages = { en, de };
type Locale = keyof typeof messages;

// First supported language in the browser's preference list; German if none matches
const detectLocale = (): Locale => {
  const languages = navigator.languages?.length ? navigator.languages : [navigator.language];
  for (const language of languages) {
    const primary = language?.toLowerCase().split('-')[0];
    if (primary && primary in messages) return primary as Locale;
  }
  return 'de';
};

const locale = detectLocale();
document.documentElement.lang = locale;

export const i18n = createI18n<[MessageSchema], Locale>({
  legacy: false,
  locale,
  fallbackLocale: 'de',
  messages,
});
