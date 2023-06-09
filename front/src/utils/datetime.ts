export function getDatetime(date: string): string {
  const d = new Date(date);
  const offset = d.getTimezoneOffset();
  if (date.match(/\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z)/) === null) {
    d.setMinutes(d.getMinutes() - offset);
  }

  return d.toLocaleString(navigator.language, { timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone });
}

export function toIsoStringWithTimeZone(date: Date): string {
  const tzo = -date.getTimezoneOffset(),
    diff = tzo >= 0 ? "+" : "-",
    pad = function (num: number) {
      const norm = Math.floor(Math.abs(num));
      return (norm < 10 ? "0" : "") + norm;
    };
  const day = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
  const time = `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
  const zone = `${diff}${pad(tzo / 60)}:${pad(tzo % 60)}`;
  return `${day}T${time}${zone}`;
}

export function durationToSecond(duration: string): number {
  const pattern = /^(([0-1]?[0-9]|[2][0-3]):)?([0-5][0-9])(:([0-5][0-9]))$/;
  const match = duration.match(pattern);
  if (match === null) {
    return NaN;
  }
  if (match[2] === undefined) {
    const mins = parseInt(match[3]);
    const seconds = parseInt(match[5]);
    return mins * 60 + seconds;
  }
  const hours = parseInt(match[2]);
  const mins = parseInt(match[3]);
  const seconds = parseInt(match[5]);
  return hours * 3600 + mins * 60 + seconds;
}
