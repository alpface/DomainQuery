from query_aliyun import domainQueryFromAliyun
import time

def main():
    code = str(input('请输入完整的domain：'))
    lList = [code]
    with open('resource/active.txt', 'a+') as activeFile:
        # 记录当前查询日期
        isotimeformat = '%Y-%m-%d %H:%M:%S'
        current_date = time.strftime(isotimeformat, time.localtime(time.time()))
        activeFile.write(current_date + "\n")
    while (1):
        actives = domainQueryFromAliyun(lList, 5)
        if len(actives):
            break

if __name__ == '__main__':
    main()