export function detectRouteChange(route: any) {
  if (route === undefined) {
    return undefined;
  }
  return JSON.stringify(route.path) + JSON.stringify(route.query) + JSON.stringify(route.params);
}
