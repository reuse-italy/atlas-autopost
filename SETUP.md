# Atlas of Ruins auto-poster: one-time setup (about 1 hour)

Do this once. After that the boss approves rows on the approval board and the
photos post themselves, one a day at 18:00 Rome time. Nobody else touches it.

How it works: every afternoon Claude copies the approved rows from the board into
this GitHub folder. Every evening GitHub posts the next approved photo to Instagram
and records it, and the board shows it as "Posted".

## You need
- @atlas_of_ruins switched to a Professional account (Business or Creator).
  In the Instagram app: Settings > Account type and tools. No Facebook Page is needed.
- A Meta for Developers account (developers.facebook.com).

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

## Step 3. Get the Instagram key
1. developers.facebook.com > **My Apps > Create App**. Name it "Atlas autopost".
2. For the use case pick **Manage messaging & content on Instagram**. Finish creating the app.
3. In the app, open **Instagram > API setup with Instagram login**.
4. Under **Generate access tokens**, click **Add account** and log in as @atlas_of_ruins.
5. Click **Generate token** next to the account and copy the long code. That is your **IG_ACCESS_TOKEN**.
   The poster refreshes this key every day, so it does not expire while posting runs.

## Step 4. Give the key to GitHub
In the repository: **Settings > Secrets and variables > Actions > New repository secret**.
Name it `IG_ACCESS_TOKEN` and paste the code.

## Step 5. Test
Approve one row on the board. The next afternoon the queue updates on its own.
To test straight away: Actions tab > **Daily Instagram post** > **Run workflow**.
If something is due, it appears on Instagram within a minute.

That's it. From now on only the board is used.
