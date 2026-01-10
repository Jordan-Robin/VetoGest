import axios, { AxiosError, type AxiosResponse } from 'axios'

const api = axios.create({
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

// Intercepteur axios pour gérer les erreurs serveur
// TODO à compléter suite mise en place authentification système, + intercepteur de requête
// Mise en place logger (Sentry ?)
api.interceptors.response.use(function onFulfilled(response: AxiosResponse) {
        return response;
    }, function onRejected(error : AxiosError) {
        if (!error.response) {
            // Erreur de connexion (Backend éteint ou timeout)
            console.error(
                "%c🌐 [Network Error] Impossible de joindre le serveur.",
                "color: #ff4d4d; font-weight: bold; font-size: 12px;"
            );
        } else {
            const status = error.response.status;
            const url = error.config?.url;

            if (status === 401) {
                console.warn(`🔐 [Auth] Session expirée ou non autorisée sur : ${url}. Redirection vers Login...`);
            } else if (status === 403) {
                console.warn(`🚫 [Forbidden] Vous n'avez pas les droits pour accéder à : ${url}`);
            } else if (status >= 500) {
                console.error(`⚠️ [Server Error ${status}] Le backend a rencontré un problème sur : ${url}`);
            } else {
                console.log(`⚠️ [API Error ${status}]`, error.response.data);
            }
        }
        return Promise.reject(error)
    }
);

export default api