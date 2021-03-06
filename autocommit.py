import datetime
import os
import subprocess


DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
LOG_FOLDER = 'logs'
TODAY_DATE = datetime.datetime.now().date()

if __name__ == '__main__':
    import argparse

    cwd = os.getcwd()

    parser = argparse.ArgumentParser(description="Get the working directory of where the repo was cloned into")
    parser.add_argument('cwd', type=str, nargs='?', const=cwd)
    args = parser.parse_args()

    cwd = args.cwd if args.cwd is not None else cwd
    os.chdir(cwd)

    try:
        os.mkdir(LOG_FOLDER)
    except:
        pass

    if os.name != 'nt':
        username = subprocess.check_output('whoami', shell=True).decode('utf-8').strip('\n')
    else:
        proc = subprocess.Popen(['powershell.exe',
                                 '$(Get-WMIObject -class Win32_ComputerSystem | select username).username'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate(timeout=120)
        username = out.decode('utf-8').split('\\')[-1].strip()

    incrementer_file_name = f'{username}.txt'
    incrementer_file_name = os.path.join(LOG_FOLDER, incrementer_file_name)
    new_user = False
    try:
        if os.name != 'nt':
            last_run = subprocess.check_output(['tail', '-1', incrementer_file_name])
        else:
            proc = subprocess.Popen(['powershell.exe', f'Get-Content -tail 1 {incrementer_file_name}'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            last_run, err = proc.communicate(timeout=120)
            if proc.returncode != 0:
                new_user = True
    except:
        new_user = True
    if not new_user:
        last_run_date = datetime.datetime.strptime(last_run.decode('utf-8').strip(), DATE_FORMAT)
        last_run_date_no_time = last_run_date.date()

        if last_run_date_no_time == TODAY_DATE:
            exit()

    with open(incrementer_file_name, 'a') as f:
        f.write(f'\n{TODAY_DATE.strftime(DATE_FORMAT)}')

    subprocess.run(['git', 'add', '-A'])
    subprocess.run(['git', 'commit', '-m', f'"Autocommit from {username} on {TODAY_DATE.strftime(DATE_FORMAT)}"'])
    subprocess.run(['git', 'fetch'])
    subprocess.run(['git', 'rebase', 'origin/master'])
    subprocess.run(['git', 'push', '-f'])
