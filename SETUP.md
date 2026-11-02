# Atlas of Ruins auto-poster: one-time setup (about 1 hour)

Do this once. After that the boss approves rows on the approval board and the
photos post themselves, one a day at 18:00 Rome time. Nobody else touches it.

How it works: every afternoon Claude copies the approved rows from the board into
this GitHub folder. Every evening GitHub posts the next approved photo to Instagram
and records it, and the board shows it as "Posted".

## You need
- @atlas_of_ruins switched to a Professional account (Business or Creator) and linked
  to a Facebook Page. In the Instagram app: Settings > Account type and tools.
- A free GitHub account (github.com).
- A free Meta for Developers account (developers.facebook.com), signed in with the
  Facebook profile that manages the Page.

## Step 1. Put this folder on GitHub
1. On github.com click **New repository**. Name it exactly `atlas-autopost`.
   Choose **Public** (Instagram has to be able to fetch the images). Click Create.
2. Click **uploading an existing file**. Drag in everything in this folder:
   the `posts` folder, `.github` folder, `post_next.py`, `queue.json`, `posted.json`,
   `captions.json`. Click **Commit changes**.
   Tip: on a Mac the `.github` folder is hidden. Press Cmd+Shift+. in Finder to show it.

## Step 2. Connect GitHub to Claude
In claude.ai: **Settings > Connectors > GitHub > Connect**, and allow access to
`atlas-autopost`. This lets the daily sync update the queue.

## Step 3. Get the two Instagram keys
1. developers.facebook.com > **My Apps > Create App** > use case **Other** > type **Business**.
2. In the app, add the product **Instagram** (API setup with Facebook login).
3. Open **Tools > Graph API Explorer**. Choose your app, click **Generate Access Token**,
   and tick `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
   `pages_read_engagement`, `business_management`. Approve the pop-up.
4. In the Explorer, type `me/accounts?fields=instagram_business_account` and press **Submit**.
   The number under `instagram_business_account` > `id` is your **IG_USER_ID**.
5. For a key that never expires: business.facebook.com > **Settings > Users > System users** >
   **Add** (role Admin). Assign it the app and the Page (full control), then **Generate new token**
   with the same permissions and expiry **Never**. That is your **IG_ACCESS_TOKEN**.

## Step 4. Give the keys to GitHub
In the repository: **Settings > Secrets and variables > Actions > New repository secret**.
Add `IG_USER_ID` and `IG_ACCESS_TOKEN`.

## Step 5. Test
Approve one row on the board. The next afternoon the queue updates on its own.
To test straight away: Actions tab > **Daily Instagram post** > **Run workflow**.
If something is due, it appears on Instagram within a minute.

That's it. From now on only the board is used.
