from discord_webhook import DiscordWebhook
from time import sleep
from datetime import timedelta, datetime
import requests
from discord_timestamps import format_timestamp, TimestampType

# set webhook url here
webhookurl = 'https://discord.com/api/webhooks/...'

# the uuid for your worker
workerid = ''
#workerid = '351064fc-f360-4910-85f7-7f2f41b5c201' # an offline worker for testing
#workerid = 'a68c78f2-3303-4b68-b4a2-586183ce7e24' # an online (probably) worker for testing

# your userid (not your api key, not your full username, just the numbers)
# the example can be used to test the script with a relatively short time (I picked a user on page 3)
horde_userid = 7218

# your discord userid, used to ping you. if you dont have dev mode on, ping yourself, add \ before the @
discord_userid = 215...

# recommend not increasing this more, im not doing any async here...
leaderboard_pages_to_fetch = 100

# approximately every 3 hours update leaderboard (counter for number of worker updates before updating userinfo)
leaderboard_interval = 36

# I wont be updating this, so you'll have to add your own contact info here
headers={'Client-Agent':'unmaintained-webhook:0:efreak@Discord'}


pos = "Unknown"
userts = ""
since_leaderboard = leaderboard_interval
username = ""
oldpos = False
oldts = False
firstrun = True
userinfo = ""
webhook = DiscordWebhook(url=webhookurl, content="fetching data...")
webhook.execute()
while firstrun or sleep(300):
    firstrun = False
    response = requests.get("https://aihorde.net/api/v2/workers/"+workerid,headers=headers)
    data = response.json()
    if data['maintenance_mode'] or not data['online']:
        status = "🔴 "
        if not data['online']:
            status += "OFFLINE!  "
        if data['maintenance_mode']:
            status += "Maintenance"
        badwebhook = DiscordWebhook(url=webhookurl, content=f"<@{discord_userid}>\n{status}")
        badwebhook.execute()
    else: status = "🟢 Online"
    content = f"""
[{data['name']}](https://aihorde.net/api/v2/workers/{workerid}):
- **Status**: {status}
- **Uptime**: {timedelta(data['uptime'])}
- **Uncompleted Jobs**: {data['uncompleted_jobs']}
- **Requests Completed**: {data['requests_fulfilled']}
- **Kudos**: {data['kudos_rewards']} ({data['kudos_details']['generated']} generation, {data['kudos_details']['uptime']} uptime)
- **Performance**: {data['performance']}
*Updated: {format_timestamp(datetime.utcnow().timestamp(),TimestampType.RELATIVE)}*"""
    webhook.content = content + '\n\nNo userinfo yet...'
    webhook.edit()
    since_leaderboard += 1
    if since_leaderboard > leaderboard_interval:
        print("Fetching leaderboard...")
        since_leaderboard = 0
        page=0
        newpos = 0
        loop = True
        while page < leaderboard_pages_to_fetch:
            page += 1
            url = f"https://aihorde.net/api/v2/users?page={page}"
            print(f"fetching {url}")
            webhook.content = content + f"\n\nUserinfo not found yet\nNow checking page {page}"
            webhook.edit()
            users = requests.get(url,headers=headers).json()
            for user in users:
                newpos += 1
                if user['id'] == horde_userid:
                    print(f"FOUND: {user['id']}: {user['username']} AT {newpos}")
                    loop = False
                    oldpos = pos
                    oldts = userts
                    userinfo = user
                    userts = format_timestamp(datetime.utcnow().timestamp(),TimestampType.RELATIVE)
                    pos = newpos
                    break
            if not loop:
                break
            sleep(3)
    if pos and userts:
        print("pos found")
        content += f"""

Details for [{userinfo['username']}](https://aihorde.net/api/v2/users/{horde_userid}):
- **Kudos**: {userinfo['kudos']}
- **Leaderboard Position**: {pos}
- **Workers**: {userinfo['worker_count']}
- **Trusted**: {userinfo['trusted']}
- **Account Created**: {format_timestamp(datetime.utcnow().timestamp() - userinfo['account_age'], TimestampType.RELATIVE)}
"""
        if oldpos and oldts:
            print("oldpos found")
            content += f"- **Previous Position**: {oldpos} {oldts})"
        content += f"\n\n*Updated: {format_timestamp(datetime.utcnow().timestamp(),TimestampType.RELATIVE)}*"
    else: content += f"\n\n*User not found. Leaderboard position unavailable*."
    print("done")
    webhook.content = content
    webhook.edit()
