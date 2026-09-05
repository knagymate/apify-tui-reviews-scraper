from apify._actor import _ActorType, Actor
from apify_common.client import AsyncHttpClient, ProxySettings
from apify_common.retry import RetryRule, retry
from curl_cffi.requests.exceptions import ConnectionError

from src.exceptions import ServerError
from src.models import AggregateResponse, ReviewsPage
from src.parser import ensure_search_scope

AGGREGATE_URL = (
    "https://cloud.tui.com/osp/ao/ml/customer-reviews/reviews/customerReviews/"
)
REVIEWS_URL = "https://cloud.tui.com/osp/ao/ml/customer-reviews/reviews/"

LOCALE = "de-DE"
PAGE_LIMIT = 100

HEADERS = {
    "accept": "*/*",
    "origin": "https://www.tui.com",
    "referer": "https://www.tui.com/",
}


class Client(AsyncHttpClient):
    @retry(
        rules=[
            RetryRule(
                exception=[ServerError, ConnectionError],
                new_proxy=ProxySettings(groups=["auto"], country_code="US"),
                new_impersonate=True,
                clean_cookies=True,
            ),
        ],
        max_retries=3,
    )
    async def get_start_url(self, url: str) -> tuple[str, str]:
        assert self.client

        response = await self.client.get(ensure_search_scope(url))

        if response.status_code >= 500:
            raise ServerError("Server error occurred.")

        return response.text, str(response.url)

    @retry(
        rules=[
            RetryRule(
                exception=[ServerError, ConnectionError],
                new_proxy=ProxySettings(groups=["auto"], country_code="US"),
                new_impersonate=True,
                clean_cookies=True,
            ),
        ],
        max_retries=3,
    )
    async def get_aggregate(self, hotel_id: str) -> AggregateResponse:
        assert self.client

        response = await self.client.get(
            AGGREGATE_URL,
            params={
                "locale": LOCALE,
                "limit": PAGE_LIMIT,
                "accommodationCode": hotel_id,
            },
            headers=HEADERS,
        )

        if response.status_code == 500 and "Internal Server Error" in response.text:
            Actor.log.warning("There are no reviews for this hotel yet.")
            return AggregateResponse.model_validate({"reviews": None, "rating": None})

        return AggregateResponse.model_validate(response.json())

    @retry(
        rules=[
            RetryRule(
                exception=[ServerError, ConnectionError],
                new_proxy=ProxySettings(groups=["auto"], country_code="US"),
                new_impersonate=True,
                clean_cookies=True,
            ),
        ],
        max_retries=3,
    )
    async def get_reviews(self, hotel_id: str, after: str | None = None) -> ReviewsPage:
        assert self.client

        params: dict[str, str | int] = {
            "locale": LOCALE,
            "limit": PAGE_LIMIT,
            "accommodationCode": hotel_id,
            "orderBy": "TRAVEL_DATE",
        }
        if after:
            params["after"] = after

        response = await self.client.get(
            REVIEWS_URL,
            params=params,
            headers=HEADERS,
        )

        if response.status_code >= 500:
            raise ServerError("Server error occurred.")

        return ReviewsPage.model_validate(response.json())
