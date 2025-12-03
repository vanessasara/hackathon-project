/**
 * Google Keep Color Palette
 * 12 colors with light and dark mode variants
 */

export type ColorKey =
  | "default"
  | "coral"
  | "peach"
  | "sand"
  | "mint"
  | "sage"
  | "fog"
  | "storm"
  | "dusk"
  | "blossom"
  | "clay"
  | "chalk";

export interface ColorVariant {
  light: string;
  dark: string;
}

export const KEEP_COLORS: Record<ColorKey, ColorVariant> = {
  default: { light: "transparent", dark: "transparent" },
  coral: { light: "#f28b82", dark: "#77172e" },
  peach: { light: "#fbbc04", dark: "#692b17" },
  sand: { light: "#fff475", dark: "#7c4a03" },
  mint: { light: "#ccff90", dark: "#264d3b" },
  sage: { light: "#a7ffeb", dark: "#0c625d" },
  fog: { light: "#cbf0f8", dark: "#256377" },
  storm: { light: "#aecbfa", dark: "#1e3a5f" },
  dusk: { light: "#d7aefb", dark: "#42275e" },
  blossom: { light: "#fdcfe8", dark: "#5b2245" },
  clay: { light: "#e6c9a8", dark: "#442f19" },
  chalk: { light: "#e8eaed", dark: "#3c3f43" },
};

export const COLOR_KEYS = Object.keys(KEEP_COLORS) as ColorKey[];

/**
 * Get the appropriate color based on theme
 */
export function getColor(colorKey: ColorKey, isDark: boolean): string {
  const color = KEEP_COLORS[colorKey];
  return isDark ? color.dark : color.light;
}

/**
 * Get both color variants for CSS custom property usage
 */
export function getColorStyles(colorKey: ColorKey): {
  "--note-color-light": string;
  "--note-color-dark": string;
} {
  const color = KEEP_COLORS[colorKey];
  return {
    "--note-color-light": color.light,
    "--note-color-dark": color.dark,
  };
}
