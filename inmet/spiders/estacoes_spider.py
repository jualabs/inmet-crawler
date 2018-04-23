import scrapy
import os

class EstacoesSpider(scrapy.Spider):
    name = "estacoes"
    cookie = ""

    def __init__(self, url=None, dtaIni=None, dtaFim=None, *args, **kwargs):
        super(EstacoesSpider, self).__init__(*args, **kwargs)
        self.url = url
        self.dtaIni = dtaIni
        self.dtaFim = dtaFim
        self.directory = 'inmet/data/%s' % dtaIni.replace("/","-")
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def start_requests(self):
        dadosConsulta = {
            'aleaValue': 'NDY0Nw==',
            'dtaini': self.dtaIni,
            'dtafim': self.dtaFim,
            'aleaNum': '4647'
        }
        yield scrapy.FormRequest(url=self.url, formdata=dadosConsulta, callback=self.parse_form, priority=1)

    def parse_form(self, response):
        try:
            self.cookie = response.headers["Set-Cookie"]
        except:
            self.cookie = self.cookie
        cabecalho = {
            'Cookie': self.cookie
        }
        self.log('Get data from the site')
        url = 'http://www.inmet.gov.br/sonabra/pg_downDadosCodigo_sim.php'
        yield scrapy.Request(url=url, callback=self.parse_data, headers= cabecalho, dont_filter=True, priority=2)

    def parse_data(self, response):
        self.log('Lets save data...')
        body = response.text
        estacao = body.split('<br>')[1].split(',')[0]
        filename = '/estacao-%s.html' % estacao

        with open(self.directory+filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
