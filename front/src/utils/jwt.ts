function getJSON(base64UrlString: string): object {
  // https://stackoverflow.com/questions/38552003/how-to-decode-jwt-token-in-javascript-without-using-a-library

  const base64String = base64UrlString.replace(/-/g, "+").replace(/_/g, "/");
  const decodedString = decodeURIComponent(
    window
      .atob(base64String)
      .split("")
      .map(function (c) {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join(""),
  );
  return JSON.parse(decodedString);
}

function getJSONString(base64UrlString: string): string {
  const jsonObject = getJSON(base64UrlString);
  return JSON.stringify(jsonObject, null, 4);
}

export class JWTParser {
  private token: string;
  private parts: Array<string>;

  constructor(token: string) {
    this.token = token;
    this.parts = this.token.split(".");
  }
  get headerString(): string {
    return getJSONString(this.parts[0]);
  }
  get payloadString(): string {
    return getJSONString(this.parts[1]);
  }
}
