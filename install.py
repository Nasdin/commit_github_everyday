import os
import subprocess
from crontab import CronTab


USERNAME = subprocess.check_output('whoami', shell=True).decode('utf-8').strip('\n')
CWD = os.getcwd()
autocommit_filename = 'autocommit.py'

cron = CronTab(user=USERNAME)

job_reboot = cron.new(command=f'python {os.path.abspath(autocommit_filename)} {CWD}', comment='Make a commit everyday to fill up github profile')
job = cron.new(command=f'python {os.path.abspath(autocommit_filename)} {CWD}', comment='Make a commit everyday to fill up github profile')
job.every().hour()
job_reboot.every_reboot()

cron.write()
job.enable()

