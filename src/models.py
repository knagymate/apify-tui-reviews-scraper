from datetime import date, datetime
from typing import Literal

import arrow
from pydantic import BaseModel, validator


class Url(BaseModel):
    url: str


class ActorInput(BaseModel):
    startUrls: list[Url]
    cutoffDate: datetime | None = None
    maxReviewsPerHotel: int | None = 100
    alwaysReturnSummary: bool = True

    @validator("cutoffDate", pre=True, always=True)
    def set_cutoff_date(cls, raw_date: str) -> date | None:
        return arrow.get(raw_date).date() if raw_date else None


# --- TUI API response models ---


class LabeledKey(BaseModel):
    key: str | None = None
    label: str | None = None


class LabeledValue(BaseModel):
    label: str | None = None
    value: float | None = None


class ScoreItem(BaseModel):
    key: str
    label: str | None = None
    value: float | None = None


class ReviewItem(BaseModel):
    id: str
    travelDate: datetime | None = None
    travelParty: LabeledKey | None = None
    travelSeason: LabeledKey | None = None
    ageGroup: LabeledKey | None = None
    contributor: str | None = None
    language: str | None = None
    header: str | None = None
    recommended: bool | None = None
    overallExperience: float | None = None
    review: str | None = None
    scores: list[ScoreItem] = []


class PageInfo(BaseModel):
    endCursor: str | None = None
    hasNextPage: bool = False
    hasPreviousPage: bool = False
    startCursor: str | None = None


class ReviewsPage(BaseModel):
    noOfReviews: int | None = None
    items: list[ReviewItem] = []
    pageInfo: PageInfo = PageInfo()


class AggregateRating(BaseModel):
    accommodationCode: str | None = None
    lastReviewDate: datetime | None = None
    overallExperience: LabeledValue | None = None
    recommended: LabeledValue | None = None
    scores: list[ScoreItem] = []


class AggregateResponse(BaseModel):
    rating: AggregateRating | None = None
    reviews: ReviewsPage | None = None


# --- Actor output models ---


class ReviewRatings(BaseModel):
    average: float | None = None
    cleanliness: float | None = None
    foodAndDrinks: float | None = None
    staffService: float | None = None
    childFriendliness: float | None = None
    accommodationCondition: float | None = None
    activityAndEntertainment: float | None = None


class HotelSummary(BaseModel):
    hotelId: str | None = None
    startUrl: str | None = None
    actualUrl: str | None = None
    numberOfReviews: int | None = None
    recommendationRate: float | None = None
    lastReviewDate: datetime | None = None
    ratings: ReviewRatings | None = None


class ActorOutput(BaseModel):
    recordType: Literal["review", "summary"]
    reviewId: str | None = None
    reviewDate: datetime | None = None
    reviewerName: str | None = None
    reviewerType: str | None = None
    reviewerAgeGroup: str | None = None
    travelSeason: str | None = None
    language: str | None = None
    reviewTitle: str | None = None
    reviewText: str | None = None
    hotelRecommendation: bool | None = None
    ratings: ReviewRatings | None = None
    hotelSummary: HotelSummary | None = None
