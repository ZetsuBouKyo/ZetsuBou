export function toTitle(s: string | number): string {
  s = s.toString();
  s = s.toLowerCase();
  return s.charAt(0).toUpperCase() + s.slice(1);
}

export function getUUID() {
  return (<any>[1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c: any) =>
    (c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))).toString(16),
  );
}

export function joinWithAnd(arr: Array<string>) {
  let s = "";
  if (arr.length === 1) {
    s = arr[0];
  } else if (arr.length === 2) {
    s = arr.join(" and ");
  } else if (arr.length > 2) {
    s = arr.slice(0, -1).join(", ") + ", and " + arr.slice(-1);
  }
  return s;
}
