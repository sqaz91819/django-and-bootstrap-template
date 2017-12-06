import requests
from bs4 import BeautifulSoup
from pprint import pprint
import base64
from crawler_api.mongodb import Mongodb


def __get_urls(url):
    resp = requests.get(url)
    page = resp.text
    soup = BeautifulSoup(page, "html.parser")
    lst = soup.find_all("a", style="text-decoration: none; font-weight: 700")
    urls = []
    for d in lst:
        href = d.get('href')
        urls.append("http://www.truemovie.com/" + href)

    return urls


def __get_info(url):
    resp = requests.get(url)
    resp.encoding = 'big5'
    page = resp.text
    soup = BeautifulSoup(page, "html.parser")
    img = soup.find_all('img', border="0")
    pic_url = 'http://www.truemovie.com/' + img[0]['xthumbnail-orig-image'][3:]
    test = list(soup.strings)
    new = [l.replace('\n', '') for l in test]
    new = [l.replace('\t', '').replace('：', '').strip('()') for l in new if l]
    labels = ['中文片名', '大陸譯名', '英文片名', '台灣上映日期', '北美上映日期', '類型', '導演']
    movies = {}
    for label in labels:
        movies[label] = None
    for i in range(len(new)):
        if new[i] in labels:
            movies[new[i]] = new[i + 1]
    movies['picture'] = base64.b64encode(requests.get(pic_url).content)
    return movies


if __name__ == '__main__':
    f = open('2016failed_list.txt', 'w')
    with Mongodb(hash_check=False) as mgd:
        count = 1
        urls = __get_urls("http://www.truemovie.com/tairelease2016.htm")
        for url in urls:
            print(url)
            try:
                movie = __get_info(url)
            except:
                f.write(url)
                continue
            mgd.insert_one('movie_list', movie)
            print("Success!" + str(count) + "/" + str(len(urls)))
            count += 1
    f.close()
