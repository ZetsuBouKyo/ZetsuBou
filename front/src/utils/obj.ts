export function isEmpty(obj: object) {
    for (var prop in obj) {
        if (Object.prototype.hasOwnProperty.call(obj, prop)) {
            return false;
        }
    }

    return JSON.stringify(obj) === JSON.stringify({});
}

export function getValue(obj: any, key: string | Array<string>, separator: string = ".") {
    const keys = Array.isArray(key) ? key : key.split(separator);
    return keys.reduce((prev, curr) => prev?.[curr], obj);
}

export function setValue(obj: any, key: string | Array<string>, value: any, separator: string = ".") {
    const keys = Array.isArray(key) ? key : key.split(separator);
    const lastKey = keys.pop();
    const lastObj = keys.reduce((prev, curr) => prev?.[curr], obj);
    lastObj[lastKey] = value;
}
