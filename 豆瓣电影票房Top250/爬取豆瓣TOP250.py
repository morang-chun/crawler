import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

movie_name = []
movie_url = []
movie_star = []
movie_star_pople = []
movie_director = []
movie_actor = []
movie_year = []
movie_country = []
movie_type = []

def get_movie_info(url,headers):
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')
    for movie in soup.select('.item'):
        name = movie.select('.hd a')[0].text.replace('\n','')
        movie_name.append(name)
        url = movie.select('.hd a')[0]['href']
        movie_url.append(url)
        star = movie.select('.rating_num')[0].text
        movie_star.append(star)
        star_people = movie.select('.star span')[3].text
        star_people = star_people.strip().replace('人评价','')
        movie_star_pople.append(star_people)
        movie_infos = movie.select('.bd p')[0].text.strip()
        director = movie_infos.split('\n')[0].split('   ')[0]
        movie_director.append(director)
        try:
            actor = movie_infos.split('\n')[0].split('   ')[1]
            movie_actor.append(actor)

        except:
            movie_actor.append(None)

        if name == '大闹天宫 / 大闹天宫 上下集 / The Monkey King':
            year0 = movie_infos.split('\n')[1].split('/')[0].strip()
            year1 = movie_infos.split('\n')[1].split('/')[1].strip()
            year2 = movie_infos.split('\n')[1].split('/')[2].strip()
            year = year0 + '/' + year1 + '/' + year2
            movie_year.append(year)
            country  = movie_infos.split('\n')[1].split('/')[3].strip()
            movie_country.append(country)
            type = movie_infos.split('\n')[1].split('/')[4].strip()
            movie_type.append(type)

        else:
            year = movie_infos.split('\n')[1].split('/')[0].strip()
            movie_year.append(year)
            country = movie_infos.split('\n')[1].split('/')[1].strip()
            movie_country.append(country)
            type = movie_infos.split('\n')[1].split('/')[2].strip()
            movie_type.append(type)
def save_to_csv(csv_name):
    df = pd.DataFrame()
    df['电影名称'] = movie_name
    df['电影链接'] = movie_url
    df['电影评分'] = movie_star
    df['评分人数'] = movie_star_pople
    df['导演'] = movie_director
    df['主演'] = movie_actor
    df['上映年份'] = movie_year
    df['国家'] = movie_country
    df['类型'] = movie_type
    df.to_csv(csv_name,encoding='utf_8_sig')


if __name__ == "__main__":
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.9231 SLBChan/30'
    }
    for i in range(10):
        page_url = "https://movie.douban.com/top250?start={}".format(str(i*25))
        print("开始爬取{}页，地址是{}".format(str(i+1),page_url))
        get_movie_info(page_url,headers)
        sleep(1)

    save_to_csv(csv_name="豆瓣TOP250.csv")



