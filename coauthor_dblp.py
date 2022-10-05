# cyc @ 2022-10-04

import requests
import xmltodict
import argparse

def get_dblp_coauthors(pid, start_year: int = 0, min_papers: int = 1):
    
    url = "https://dblp.org/pid/" + pid + ".xml"

    try:
        response = requests.get(url)
        data = xmltodict.parse(response.content, dict_constructor = dict)
    except:
        return None

    if 'dblpperson' not in data.keys():
        pass

    coauthors = {}
    for _paper in data['dblpperson']['r']:
        for _, _paper_kvs in _paper.items():
            if 'year' not in _paper_kvs or 'author' not in _paper_kvs:
                continue

            _y = int(_paper_kvs['year'])
            if _y >= start_year:
                _author_kvs_lst = _paper_kvs['author']
                if type(_author_kvs_lst) == list:
                    pass
                elif type(_author_kvs_lst) == dict: # workshop
                    _author_kvs_lst = [_author_kvs_lst]

                for _authorkvs in _author_kvs_lst:
                    _authorpid = _authorkvs['@pid']
                    _authorname = _authorkvs['#text']
                    if _authorpid not in coauthors:
                        coauthors[_authorpid] = (_authorname, [])
                    coauthors[_authorpid][1].append(_y)


    if pid not in coauthors:
        print('[Error] args.pid not in coauthor list. {} -- {}'.format(pid, str(coauthors)))
        return None

    coauthors.pop(pid)

    for _k in list(coauthors.keys()):
        if len(coauthors[_k][1]) < min_papers:
            coauthors.pop(_k)
    return coauthors



def coauthors_dic_to_str(coauthors, sep = '\n'):
    rtn = ""
    if coauthors is not None:
        for _, (_authorname, _y_lst) in sorted(coauthors.items(), key = lambda x: x[1][0]):
            rtn +=   _authorname + ': [' + ', '.join([str(_y) for _y in _y_lst]) + ']' + sep
    return rtn



# To show all Gao Cong's coauthors from 2020:
#       python coauthor_dblp.py --pid 33/3180 --start_year 2020 --min_papers 2
# Jianzhong 41/1074-1
# Egemen    22/544
# Junhao    06/11411
# Zhifeng   20/3716
# Lars      57/1331
# Tony 
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--pid', type = str, required = True,
                        help = "Pid of the author. It can be obtained from the url of the author's dblp homepage."
                                "For example, Kaiming's pid = '34/7659', and "
                                "Yufei's is 't/YufeiTao'.")
    parser.add_argument('--start_year', type = int, default = 0, 
                        help = "Output the papers published between $start_year (included) "
                                "and the current year. E.g., 2020.")
    parser.add_argument('--min_papers', type = int, default = 1, 
                        help = "The minimal number of common papers. "
                                "E.g., 1, that is at least having 1 common paper. ")
                             
    args = parser.parse_args()

    coauthors = get_dblp_coauthors(args.pid, args.start_year, args.min_papers)
    if coauthors != None:
        print(coauthors_dic_to_str(coauthors, sep = '\n'))