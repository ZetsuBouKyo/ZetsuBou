export function pad(num: number, size: number): string {
  let numS = num.toString();
  while (numS.length < size) {
    numS = "0" + numS;
  }
  return numS;
}
