# Programa MPI em Python para enviar nome e número de matrícula

## Requisitos

- MPI (OpenMPI ou MPICH)
- MPI4PY

## Utilização

- Renomeie o arquivo .env.example para .env e coloque seu nome e número de matrícula
- Utilize o seguinte comando no terminal, em que N é o número de processos.

```bash
mpirun -n N python main.py
```

## Observações

Politicas de privadade do sistema podem causar problemas na execução do código, caso tenha problemas execute os seguintes comandos:

### Verificar a politica atual do PTrace

```bash
cat /proc/sys/kernel/yama/ptrace_scope
```

Os valores possíveis são:

- 0: ptrace totalmente permissivo.
- 1: ptrace restrito a filhos do processo.
- 2: ptrace restrito a processos do mesmo UID.
- 3: ptrace completamente restrito.

### Alterar a Política do ptrace

Para permitir o uso do CMA, você pode definir a política do ptrace para um valor menos restritivo (por exemplo, 0 ou 1):

```bash
sudo sysctl -w kernel.yama.ptrace_scope=0
```

Para tornar a alteração permanente, edite o arquivo /etc/sysctl.d/10-ptrace.conf (ou crie um novo arquivo de configuração):

```bash
echo "kernel.yama.ptrace_scope=0" | sudo tee /etc/sysctl.d/10-ptrace.conf
```

Recarregue as configurações do sysctl:

```bash
sudo sysctl --system
```
