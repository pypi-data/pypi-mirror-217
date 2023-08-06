import argparse



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--resource","data_id",help="DATA ID")
    print("输入的参数为")
    args = parser.parse_args()
    print(args.resource)