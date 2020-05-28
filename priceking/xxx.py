import sys

sys.path.append("/home/webgladiator/.virtualenvs/premiumdog/lib/python3.8/site-packages")
#sys.path.append("/home/webgladiator/priceking/shop")
#sys.path.insert(0, 'home/webgladiator/priceking')

import schedule


def job():
    print('teszt')

schedule.every(5).seconds.do(job)
