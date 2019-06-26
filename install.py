import os
import subprocess
from crontab import CronTab

USERNAME = subprocess.check_output('whoami', shell=True).decode('utf-8').strip('\n')
CWD = os.getcwd()
autocommit_filename = 'autocommit.py'
autocommit_filepath = os.path.abspath(os.path.join(CWD, autocommit_filename))

cron = CronTab(user=USERNAME)

job_reboot = cron.new(command=f'python {autocommit_filepath} {CWD}', comment='Make a commit everyday to fill up github profile')
job = cron.new(command=f'python {autocommit_filepath} {CWD}', comment='Make a commit everyday to fill up github profile')
job.minute.every(1)
job_reboot.every_reboot()

cron.write()
job.enable()

