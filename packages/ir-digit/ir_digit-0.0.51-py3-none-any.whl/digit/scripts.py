import argparse
from .core import Core

def main():
    parser = argparse.ArgumentParser(prog="digit")
    subparsers = parser.add_subparsers(dest='command')

    parser.add_argument("-h", "--help", action='help', help="帮助")
    parser.add_argument("-u", "--update-api-token", help="设置/更新个人的API-token")
    parser.add_argument("-c", "--category", help="查看分类体系中的编码与含义", default=None)

    query_parser = subparsers.add_parser('query', help='子命令：查看平台现有资源')
    query_parser.add_argument("-t", "--type", help="查看哪种类型的资源，data/card/useraccount/websetting/dataid", default='data')
    query_parser.add_argument("-i", "--id", help="选择特定id的资源查看", default=None)
    query_parser.add_argument("-d", "--detail", help="是否查看详情，默认为否", default=False)

    download_parser = subparsers.add_parser('download', help='子命令：下载资源到本地')
    download_parser.add_argument("-i", "--id-or-name", help="根据data_id_or_name下载对应的资源至本地，默认如果已经存在则不更新资源")
    download_parser.add_argument("-u", "--update", help="更新下载的资源")

    args = parser.parse_args()
    core = Core()

    if args.command == "query":
        core.get_resources(api_type=args.type, id=args.id, detail=args.detail)
    elif args.command == "download":
        core.download_repo(data_id_or_name=args.id_or_name, update=args.update)
    else:
        if args.update_api_token:
            core.update_api_token(new_token=args.update_api_token)
        elif args.category:
            core.get_category()
        else:
            parser.print_help()

if __name__ == '__main__':
    main()
