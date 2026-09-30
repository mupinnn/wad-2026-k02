import { type MaybeRefOrGetter, type Ref} from "vue";
type HttpMethod = "GET" | "POST" | "DELETE";

export interface UseFetchOptions {
  url: MaybeRefOrGetter<string>;
  method?: HttpMethod;
  body?: MaybeRefOrGetter<unknown>;
  immediate?: boolean;
  config?: RequestInit;
}

export interface UseFetchReturn<T> {
  data: Ref<T | null>;
  loading: Ref<boolean>;
  error: Ref<string | null>;
  execute: () => Promise<void>;
}