import os

def count_list(arr):
    '''
     list中的count,获取所有元素的出现次数
    :param arr:
    :return: {key: count}
    '''
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    return result

def domainFilter():
    '''
    过滤所有active的domain，查找只出现过一次能注册的domain
    :return:
    '''
    with open('resource/active.txt', 'r+') as file:
        activeDomains = file.readlines()
        newlist = []
        for line in activeDomains:
            # 去掉换行符
            domain = line.strip('\n')
            if domain.endswith('.com'):
                newlist.append(domain)
        resultDict = count_list(newlist)
        onlyDomains = []
        for (key, value) in resultDict.items():
            if value == 1:
                onlyDomains.append(key)
                print(key)
if __name__ == '__main__':
    domainFilter()