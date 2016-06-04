from blessings import Terminal
import os
import urllib2
import shutil
from glob import iglob
from progressbar import ProgressBar


class Writer(object):
    '''
        Cria um objeto para imprimir a barra de progresso utilizando
        o progressbar e o blessing
    '''

    def __init__(self, location):
        self.location = location

    def write(self, string):
        term = Terminal()

        with term.location(*self.location):
            print(string)


def baixar_uma_parte_do_arquivo(url, indice, intervalo):

    # prepara a requisicao
    requisicao = urllib2.Request(url)

    # define no cabecario da requisicao o intervalo de bits do arquivo que deseja baixar
    requisicao.headers['Range'] = 'bytes=%s-%s' % (intervalo['inicio'], intervalo['fim'])

    try:
        # abre a requisicao
        requisicaoAberta = urllib2.urlopen(requisicao)

        # criar um arquivo temporario para salvar o intervalo baixado
        with open('/Users/edmilsonneto/Downloads/temp/' + os.path.basename(url), "wb") as arquivo:
            # define o nome do arquivo
            nomeDoArquivo = arquivo.name

            # concatena o indice + .part ao nome do arquivo, ex: arquivo01.part
            os.rename(nomeDoArquivo, nomeDoArquivo[:len(nomeDoArquivo) - 4] + str(indice) + '.part')

            # escreve a parte baixada no arquivo temporario

            # obtem o tamanho do arquivo
            tamanhoDoArquivo = int(requisicaoAberta.headers.get("content-length"))

            # perfumaria para a barra de progresso ;)

            # define o tamanho do bloco da barra de progresso
            tamanhoDoBloco = int(int(tamanhoDoArquivo) / 100)
            att = 0

            # define a posicao que a barra de progresso sera plotada no terminal
            writer = Writer((1, indice + 1))

            # incrementa a barra de progresso e faz a magica acontecer
            with ProgressBar(max_value=tamanhoDoArquivo, fd=writer) as progress:
                while 1:
                    # salva o bloco baixado no arquivo temporario
                    arquivo.write(requisicaoAberta.read(tamanhoDoBloco))

                    att += tamanhoDoBloco

                    if att >= tamanhoDoArquivo:
                        break
                    progress.update(att)

        return True

    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
        return False
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
        return False


def fabricar_intervalos(url):

    # prepara a requisicao
    requisicao = urllib2.Request(url)

    # abre a requisicao
    f = urllib2.urlopen(requisicao)

    # obtem o tamanho total do arquivo
    tamanhoTotalDoArquivo = f.headers['Content-Length']

    # divide o tamanho do intervalo por 4 para definir o tamanho de cada intervalo
    tamanhoDoIntervalo = int(tamanhoTotalDoArquivo) / 4

    # cria varios intervalos contendo o valor inicial e final obs: rola uma magica matematica aqui kkkk
    particao01 = {'inicio': 0, 'fim': tamanhoDoIntervalo}
    particao02 = {'inicio': tamanhoDoIntervalo + 1, 'fim': tamanhoDoIntervalo * 2}
    particao03 = {'inicio': (tamanhoDoIntervalo * 2) + 1, 'fim': tamanhoDoIntervalo * 3}
    particao04 = {'inicio': (tamanhoDoIntervalo * 3) + 1, 'fim': tamanhoDoIntervalo * 4}

    # cria uma colecao de intervalos e adiciona cada um dos intervalos criados
    intervalos = []
    intervalos.append(particao01)
    intervalos.append(particao02)
    intervalos.append(particao03)
    intervalos.append(particao04)

    return intervalos


def obter_o_nome_do_arquivo(url):

    nomeDoArquivo = url.split('/', len(url) - 1)
    nomeDoArquivo = nomeDoArquivo[len(nomeDoArquivo) - 1]

    return nomeDoArquivo


def deletar_o_diretorio_temporario():
    shutil.rmtree('/Users/edmilsonneto/Downloads/temp/')


def juntar_arquivos_temporarios(url):

    # obtem o nome do arquivo
    nomeDoArquivo = obter_o_nome_do_arquivo(url)

    # cria um novo arquivo
    arquivo = open('/Users/edmilsonneto/Downloads/' + nomeDoArquivo, 'wb')

    # itera sobre cada arquivo temporario
    for filename in iglob(os.path.join(os.getcwd(), '*.part')):
        # copia o conteudo de cada arquivo temporario para o arquivo final
        shutil.copyfileobj(open(filename, 'rb'), arquivo)

    # fecha o arquivo
    arquivo.close()


def criar_diretorio_temporario_caso_nao_exista():
    diretorioTemporario = '/Users/edmilsonneto/Downloads/temp/'

    if not os.path.isdir(diretorioTemporario):
        os.mkdir(diretorioTemporario)
