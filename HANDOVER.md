# Atlas of Ruins auto-posting: handover

Everything that posts to @atlas_of_ruins, and how to keep it running after Isabella leaves.

## How it works
1. **Approval board** (a Claude page): rows of three photos. Approve, reorder or swap them, and set the post time.
2. **Hourly sync** (a Claude scheduled task): copies the approved rows, start date and post time from the board into `queue.json` in this repository.
3. **GitHub** (this repository): every 15 minutes it checks the time; once the day's post time has passed it posts the next approved photo with its book caption, then records it in `posted.json`. It never posts twice in one day.

## Who owns what
| Piece | Lives in | Must belong to the company |
|---|---|---|
| Instagram account | @atlas_of_ruins | already company |
| Posting key (`IG_ACCESS_TOKEN`) | GitHub > Settings > Secrets | system-user key, never expires |
| Meta app "Atlas autopost" | Reuse Italy business portfolio | add the boss with Full control |
| This repository + images | GitHub account `reuse-italy` | change login email to a company address |
| Approval board + hourly sync | Claude | move to a company Claude account (below) |

## Moving the board and the sync to a company Claude account
Sign in to claude.ai with the company account, connect GitHub (Settings > Connectors > GitHub, allow `atlas-autopost`), start a new chat and paste this:

> Rebuild the Atlas of Ruins approval board from the GitHub repository reuse-italy/atlas-autopost, folder `board-backup`. Publish `board-backup/index.html` as an artifact with the `db` and `user` capabilities, together with every file in `board-backup/img` (publish them in batches of 200 or fewer at the same paths). Then load the saved data from `board-backup/data` into the new board's database: each JSON file is one document, at collection = its folder (`groups`, `plan`, `settings`, `status`) and document id = its file name. Then create an hourly scheduled task that does what `SYNC_TASK.md` in the repository describes, using the new board's link. Share the board with the people who approve posts as Editors, with link sharing turned off.

The backup in `board-backup/data` is a snapshot; ask Claude in the old board's chat for a fresh export just before switching, or rebuild from the latest copy if the old one is gone.

## If something stops
- **Nothing posted today:** GitHub > Actions tab. A red run shows the reason. "Not yet" means the post time has not come; "Nothing approved is waiting" means approve more rows.
- **Approvals not reaching GitHub:** the hourly sync is not running. Check the scheduled task in the Claude account that owns it.
- **Post now by hand:** Actions > Daily Instagram post > Run workflow.
