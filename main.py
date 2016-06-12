from mpi4py import MPI
import util


def main():
    # recupera o comunicador
    comm = MPI.COMM_WORLD

    # obtem o ranque do processo atual
    rank = comm.Get_rank()

    # define a url do arquivo a ser baixado
    url = 'http://api.soundcloud.com/tracks/86979624/stream?client_id=36c93f8b49b8a30bd3bab88e57e4758a&.mp3'

    # processo coordenador
    if rank == 0:
        util.criar_diretorio_temporario_caso_nao_exista()

        # obtem a colecao de intervalos
        intervalos = util.fabricar_intervalos(url)

        # manda cada intervalo para um processo
        comm.send(intervalos[0], dest=1)
        comm.send(intervalos[1], dest=2)
        comm.send(intervalos[2], dest=3)
        comm.send(intervalos[3], dest=4)

        # verifica se todos os processos baixaram suas partes com sucesso
        if comm.recv(source=1)\
                and comm.recv(source=2)\
                and comm.recv(source=3)\
                and comm.recv(source=4):

                # junta os arquivos temporarios em um unico arquivo
            util.juntar_arquivos_temporarios(url)
            # util.deletar_o_diretorio_temporario()

        print '\n'

    # processos operarios
    if rank == 1:
        intervalo = comm.recv(source=0)

        baixouComSucesso = util.baixar_uma_parte_do_arquivo(url, 0, intervalo)

        comm.send(baixouComSucesso, dest=0)
    if rank == 2:
        intervalo = comm.recv(source=0)

        baixouComSucesso = util.baixar_uma_parte_do_arquivo(url, 1, intervalo)

        comm.send(baixouComSucesso, dest=0)
    if rank == 3:
        intervalo = comm.recv(source=0)

        baixouComSucesso = util.baixar_uma_parte_do_arquivo(url, 2, intervalo)

        comm.send(baixouComSucesso, dest=0)
    if rank == 4:
        intervalo = comm.recv(source=0)

        baixouComSucesso = util.baixar_uma_parte_do_arquivo(url, 3, intervalo)

        comm.send(baixouComSucesso, dest=0)


if __name__ == '__main__':
    main()
