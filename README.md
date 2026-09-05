# TUI Reviews Scraper

Scrape **TUI hotel reviews** at scale with a fast, reliable, and production-ready Apify Actor.

Extract structured **TUI customer review data** including:
- ⭐ Guest ratings with detailed category scores
- 📝 Review titles & full guest comments
- 👤 Reviewer names, traveler types & age groups
- 🏨 Hotel summary with aggregated ratings
- 🔢 Total review count per hotel
- 🌐 Review language, travel season & recommendation status
- ✅ TUI recommendation rate and last review date

Perfect for:
- Travel & hospitality businesses
- Hotel content and landing page teams
- AI/LLM training datasets
- Reputation management platforms
- Market research & competitive analysis
- Customer experience analysis

Optimized for large-scale review extraction from **TUI.com**, one of Europe's leading travel, hotel, and package holiday platforms.

---

# ✨ Features

- ✅ Scrape **TUI.com hotel reviews** from TUI hotel detail and offer pages
- ✅ Extract guest ratings with category-level scores
- ✅ Capture review dates, traveler type, age group, travel season & language
- ✅ Extract full guest comments, review titles & reviewer names
- ✅ Detailed category ratings (cleanliness, food & drinks, staff service, child friendliness, accommodation condition, activity & entertainment)
- ✅ Aggregated hotel rating summary
- ✅ Review count statistics per hotel
- ✅ TUI recommendation rate per hotel
- ✅ Last review date for freshness checks
- ✅ Multiple TUI hotel URLs in a single run
- ✅ Optional cutoff date filtering
- ✅ Configurable maximum reviews per hotel
- ✅ Cursor-based pagination through review history
- ✅ Apify API ready
- ✅ Webhook & workflow integrations (Make, Zapier, Google Sheets, BigQuery)

---

# 🔍 Supported TUI Hotel Pages

The scraper works with standard **TUI.com hotel detail / offer pages**. Simply provide the hotel URL, and the Actor extracts all available reviews.

Example URLs:
```text
https://www.tui.com/hotel/suchen/angebote/TUI-KIDS-CLUB-Wangerland-Resort/92399/offer/?startDate=2026-09-08&endDate=2026-12-07&duration=default&travellers=2&searchScope=PACKAGE&showTotalPrice=0&earlyBird=0&sortOffersAsc=1&sortOffersField=campaignOffers
https://www.tui.com/hotel/suchen/angebote/Hotel-Grupotel-Taurus-Park/3496/offer/?searchScope=HOTEL&startDate=2026-09-06&endDate=2026-12-05&duration=7-&travellers=2&destinations=133|REGION&productId=PMI43003&boardCode=G&supplierRoomId=DZX1&productAccommodationUnitId=DZX1G&finalPosition=1&rateType=STANDARD&selectedDuration=7&selectedStartDate=2026-11-15
https://www.tui.com/pauschalreisen/suchen/angebote/TUI-KIDS-CLUB-JAZ-Bluemarine/229480/offer/?startDate=2026-09-06&endDate=2027-04-30&duration=7-&travellers=2&searchScope=PACKAGE&showTotalPrice=0&regionGiataIds=651&contentid=1_ad1_3_aegypten_20260817
```

The Actor automatically detects the TUI hotel ID from the page, resolves the final URL, then collects review data from TUI customer-review endpoints.

---

# ⚙️ Input Configuration

| Field | Type | Description |
|---|---|---|
| `startUrls` | array | One or more TUI.com hotel URLs |
| `maxReviewsPerHotel` | integer | Maximum reviews to scrape per hotel (default: `100`) |
| `cutoffDate` | date | Return only reviews from this date onwards (format: `YYYY-MM-DD`) |
| `alwaysReturnSummary` | boolean | Include hotel summary even if no reviews found (default: `true`) |

---

# 📥 Example Input

```json
{
  "startUrls": [
    {
      "url": "https://www.tui.com/hotel/suchen/angebote/TUI-KIDS-CLUB-Wangerland-Resort/92399/offer/?startDate=2026-09-08&endDate=2026-12-07&duration=default&travellers=2&searchScope=PACKAGE&showTotalPrice=0&earlyBird=0&sortOffersAsc=1&sortOffersField=campaignOffers"
    },
    {
      "url": "https://www.tui.com/hotel/suchen/angebote/Hotel-Grupotel-Taurus-Park/3496/offer/?searchScope=HOTEL&startDate=2026-09-06&endDate=2026-12-05&duration=7-&travellers=2&destinations=133|REGION&productId=PMI43003&boardCode=G&supplierRoomId=DZX1&productAccommodationUnitId=DZX1G&finalPosition=1&rateType=STANDARD&selectedDuration=7&selectedStartDate=2026-11-15"
    },
    {
      "url": "https://www.tui.com/pauschalreisen/suchen/angebote/TUI-KIDS-CLUB-JAZ-Bluemarine/229480/offer/?startDate=2026-09-06&endDate=2027-04-30&duration=7-&travellers=2&searchScope=PACKAGE&showTotalPrice=0&regionGiataIds=651&contentid=1_ad1_3_aegypten_20260817"
    }
  ],
  "maxReviewsPerHotel": 1000
}
```

---

# 📦 Output Dataset

For every review, the Actor returns a clean, structured record that combines the **individual TUI hotel review**, its **category ratings**, traveler metadata, recommendation status, and an **aggregated hotel summary** — making downstream processing simple and scalable.

---

# 🧾 Output Fields

