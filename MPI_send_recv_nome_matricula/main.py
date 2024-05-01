from mpi4py import MPI
from decouple import config

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

ID_PROCESSO_MESTRE = 0

# Processo 0, mestre, envia nome e número de matrícula para os demais processos
for id_processo in range(size):
    if id_processo != ID_PROCESSO_MESTRE and rank == ID_PROCESSO_MESTRE:
        nome = config("NOME")
        matricula = config("MATRICULA")

        print(f"Processo {rank} enviando mensagem para processo {id_processo}")

        comm.send(nome, dest=id_processo)
        comm.send(matricula, dest=id_processo)
        # comm.send([nome, matricula], dest=id_processo)

# Demais processos recebem a mensagem do processo 0
if rank != ID_PROCESSO_MESTRE:
    nome_recebido = comm.recv(source=ID_PROCESSO_MESTRE)
    matricula_recebida = comm.recv(source=ID_PROCESSO_MESTRE)
    # mensagem_recebida = comm.recv(source=ID_PROCESSO_MESTRE)

    mensagem_recebida = [nome_recebido, matricula_recebida]
    print("Processo {} recebeu mensagens do processo {}: {}"
          .format(rank, ID_PROCESSO_MESTRE, mensagem_recebida))
