# Discord Webhook for AI Horde Worker

Updates status every 5 minutes, checks info for an ai horde text worker.

Limitations:
- leaderboard only checks the first 50 pahes of API for time reasons.
- currently only works for text workers.
- Efreak will *not* maintain this. They wrote it for me and I should be the one contacted with issues.
- timers are not exact, because there's no async going on here; it'll update a little over every 5 minutes, and update the keyboard every 36 updates (actually every 3 hours; this is configurable)

## Requirements:
- discord-webhook
- discord-timestamps

discord-timestamps is probably unnecessary in retrospect, not it's a *very* lightweight dependency with only one unnecessary subdependency (Arrow).

## Usage
1. `pip install -r requirements.txt`
2. edit webhook.py to update configuration
3. `python webhook.py`

## TODO:
- bianary search

## License
[![WTFPL](http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl.svg)](http://www.wtfpl.net)
