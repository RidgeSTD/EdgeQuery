import common
import file_loader
import initiater
import query_composer
import search_engine

__author__ = 'alex'


def main():
    print("hello world!")
    l_in, l_out, l_in_menu, l_out_menu, node_set = file_loader.load_map()
    in_tree, out_tree = initiater.init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu, node_set)
    queries, q_in, q_out, q_in_menu, q_out_menu = query_composer.compose_query()
    for i in range(0, len(queries)):
        print('for query ' + str(i) + ':')
        result = search_engine.entrance(in_tree=in_tree, out_tree=out_tree, twigs=queries[i], l_in=l_in, l_out=l_out,
                                        q_in=q_in, q_out=q_out, q_in_menu=q_in_menu, q_out_menu=q_out_menu)
        if result == common.INVALID_CANDIDATE:
            print('no result')
        print('\n\n')


if __name__ == "__main__":
    main()
