Set up the Atlas of Ruins Instagram posting system on my Claude account. Everything you need is in the GitHub repository reuse-italy/atlas-autopost, folder "board".

1. Attach and clone the repository reuse-italy/atlas-autopost (read access is enough for this step).
2. Publish board/index.html as a new artifact, together with every image in board/img/ (publish them as files at the paths img/<name>.jpg, in two publishes if there are more than 255). Declare the capabilities db and user. Title: Atlas of Ruins Queue.
3. Fill the new artifact's database. If I can open the old board at https://claude.ai/artifact/MyeiMoxtkVsf2tXj9UXv6j, copy every document from it (collections plan, settings, status, groups) so the data is current. Otherwise load board/board-data.json, where each key is "<collection>/<doc id>" and each value is the document.
4. Create a scheduled task named "Atlas of Ruins queue sync" that runs every hour, using the instructions in board/SYNC_TASK.md with BOARD_URL replaced by the new artifact's link.
5. Open the new board for me and tell me its link.
