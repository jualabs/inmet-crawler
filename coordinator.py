from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process, Queue
from twisted.internet import reactor
import sys

# the wrapper to make the spider run more times
def run_spider(url,dtaIni,dtaFim):
    def f(q,url,dtaIni,dtaFim):
        try:
            settings = get_project_settings()
            runner = CrawlerRunner(settings)
            deferred = runner.crawl('estacoes',url=url,dtaIni=dtaIni,dtaFim=dtaFim)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,url,dtaIni,dtaFim,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

f = open('inmet/metadata/url.data','r')
urls = []
for l in f:
    urls.append(l.replace('\n',''))
f.close()

for url in urls:
   print("Getting url %s" % url)
   dia = str(sys.argv[1])
   run_spider(url,dia,dia)
