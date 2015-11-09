import file_loader
import initiater
import query_composer
import search_engine

__author__ = 'alex'


def show_ans(a, b):
    print(a)
    print(b)


def main():
    print("hello world!")
    l_in, l_out, l_in_menu, l_out_menu, node_set = file_loader.load_map()
    in_tree, out_tree = initiater.init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu, node_set)
    queries, q_in, q_out, q_in_menu, q_out_menu = query_composer.compose_query()
    for twigs in queries:
        search_engine.entrance(in_tree=in_tree, out_tree=out_tree,
                               twigs=twigs, q_in=q_in, q_out=q_out, q_in_menu=q_in_menu, q_out_menu=q_out_menu)
    # show_ans(l_in, l_in_menu)


if __name__ == "__main__":
    main()
