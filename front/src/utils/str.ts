export function toTitle(s: string | number): string {
  s = s.toString();
  s = s.toLowerCase();
  return s.charAt(0).toUpperCase() + s.slice(1);
}
