__author__ = 'alex'

import file_loader
import initiater
import query_composer


def show_ans(queries):
    # out_tree.traverse(debug=True)

    for query in queries:
        for twig in query:
            print('head:'+str(twig.head)+' in:'+str(twig.in_edge)+' out:'+str(twig.out_edge))


def main():
    print("hello world!")
    l_in, l_out, l_in_menu, l_out_menu = file_loader.load_map()
    in_tree, out_tree = initiater.init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu)
    queries = query_composer.compose_query()
    show_ans(queries=queries)



if __name__ == "__main__":
    main()
