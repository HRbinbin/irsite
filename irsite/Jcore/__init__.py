import os


def search(keyword):
    path = os.path.dirname(os.path.realpath(__file__))
    cmd = 'echo "{0}" | java -classpath .;{1}/lib/*;{2}; search.ZWPaperInex'.format(keyword, path, path)
    result = os.popen(cmd)
    # print(result.read())
    results = []
    for i in result.read().split('\n'):
        if i.count('加载扩展词典：ext.dic') != 0 or i.count('加载扩展停止词典：stopword.dic') != 0:
            continue
        results.append(i.split('\t'))
    return results
