# Render deployment

1. Push this folder to a GitHub repository with `render.yaml` at the repository root.
2. In Render, choose **New → Blueprint**, select the repository, and apply the Blueprint.
3. The Blueprint creates one Python web service and one Render Postgres database. `DATABASE_URL` is injected from the database connection string. Render documents this `fromDatabase` pattern in its Blueprint reference.
4. After deployment, open the web service URL and check `/health`.
5. The UI and API are same-origin, so no CORS configuration is needed.

## Demo test
- Create a brand, e.g. Nike.
- Set official social to `nike`, official app to `Nike`, official publisher to `Nike, Inc.`.
- Add a candidate named `Nike Support` with an unknown publisher.
- Run scan and confirm a HIGH/CRITICAL result with evidence.
- Test the Google Play adapter with a public `play.google.com/store/apps/details?id=...` URL.
- Test the social adapter with a public profile URL from Instagram, X/Twitter, LinkedIn, Facebook, or TikTok. Some platforms may block automated public-page requests; the app returns the fetch error rather than bypassing platform controls.
