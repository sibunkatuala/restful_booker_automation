import logging

from config.config import BASE_URL


logger = logging.getLogger(__name__)


class APIClient:

    def __init__(self, request_context):
        self.request_context = request_context

    def _build_url(self, endpoint):
        return f"{BASE_URL}{endpoint}"

    def _headers(self, token=None):

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if token:
            headers["Cookie"] = f"token={token}"

        return headers

    def _log_response(self, method, url, response):

        logger.info(
            "%s %s - %s",
            method,
            url,
            response.status
        )

        if response.status >= 400:
            logger.error(
                "%s %s failed with status %s",
                method,
                url,
                response.status
            )

            try:
                logger.error(
                    "Response: %s",
                    response.text()
                )
            except Exception:
                pass

    def get(self, endpoint, params=None, headers=None, token=None):

        url = self._build_url(endpoint)

        logger.info("GET %s", url)

        response = self.request_context.get(
            url,
            params=params,
            headers=headers or self._headers(token)
        )

        self._log_response("GET", url, response)

        return response

    def post(self, endpoint, data=None, headers=None, token=None):

        url = self._build_url(endpoint)

        logger.info("POST %s", url)

        response = self.request_context.post(
            url,
            data=data,
            headers=headers or self._headers(token)
        )

        self._log_response("POST", url, response)

        return response

    def put(self, endpoint, data=None, headers=None, token=None):

        url = self._build_url(endpoint)

        logger.info("PUT %s", url)

        response = self.request_context.put(
            url,
            data=data,
            headers=headers or self._headers(token)
        )

        self._log_response("PUT", url, response)

        return response

    def patch(self, endpoint, data=None, headers=None, token=None):

        url = self._build_url(endpoint)

        logger.info("PATCH %s", url)

        response = self.request_context.patch(
            url,
            data=data,
            headers=headers or self._headers(token)
        )

        self._log_response("PATCH", url, response)

        return response

    def delete(self, endpoint, headers=None, token=None):

        url = self._build_url(endpoint)

        logger.info("DELETE %s", url)

        response = self.request_context.delete(
            url,
            headers=headers or self._headers(token)
        )

        self._log_response("DELETE", url, response)

        return response