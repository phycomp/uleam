import { Container } from "cloudflare:containers";

export class AppContainer extends Container {
  defaultPort = 8501;
  sleepAfter = "2m";
}

export default {
  async fetch(request, env) {
    const id = env.APP_CONTAINER.idFromName("app");
    const container = env.APP_CONTAINER.get(id);
    return container.fetch(request);
  },
};