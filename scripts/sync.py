import subprocess
import time

branchnames = 'test_branches.txt'

def init():
    subprocess.call(['./init  >/dev/null 2>&1'], shell=True)
    time.sleep(5)

def check_diff():
    with open(branchnames) as branch_list:
        branches = branch_list.readlines()

    flag = 0
    for branch in branches:
        current = branch.rstrip()
        p = subprocess.Popen(['git','diff','--diff-filter=(M|A|D)', 'origin/' + current, current], stdout=subprocess.PIPE)
        difference = p.communicate()[0]
        if difference:
            reconcile_diff(current)
            flag = 1
    if flag == 0:
        print 'No new updates'


def reconcile_diff(branch):
    subprocess.call(['git checkout '+branch], shell=True)
    time.sleep(5)
    subprocess.call(['git pull origin '+branch], shell=True)
    time.sleep(5)
    print 'Most recent branch syncronised: '+branch
    subprocess.call(['./build_script &'], shell=True)
    time.sleep(90)

init()
while True:
    subprocess.call(['git pull origin >/dev/null 2>&1'], shell=True)
    time.sleep(3)
    subprocess.call(['git checkout release >/dev/null 2>&1'], shell=True)
    time.sleep(1)
    check_diff()
