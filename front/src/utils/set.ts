export function isSetEqual(s1: Set<any>, s2: Set<any>): boolean {
  if (s1.size !== s2.size) {
    return false;
  }
  for (const s of s2) {
    if (!s1.has(s)) {
      return false;
    }
  }
  return true;
}
