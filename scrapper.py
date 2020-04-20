import requests
import time
from bs4 import BeautifulSoup
from review import extract_review

URL = "https://movie.naver.com/movie/running/current.nhn"

result = requests.get(URL)
soup = BeautifulSoup(result.text, "html.parser")

cards = soup.find_all("dl", {"class": "lst_dsc"})


def setting(Pstart, Pend, Ppage):
  global start
  start = Pstart
  global end
  end = Pend
  global max_comment_page
  max_comment_page = Ppage
  return start_scrapping()


def extract_movie(html, rank):
  title = html.find("dt", {"class", "tit"}).find("a").string
  link = html.find("dt", {"class", "tit"}).find("a")["href"]
  link = f"{URL}{link}"

  star = html.find("div", {"class", "star_t1"}).find("span", {"class", "num"}).string
  try:
    exp = html.find("div", {"class", "b_star"}).find("span", {"class", "num"}).string
    exp = f"{exp}%"
  except:
    exp = "none"
  runtime = html.find("dl", {"class", "info_txt1"}).find("dd").text
  tmp = runtime.find("분")
  runtime = runtime[tmp - 5 : tmp + 1].strip()
  infos = html.find_all("span", {"class", "link_txt"})
  for info in infos:
    tmp = str(info)
    if tmp.find("/bi/pi/") != -1:
      infos = info
      break
  director = infos.find("a").string
  
  if max_comment_page == 0:
    comment = ""
  else:
    comment = extract_review(link, max_comment_page)

  return {
        'rank': rank,
        '제목': title,
        '평점': star,
        '감독': director,
        '상영시간': runtime,
        '예매율': exp,
        'link': link,
        'comment': comment
    }


def start_scrapping():
  movies = []
  cnt = start
  print("scrapping start")
  for card in cards[start - 1 : end]:
    print(f"scrapping movie {cnt}")
    movies.append(extract_movie(card, cnt))
    cnt += 1
    print()
  print("scrapping finish")
  return movies




