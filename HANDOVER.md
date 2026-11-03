# Atlas of Ruins posting: handover

Everything that posts to @atlas_of_ruins lives in this GitHub repository, except two
pieces that live on a Claude account: the approval board and the hourly sync.
These steps move those two pieces to the new owner's Claude account.

## What runs where
| Piece | Where it lives | Owner after handover |
|---|---|---|
| Images, captions, posting program, daily schedule | GitHub `reuse-italy/atlas-autopost` | Company GitHub login |
| Instagram key | GitHub secret `IG_ACCESS_TOKEN` (never expires) | Stays in GitHub |
| Meta app "Atlas autopost" | Business portfolio "Reuse Italy" | Admins of that portfolio |
| Approval board | Claude artifact | New owner's Claude account |
| Hourly sync (board → GitHub) | Claude scheduled task | New owner's Claude account |

## Steps for the new owner (about 20 minutes)
1. **GitHub login.** Get the `reuse-italy` GitHub password from Isabella. Change the
   password and the account email to your own (github.com > Settings).
2. **Connect GitHub to Claude.** In claude.ai: Settings > Connectors > GitHub > Connect,
   signed in as `reuse-italy`, and allow the repository `atlas-autopost`.
   If Claude later says it cannot push, install the Claude GitHub app on the repository:
   https://github.com/apps/claude/installations/select_target
3. **Recreate the board and sync.** Start a new chat in Claude and paste the text in
   `board/SETUP_PROMPT.md`. Claude publishes your own copy of the board, copies over all
   approvals and order, and sets up the hourly sync. Check the new board shows the same rows.
4. **Meta.** Accept the invite to the "Reuse Italy" business portfolio with full control
   (business.facebook.com). Isabella sends it.
5. **Tell Isabella it works.** She then deletes her sync task so only yours runs, and
   removes her copy of the board.

## Day to day
- Approve, reorder or swap rows on the board. Changes reach GitHub within an hour.
- Posts go up once a day at the time set on the board (default 11:00 Rome time).
- If a post fails, GitHub emails the account owner and the same photo is tried again
  at the next check.
