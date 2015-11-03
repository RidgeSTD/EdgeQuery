__author__ = 'alex'

import file_loader
import initiater

def main():
    print("hello world!")
    l_in, l_out, l_in_menu, l_out_menu = file_loader.load_map()
    in_tree, out_tree = initiater.init_in_out_tree(l_in, l_out, l_in_menu, l_out_menu)
    out_tree.traverse(debug=True)


if __name__ == "__main__":
    main()
