from crontab import CronTab

from config.utils import logging
from config.utils import setup_env, get_env_value


def main():
    setup_env()

    logger = logging.get_logger()

    # instantiate cron, automatically run `cron.write()` on exit
    with CronTab(user=True) as cron:
        # clear existing cron jobs
        cron.remove_all()
        # create new job
        job = cron.new(command='python main.py')
        # set job to run at 12PM daily
        job.setall(get_env_value("CRON_SLICES"))

    # validate job
    for job in cron:
        logger.info(f"Cron job instantiated: {job}")


if __name__ == '__main__':
    main()
    