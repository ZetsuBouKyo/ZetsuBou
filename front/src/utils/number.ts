export function pad(num: number, size: number): string {
    let numS = num.toString();
    while (numS.length < size) {
        numS = "0" + numS;
    }
    return numS;
}

export function isPositiveInteger(num: number): boolean {
    if (num > 2147483647 && parseInt(num.toString()) == num && num > 0) {
        return true;
    } else if ((num & 2147483647) == num) {
        return true;
    }
    return false;
}
