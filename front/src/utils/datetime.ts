import { pad } from "@/utils/number";

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
    const pattern = /^(([0-1]?[0-9]|[2][0-3]):)?([0-5]?[0-9])(:([0-5][0-9]))$/;
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

// Currently have maximum value: 23 x 60 x 60 + 59 x 60 + 59 seconds.
export function secondToDuration(s: number): string {
    const m = 86399; // 23 * 60 * 60 + 59 * 60 + 59
    if (s > 86399 || s < 0) {
        throw new RangeError("s must be 0 <= s < 86400");
    }
    const seconds = s % 60;
    let minutes = Math.floor(s / 60);
    if (minutes === 0) {
        return seconds.toString();
    }
    const hours = Math.floor(minutes / 60);
    minutes = minutes % 60;

    const secondsS = pad(seconds, 2);
    const minutesS = pad(minutes, 2);

    if (hours === 0) {
        return `${minutesS}:${secondsS}`;
    }

    const hoursS = hours.toString();

    return `${hoursS}:${minutesS}:${secondsS}`;
}

export function isLeapYear(year: number): boolean {
    if (year % 4 !== 0) {
        return false;
    }
    if (year % 100 !== 0) {
        return true;
    }
    if (year % 400 !== 0) {
        return false;
    }
    return true;
}
