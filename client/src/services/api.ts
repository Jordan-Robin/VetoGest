import axios, {
  AxiosError,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios";

const baseURL = import.meta.env.PROD ? import.meta.env.VITE_API_URL : "/api";

const api = axios.create({
  baseURL: baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Intercepteur de requête pour ajouter le token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem("accessToken");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Intercepteur de réponse pour gérer les erreurs
api.interceptors.response.use(
  function onFulfilled(response: AxiosResponse) {
    return response;
  },
  async function onRejected(error: AxiosError) {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    // Si 401 et pas déjà retry, tenter de rafraîchir le token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refreshToken");

      if (refreshToken) {
        try {
          const response = await axios.post(`${baseURL}/token/refresh/`, {
            refresh: refreshToken,
          });
          const { access } = response.data;
          localStorage.setItem("accessToken", access);

          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${access}`;
          }
          return api(originalRequest);
        } catch {
          // Refresh échoué, déconnecter l'utilisateur
          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");
          window.dispatchEvent(new Event("auth-error"));
        }
      }
    }

    if (!error.response) {
      console.error(
        "%c🌐 [Network Error] Impossible de joindre le serveur.",
        "color: #ff4d4d; font-weight: bold; font-size: 12px;",
      );
    } else {
      const status = error.response.status;
      const url = error.config?.url;

      if (status === 401) {
        console.warn(`🔐 [Auth] Session expirée ou non autorisée sur : ${url}`);
      } else if (status === 403) {
        console.warn(
          `🚫 [Forbidden] Vous n'avez pas les droits pour accéder à : ${url}`,
        );
      } else if (status >= 500) {
        console.error(
          `⚠️ [Server Error ${status}] Le backend a rencontré un problème sur : ${url}`,
        );
      } else {
        console.log(`⚠️ [API Error ${status}]`, error.response.data);
      }
    }
    return Promise.reject(error);
  },
);

export default api;
