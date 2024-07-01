def check_causal_vector_size(causal_vector: list,
                             recv_causal_vector: list,
                             size: int) -> None:
    if len(causal_vector) != size or \
            len(recv_causal_vector) != size:
        raise ValueError('Both vectors must have the same size')


def check_causal_vector_elements(causal_vector: list,
                                 recv_causal_vector: list) -> None:
    if any(causal < 0 or recv < 0 for causal, recv in zip(causal_vector,
                                                          recv_causal_vector)):
        raise ValueError('All elements in causal_vector and',
                         'recv_causal_vector must be positive')


def check_causal_vector_types(causal_vector: list,
                              recv_causal_vector: list) -> None:
    if any(not isinstance(causal, int) or not isinstance(recv, int)
           for causal, recv in zip(causal_vector, recv_causal_vector)):
        raise ValueError('All elements in causal_vector and',
                         'recv_causal_vector must be integers')


def check_causal_vector_error(causal_vector: list,
                              recv_causal_vector: list,
                              size: int) -> None:
    check_causal_vector_size(causal_vector, recv_causal_vector, size)
    check_causal_vector_elements(causal_vector, recv_causal_vector)
    check_causal_vector_types(causal_vector, recv_causal_vector)


def check_causality_condition(causal_vector: list,
                              recv_causal_vector: list,
                              size: int,
                              i: int) -> bool:
    # Check if causal_vector and recv_causal_vector are valid
    check_causal_vector_error(causal_vector, recv_causal_vector, size)

    return causal_vector[i] + 1 == recv_causal_vector[i] and \
        all(causal_vector[k] >= recv_causal_vector[k]
            for k in range(size) if k != i)


def update_causal_vector(causal_vector: list,
                         recv_causal_vector: list,
                         size: int,
                         i: int) -> list:

    # Check if causal_vector and recv_causal_vector are valid
    check_causal_vector_error(causal_vector, recv_causal_vector, size)

    # Check if causal_vector and recv_causal_vector are equal
    if causal_vector == recv_causal_vector:
        return causal_vector

    causal_vector[i] += 1

    for k in range(size):
        if k != i:
            causal_vector[k] = max(causal_vector[k], recv_causal_vector[k])

    return causal_vector
