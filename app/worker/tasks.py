from celery import Celery
from . import crawler as c
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import os


broker = os.environ['CELERY_BROKER']
result_backend = os.environ['CELERY_RESULT_BACKEND']
es_interactor = os.environ['ES_INTERACTOR']

celery = Celery('tasks', broker=broker, backend=result_backend,
                task_track_started=True, worker_max_tasks_per_child=1)


@celery.task(name='scrape')
def scrape_url(url):
    url_list = []
    settings = get_project_settings()
    settings.set('SPIDER_MIDDLEWARES', {
        "scrapy.spidermiddlewares.offsite.OffsiteMiddleware": 500
    })
    settings.set('DOWNLOAD_DELAY', 1)
    process = CrawlerProcess(settings)
    process.crawl(c.WebCrawler, url=url, url_list=url_list, es_interactor=es_interactor)
    process.start()
    return url_list
