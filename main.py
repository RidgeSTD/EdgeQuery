import common
import file_loader
import initiater
import query_composer
import search_engine
import time
import statics

__author__ = 'alex'

ans_io_time = 0.0


def main():
    print("hello world!")
    l_in, l_out, l_in_menu, l_out_menu, node_set = file_loader.load_map()
    fo = open('/Users/alex/answer.txt', 'a')
    in_tree, out_tree = initiater.init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu, node_set)
    queries, q_in, q_out, q_in_menu, q_out_menu = query_composer.compose_query()
    for i in range(0, len(queries)):
        statics.ans_io_time = 0.0
        fo.write('for query ' + str(i) + ':\n')
        t1 = time.clock()
        result = search_engine.entrance(in_tree=in_tree, out_tree=out_tree, twigs=queries[i], l_in=l_in, l_out=l_out,
                                        q_in=q_in, q_out=q_out, q_in_menu=q_in_menu, q_out_menu=q_out_menu, fo=fo)
        if result == common.INVALID_CANDIDATE:
            print('no result')
        t2 = time.clock()
        print("查询" + str(i) + "输出结果耗时 " + str(statics.ans_io_time))
        print("查询" + str(i) + "共计耗时 " + str(t2 - t1))
        fo.write('\n\n')


if __name__ == "__main__":
    main()
