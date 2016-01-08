import time
import os

import common
import file_loader
import initiater
import query_composer
import search_engine
import statics

__author__ = 'alex'

ans_io_time = 0.0


def main():
    __init_statics()
    if os.path.isfile(common.ROOT_PATH + 'answer.txt'):
        os.remove(common.ROOT_PATH + 'answer.txt')

    if os.path.isfile(common.ROOT_PATH + 'console.txt'):
        os.remove(common.ROOT_PATH + 'console.txt')

    fo = open(common.ROOT_PATH + 'answer.txt', 'a')
    statics.f_console = open(common.ROOT_PATH + 'console.txt', mode='a', encoding='utf-8')
    print("hello world!")
    print("hello world!", file=statics.f_console)
    l_in, l_out, l_in_menu, l_out_menu, node_set, neighbor = file_loader.load_map()
    in_tree, out_tree = initiater.init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu, node_set, neighbor)
    queries, q_in, q_out, q_in_menu, q_out_menu = query_composer.compose_query()
    for i in range(0, len(queries)):
        __debug_counter_reset()  # TODO 调试!日后删除

        statics.ans_io_time = 0.0
        fo.write('for query ' + str(i) + ':\n')
        t1 = time.clock()  # timer

        result = search_engine.entrance(in_tree=in_tree, out_tree=out_tree, twigs=queries[i], l_in=l_in, l_out=l_out,
                                        q_in=q_in[i], q_out=q_out[i], q_in_menu=q_in_menu[i], q_out_menu=q_out_menu[i],
                                        fo=fo, node_set=node_set)
        if result == common.INVALID_CANDIDATE:
            fo.write('no result\n')
            print('no result')
            print('no result', file=statics.f_console)
        t2 = time.clock()  # timer
        print("查询" + str(i) + "输出结果耗时 " + str(statics.ans_io_time))
        print("查询" + str(i) + "输出结果耗时 " + str(statics.ans_io_time), file=statics.f_console)
        print("查询" + str(i) + "共计耗时 " + str(t2 - t1))
        print("查询" + str(i) + "共计耗时 " + str(t2 - t1), file=statics.f_console)
        __debug_counter_output()
        fo.write('\n\n')
    fo.close()


def __init_statics():
    statics.fade_factor_pow = [1]
    for i in range(1, statics.neighbor_threshold + 1):
        statics.fade_factor_pow.append(statics.fade_factor_pow[i - 1] * statics.fade_factor)


def __debug_counter_output():
    print("__locate_node调用次数: " + str(statics.locate_called_time))
    print("__locate_node调用次数: " + str(statics.locate_called_time), file=statics.f_console)
    print("__locate_node调用耗时: " + str(statics.located_run_time))
    print("__locate_node调用耗时: " + str(statics.located_run_time), file=statics.f_console)


def __debug_counter_reset():
    statics.located_run_time = 0
    statics.locate_called_time = 0


if __name__ == "__main__":
    main()
