import subprocess
from crontab import CronTab


USERNAME = subprocess.check_output('whoami', shell=True).decode('utf-8').strip('\n')

cron = CronTab(user=USERNAME)
cron.remove_all(comment='Make a commit everyday to fill up github profile')

cron.write()

