from datetime import datetime

import arrow
from apify_common.actor import CommonActor

from src.models import (
    ActorInput,
    ActorOutput,
    AggregateResponse,
    HotelSummary,
    ReviewItem,
    ReviewRatings,
    ScoreItem,
)
from src.parser import parse_hotel_id_from_html
from src.requests import Client

SCORE_KEY_MAP = {
    "CLEANLINESS": "cleanliness",
    "FOOD_AND_DRINKS": "foodAndDrinks",
    "STAFF_SERVICE": "staffService",
    "CHILD_FRIENDLINESS": "childFriendliness",
    "ACCOMMODATION_CONDITION": "accommodationCondition",
    "ACTIVITY_AND_ENTERTAINMENT": "activityAndEntertainment",
}


def build_ratings(
    scores: list[ScoreItem], average: float | None = None
) -> ReviewRatings:
    values: dict[str, float | None] = {field: None for field in SCORE_KEY_MAP.values()}
    for score in scores:
        field = SCORE_KEY_MAP.get(score.key)
        if field:
            values[field] = score.value

    return ReviewRatings(average=average, **values)


def build_hotel_summary(
    hotel_id: str,
    start_url: str,
    actual_url: str,
    aggregate: AggregateResponse,
) -> HotelSummary:
    rating = aggregate.rating
    number_of_reviews = aggregate.reviews.noOfReviews if aggregate.reviews else None

    if not rating:
        return HotelSummary(
            hotelId=hotel_id,
            startUrl=start_url,
            actualUrl=actual_url,
            numberOfReviews=number_of_reviews,
        )

    return HotelSummary(
        hotelId=hotel_id,
        startUrl=start_url,
        actualUrl=actual_url,
        numberOfReviews=number_of_reviews,
        recommendationRate=rating.recommended.value if rating.recommended else None,
        lastReviewDate=rating.lastReviewDate,
        ratings=build_ratings(
            rating.scores,
            rating.overallExperience.value if rating.overallExperience else None,
        ),
    )


class Actor(CommonActor):
    async def scrape_url(
        self,
        client: Client,
        start_url: str,
        always_return_summary: bool = True,
        max_reviews: int | None = None,
        cutoff_date: datetime | None = None,
    ) -> None:
        self.log.info(f"Scraping URL: {start_url}")
        html, actual_url = await client.get_start_url(start_url)
        hotel_id = parse_hotel_id_from_html(html)
        if not hotel_id:
            self.log.warning(f"No hotel id found for {start_url}")
            return
        else:
            self.log.info(f"Found hotel id: {hotel_id}")

        aggregate = await client.get_aggregate(hotel_id)
        hotel_summary = build_hotel_summary(hotel_id, start_url, actual_url, aggregate)

        reviews_page = aggregate.reviews
        if not reviews_page or not reviews_page.items:
            self.log.info(f"No reviews found for hotel id: {hotel_id}")
            if always_return_summary:
                await self.push_data(
                    ActorOutput(
                        recordType="summary",
                        hotelSummary=hotel_summary,
                    ).model_dump()
                )
            return

        self.log.info(
            f"Found {reviews_page.noOfReviews} reviews for hotel id: {hotel_id}"
        )

        returned_single_results: int = 0

        while True:
            for item in reviews_page.items:
                if (
                    cutoff_date
                    and item.travelDate
                    and arrow.get(item.travelDate) < arrow.get(cutoff_date)
                ):
                    self.log.info(
                        f"Review date {item.travelDate} is before cutoff date "
                        f"{cutoff_date}, ending."
                    )
                    if always_return_summary and returned_single_results == 0:
                        self.log.info(
                            f"No reviews returned for hotel id: {hotel_id}, "
                            "pushing summary only."
                        )
                        await self.push_data(
                            ActorOutput(
                                recordType="summary",
                                hotelSummary=hotel_summary,
                            ).model_dump()
                        )
                    return

                await self.push_data(
                    self._build_review_output(item, hotel_summary).model_dump()
                )

                returned_single_results += 1
                self.returned_results += 1

                if max_reviews and returned_single_results >= max_reviews:
                    self.log.info(
                        f"Reached max reviews per hotel: {max_reviews} for {start_url}"
                    )
                    return

            if (
                not reviews_page.pageInfo.hasNextPage
                or not reviews_page.pageInfo.endCursor
            ):
                break

            reviews_page = await client.get_reviews(
                hotel_id=hotel_id, after=reviews_page.pageInfo.endCursor
            )

    @staticmethod
    def _build_review_output(
        item: ReviewItem, hotel_summary: HotelSummary
    ) -> ActorOutput:
        return ActorOutput(
            recordType="review",
            reviewId=item.id,
            reviewDate=item.travelDate,
            reviewerName=item.contributor,
            reviewerType=item.travelParty.key if item.travelParty else None,
            reviewerAgeGroup=item.ageGroup.key if item.ageGroup else None,
            travelSeason=item.travelSeason.key if item.travelSeason else None,
            language=item.language,
            reviewTitle=item.header,
            reviewText=item.review,
            hotelRecommendation=item.recommended,
            ratings=build_ratings(item.scores, item.overallExperience),
            hotelSummary=hotel_summary,
        )

    async def main_logic(self):
        actor_input: ActorInput = ActorInput.model_validate(await self.get_input())
        max_reviews_per_hotel = actor_input.maxReviewsPerHotel
        cutoff_date = actor_input.cutoffDate
        always_return_summary = actor_input.alwaysReturnSummary

        if max_reviews_per_hotel:
            self.log.info(f"Max reviews to fetch: {max_reviews_per_hotel}")
        if cutoff_date:
            self.log.info(f"Cutoff date is set to {cutoff_date}.")

        async with Client(
            impersonate="firefox",
            with_session=True,
            with_cassette=True,
        ) as client:
            for url in actor_input.startUrls:
                await self.scrape_url(
                    client,
                    url.url,
                    always_return_summary,
                    max_reviews_per_hotel,
                    cutoff_date,
                )


async def main():
    async with Actor() as actor:
        await actor.run()
