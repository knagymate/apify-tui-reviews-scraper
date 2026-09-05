# TUI Reviews Scraper

Scrape structured **TUI hotel reviews and rating data** with an Apify Actor built for travel analytics, hospitality intelligence, and SEO workflows.

This project collects guest review records from TUI hotel pages and returns clean JSON output with:
- review metadata (stay date, reviewer profile fields, travel season, language)
- full guest review text and title
- detailed category ratings per review (cleanliness, food & drinks, service, and more)
- hotel-level aggregated rating summary

---

## Why this scraper

- Built for **TUI review scraping** with stable hotel ID resolution from hotel URLs.
- Supports multiple hotels in one run via `startUrls`.
- Cursor-based pagination that walks the full TUI review history.
- Optional date filtering with `cutoffDate` for incremental scraping.
- Configurable cap using `maxReviewsPerHotel`.
- Can return a `summary` record even when no review passes filters (`alwaysReturnSummary`).
- Output is AI-ready and analytics-friendly for ETL pipelines.

---

## Supported TUI URLs

Use standard TUI hotel detail / offer URLs, for example:

```text
https://www.tui.com/hotel/suchen/angebote/TUI-KIDS-CLUB-Wangerland-Resort/92399/offer/
```

The Actor loads the hotel page, extracts the hotel ID, and requests review data from TUI customer-review endpoints.

---

## Input schema

| Field | Type | Required | Default | Description |
|---|---|---:|---:|---|
| `startUrls` | `array` | Yes | - | TUI hotel URLs to process |
| `maxReviewsPerHotel` | `integer` | No | `100` | Maximum number of returned review records per hotel |
| `cutoffDate` | `string` (`YYYY-MM-DD`) | No | - | Keep reviews on/after this date |
| `alwaysReturnSummary` | `boolean` | No | `true` | Push a summary record when no review record is returned |

`cutoffDate` is interpreted as a local date (Europe/Berlin assumption from input schema).

---

## Example input

```json
{
  "startUrls": [
    { "url": "https://www.tui.com/hotel/suchen/angebote/TUI-KIDS-CLUB-Wangerland-Resort/92399/offer/" }
  ],
  "maxReviewsPerHotel": 100,
  "cutoffDate": "2025-01-01",
  "alwaysReturnSummary": true
}
```

---

## Output format

The Actor stores results in the default Apify dataset.

Each item is either a `review` record or a `summary` record. Every `review` record also embeds the hotel-level `hotelSummary` for convenient joins. Output field documentation is provided in the generated output section based on `DATASET_SCHEMA`.

Rating category values are on the TUI **1–5** scale, and `recommendationRate` is a **0–100** percentage.

---

## Example output item (`recordType: review`)

```json
{
  "recordType": "review",
  "reviewId": "SV_24B0VBBEFVO7U6AR_8CVSN1JJZVQYU9Z",
  "reviewDate": "2026-08-29 00:00:00+00:00",
  "reviewerName": "Chris",
  "reviewerType": "FAMILY",
  "reviewerAgeGroup": "THIRTIES",
  "travelSeason": "SUMMER",
  "language": "de",
  "reviewTitle": "Sommerurlaub",
  "reviewText": "Hatten eine schöne Woche, würden aber nicht nochmal dort buchen.",
  "hotelRecommendation": true,
  "ratings": {
    "average": 4,
    "cleanliness": 3,
    "foodAndDrinks": 4,
    "staffService": 4,
    "childFriendliness": 4,
    "accommodationCondition": 3,
    "activityAndEntertainment": 4
  },
  "hotelSummary": {
    "hotelId": "92399",
    "startUrl": "https://www.tui.com/hotel/suchen/angebote/TUI-KIDS-CLUB-Wangerland-Resort/92399/offer/",
    "actualUrl": "https://www.tui.com/hotel/suchen/angebote/TUI-KIDS-CLUB-Wangerland-Resort/92399/offer/",
    "numberOfReviews": 187,
    "recommendationRate": 81,
    "lastReviewDate": "2026-08-30 00:00:00+00:00",
    "ratings": {
      "average": 4,
      "cleanliness": 3.7,
      "foodAndDrinks": 4.1,
      "staffService": 4.2,
      "childFriendliness": 4.5,
      "accommodationCondition": 4,
      "activityAndEntertainment": 4.4
    }
  }
}
```

---

## Example output item (`recordType: summary`)

```json
{
  "recordType": "summary",
  "hotelSummary": {
    "hotelId": "92399",
    "startUrl": "https://www.tui.com/hotel/suchen/angebote/TUI-KIDS-CLUB-Wangerland-Resort/92399/offer/",
    "actualUrl": "https://www.tui.com/hotel/suchen/angebote/TUI-KIDS-CLUB-Wangerland-Resort/92399/offer/",
    "numberOfReviews": 187,
    "recommendationRate": 81,
    "lastReviewDate": "2026-08-30 00:00:00+00:00",
    "ratings": {
      "average": 4,
      "cleanliness": 3.7,
      "foodAndDrinks": 4.1,
      "staffService": 4.2,
      "childFriendliness": 4.5,
      "accommodationCondition": 4,
      "activityAndEntertainment": 4.4
    }
  }
}
```

---

## How to use on Apify

1. Open the Actor on Apify.
2. Add one or more TUI hotel URLs to `startUrls`.
3. Optionally set `maxReviewsPerHotel` and `cutoffDate`.
4. Run the Actor and export results from the dataset.

---

If this Actor helps your workflow, a rating on Apify is appreciated.
