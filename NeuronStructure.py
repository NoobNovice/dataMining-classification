import copy
import random

def zero_list(n):
    return [0] * n

def structure(number_of_layer_hidden, number_of_node_hidden, number_of_input, number_of_output):
    I_layer = zero_list(number_of_input)
    O_layer = zero_list(number_of_output)
    H_layer = []
    bias_layer = []
    Wight = []

    layer = zero_list(number_of_node_hidden)
    for i in range(number_of_layer_hidden):
        H_layer.append(copy.deepcopy(layer))
        bias_layer.append(copy.deepcopy(layer))
    # bias of output in last list
    bias_layer.append(zero_list(number_of_output))

    for i in range(number_of_layer_hidden + 1):
        if i == 0:
            Wight.append(zero_list(number_of_input * len(H_layer[i])))
        elif i == number_of_layer_hidden:
            Wight.append(zero_list(number_of_output * len(H_layer[i - 1])))
        else:
            Wight.append(zero_list(len(H_layer[i]) * len(H_layer[i - 1])))

    # random wight
    for i in range(len(Wight)):
        for j in range(len(Wight[i])):
            Wight[i][j] = random.triangular(-1, 1, 0.1)
    # random bias
    for i in range(len(bias_layer)):
        for j in range(len(bias_layer[i])):
            bias_layer[i][j] = random.random()

    return I_layer, H_layer, O_layer, Wight, bias_layer