| Field | Description |
|---|---|
| `recordType` | Type of record: `review` or `summary` |
| `reviewId` | TUI internal review ID |
| `reviewDate` | Date associated with the guest review |
| `reviewerName` | Guest's display name |
| `reviewerType` | Traveler type / travel party, such as family or couple |
| `reviewerAgeGroup` | Reviewer's age group |
| `travelSeason` | Season of travel, such as summer or winter |
| `language` | Review language code |
| `reviewTitle` | Review headline written by the guest |
| `reviewText` | Full review text written by the guest |
| `hotelRecommendation` | Whether the guest recommends the hotel |
| `ratings.average` | Overall review rating |
| `ratings.cleanliness` | Cleanliness rating |
| `ratings.foodAndDrinks` | Food & drinks rating |
| `ratings.staffService` | Staff service rating |
| `ratings.childFriendliness` | Child friendliness rating |
| `ratings.accommodationCondition` | Accommodation condition rating |
| `ratings.activityAndEntertainment` | Activity & entertainment rating |
| `hotelSummary.hotelId` | TUI internal hotel ID |
| `hotelSummary.startUrl` | Original input URL |
| `hotelSummary.actualUrl` | Final resolved hotel URL |
| `hotelSummary.numberOfReviews` | Total reviews available for the hotel |
| `hotelSummary.recommendationRate` | Percentage of guests recommending the hotel |
| `hotelSummary.lastReviewDate` | Latest available review date |
| `hotelSummary.ratings.average` | Average overall hotel rating |
| `hotelSummary.ratings.cleanliness` | Average cleanliness rating |
| `hotelSummary.ratings.foodAndDrinks` | Average food & drinks rating |
| `hotelSummary.ratings.staffService` | Average staff service rating |
| `hotelSummary.ratings.childFriendliness` | Average child friendliness rating |
| `hotelSummary.ratings.accommodationCondition` | Average accommodation condition rating |
| `hotelSummary.ratings.activityAndEntertainment` | Average activity & entertainment rating |

---

# 🏨 Example Review Output

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

Example summary record:
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

> ℹ️ TUI uses a **1–5 rating scale** for review and hotel rating categories. `recommendationRate` is returned as a **0–100 percentage**.

---

# 🌍 Ideal Use Cases

Perfect for:
- **Hotel reputation monitoring** — Track guest satisfaction trends across TUI hotels and resorts
- **Travel content teams** — Build review-based destination pages, hotel comparisons & FAQ content
- **AI/LLM training** — Create travel and hospitality datasets for chatbots, recommendation engines & summarization
- **Sentiment analysis** — Analyze TUI guest feedback by language, traveler type, age group and travel season
- **Market intelligence** — Benchmark hotels, resorts and package holiday properties against competitors
- **Revenue management** — Correlate guest ratings, recommendation rates and review freshness with pricing decisions
- **OTA integration** — Aggregate TUI hotel reviews for metasearch, booking platforms and travel dashboards
- **Reputation management platforms** — Monitor guest concerns, positive mentions and recommendation patterns
- **Hospitality analytics** — Build dashboards for hotel groups, tour operators and travel agencies
- **Customer experience research** — Deep-dive analysis of cleanliness, food, service, family friendliness and entertainment feedback

---

# 🚀 Integrations

**Platforms:**
- Apify API & Console
- Python (`apify-client`)
- Node.js
- JavaScript (Puppeteer)
- Go
- Java

**Workflows:**
- Make.com (Zapier alternative)
- Zapier
- Google Sheets
- Airtable
- Slack
- Discord webhooks
- Custom webhooks

**Data Warehouses:**
- Google BigQuery
- Snowflake
- Amazon Redshift
- AWS S3
- Azure Data Lake
- Airbyte

**AI/ML:**
- LangChain
- OpenAI/GPT
- Hugging Face
- Custom transformers

**Export Formats:**
- JSON (default)
- CSV
- Excel
- XML
- Parquet

---

# ⚡ Reliability & Performance

**Technical Stack:**
- Python 3.12+ (async-first)
- Smart pagination & request handling
- Automatic retry logic with backoff
- Session management & cookies
- Proxy support (rotating, static, residential)
- Concurrent requests with rate limiting
- Error handling & recovery

**Optimized for:**
- Stable production workloads
- Large-scale TUI review extraction
- Multi-hotel review aggregation
- High-throughput data collection
- Memory-efficient dataset output
- Scheduled runs & webhooks

---

# 📊 Data Quality

**Included Features:**
- ✅ TUI hotel ID detection from hotel pages
- ✅ Final URL resolution for traceable datasets
- ✅ Date validation & normalization
- ✅ Recommendation status capture
- ✅ Traveler profile metadata
- ✅ Rating scale validation
- ✅ Category score normalization
- ✅ Structured summary records

---

# 👨‍💻 About the Author

Created by **[knagymate](https://apify.com/knagymate)** — specialized in high-performance Apify Actors for:
- Hotel & travel review scraping
- Search-friendly structured datasets
- AI-ready structured data
- Production-grade integrations

**Need custom solutions?**
- Enterprise scraping setups
- Private Actor modifications
- Custom integrations & webhooks
- Data pipeline optimization

👉 Contact via Apify marketplace.

---

# ⭐ Support & Feedback

If this Actor helps your project:
- ⭐ **Star** this repository (GitHub)
- 💬 **Leave a review** on the Apify marketplace
- 📧 **Report issues** or request features

Your feedback helps improve this tool for the community!
