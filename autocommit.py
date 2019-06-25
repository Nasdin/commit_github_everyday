import subprocess
import datetime

username = subprocess.check_output('whoami', shell=True).decode('utf-8').strip('\n')
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

today_date = datetime.datetime.now().date()
incrementer_file_name = f'{username}.txt'

last_run = subprocess.check_output(['tail', '-1', incrementer_file_name])
last_run_date = datetime.datetime.strptime(last_run, DATE_FORMAT)
last_run_date_no_time = last_run_date.date()

if last_run_date_no_time == today_date:
    exit()

with open(incrementer_file_name, 'w') as f:
    f.write(today_date.strftime(DATE_FORMAT))

subprocess.run(['git', 'add', '-A'])
subprocess.run('git', 'commit', '-m', f'"Autocommit from {username} on {today_date.strftime(DATE_FORMAT)}"'])
subprocess.run(['git', 'fetch'])
subprocess.run(['git', 'rebase', 'origin/master'])
subprocess.run(['git', 'push', '-f'])
