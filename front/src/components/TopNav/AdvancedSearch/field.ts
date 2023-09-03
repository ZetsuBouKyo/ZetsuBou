export class RouteQueryKey {
  private name: string;
  constructor(name: string) {
    this.name = name;
  }
  get fuzziness(): string {
    return `${this.name}_fuzziness`;
  }
  get analyzer(): string {
    return `${this.name}_analyzer`;
  }
  get bool(): string {
    return `${this.name}_bool`;
  }
  get gte(): string {
    return `${this.name}_gte`;
  }
  get lte(): string {
    return `${this.name}_lte`;
  }
}
