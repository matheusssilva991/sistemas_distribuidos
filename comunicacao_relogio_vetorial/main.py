from mpi4py import MPI  # noqa
from utils.utils import update_causal_vector, check_causality_condition

TIME_LIMIT = 12
TIME_UPDATE = 1 / 10000

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

messages_to_send = {
    0: [
        {"t_send": 0, "t_receive": 3, "destination": 1},
        {"t_send": 0, "t_receive": 6, "destination": 3},
    ],
    1: [
        {"t_send": 2, "t_receive": 3, "destination": 2},
        {"t_send": 2, "t_receive": 7, "destination": 3},
    ],
    2: [{"t_send": 4, "t_receive": 5, "destination": 3}],
}
causal_vector = [0 for _ in range(size)]
current_time = 0
messages_buffer = {i: [] for i in range(size)}

while current_time < TIME_LIMIT:
    # Pick messages to send in current time
    current_time_messages = [m for m in messages_to_send.get(rank, [])
                             if m.get("t_send") == current_time]

    # Update the causal vector
    if len(current_time_messages) > 0:
        causal_vector[rank] += 1

    # Send messages in current time
    for message in current_time_messages:
        ts_m = {"message": message, "causal_vector": causal_vector}
        comm.send(ts_m, dest=message.get("destination"))
        messages_to_send.get(rank).remove(message)

    tmp_buffer = messages_buffer.copy()
    for i, messages in tmp_buffer.items():
        for ts_m in messages:
            message = ts_m.get("message")
            recv_causal_vector = ts_m.get("causal_vector")

            if message.get("t_receive") <= current_time:
                if check_causality_condition(
                    causal_vector, recv_causal_vector, size, i
                ):
                    causal_vector = update_causal_vector(
                        causal_vector, recv_causal_vector, size, i
                    )
                    if message in messages_buffer[i]:
                        messages_buffer[i].remove(message)

    # Receive messages
    for i in range(size):
        if i != rank:
            if comm.iprobe(source=i):
                ts_m = comm.recv(source=i)
                message = ts_m.get("message")
                recv_causal_vector = ts_m.get("causal_vector")

                if not ts_m:
                    continue

                if message.get("t_send") > current_time:
                    messages_buffer[i].append(ts_m)
                else:
                    if check_causality_condition(
                        causal_vector, recv_causal_vector, size, i
                    ):

                        causal_vector = update_causal_vector(
                            causal_vector, recv_causal_vector, size, i
                        )

    current_time += TIME_UPDATE
    current_time = round(current_time, 5)

print(f"Vc[{rank}]: ", causal_vector)
