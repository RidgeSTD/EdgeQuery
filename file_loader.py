__author__ = 'alex'


def __inner_sort(arr, menu):
    for node in menu:
        menu[node].sort()
        for label in menu[node]:
            arr[node][label].sort()


def load_map():
    """
    Pass L_in, L_out, noted for in/out degree dictionary and in/out label-marked dictionary

    NOTE! The initialization must be done outside the function
    """
    print("start loading file...")
    l_in = {}
    l_out = {}
    l_in_menu = {}
    l_out_menu = {}
    f = open("/Users/alex/data.txt")
    while True:
        line = f.readline()
        if len(line) < 1:
            break
        tpl = line.split('\t')
        ori = int(tpl[0])
        edg = int(tpl[1])
        des = int(tpl[2])
        if ori not in l_out:
            l_out[ori] = {}
        if ori not in l_out_menu:
            l_out_menu[ori] = []
        if des not in l_in:
            l_in[des] = {}
        if des not in l_in_menu:
            l_in_menu[des] = []

        try:
            l_in[des][edg].append(ori)
        except:
            l_in[des][edg] = []
            l_in[des][edg].append(ori)

        try:
            l_out[ori][edg].append(des)
        except:
            l_out[ori][edg] = []
            l_out[ori][edg].append(des)

        if edg not in l_in_menu[des]:
            l_in_menu[des].append(edg)
        if edg not in l_out_menu[ori]:
            l_out_menu[ori].append(edg)

    __inner_sort(l_in, l_in_menu)
    __inner_sort(l_out, l_out_menu)
    print("end loading file...")
    return l_in, l_out, l_in_menu, l_out_menu