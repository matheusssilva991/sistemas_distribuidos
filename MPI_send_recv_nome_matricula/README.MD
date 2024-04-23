# Programa MPI em Python para enviar nome e número de matrícula

## Requisitos

- MPI (OpenMPI ou MPICH)
- MPI4PY
- python-decouple

## Utilização

- Renomeie o arquivo .env.example para .env e coloque seu nome e número de matrícula
- Utilize o seguinte comando no terminal, em que N é o número de processos.

```bash
mpirun -n N python main.py
```
