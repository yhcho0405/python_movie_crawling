import requests
import csv
from bs4 import BeautifulSoup
from review import extract_review

URL = "https://movie.naver.com/movie/running/current.nhn"

result = requests.get(URL)
soup = BeautifulSoup(result.text, "html.parser")

cards = soup.find_all("dl", {"class": "lst_dsc"})

max_comment_page = 10 #max vallue is 10

def save(finals):
  file = open("final.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["제목", "평점", "감독", "상영시간", "예매율", "link", "comment"])
  for final in finals:
    writer.writerow(list(final.values()))
  return

def extract_movie(html):
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
  
  comment = extract_review(link, max_comment_page)

  return {
        '제목': title,
        '평점': star,
        '감독': director,
        '상영시간': runtime,
        '예매율': exp,
        'link': link,
        'comment': comment
    }

movies = []
cnt = 0
for card in cards:
  #if cnt >= 5:
    #break
  cnt += 1
  print(f"scrapping movie {cnt}")
  movies.append(extract_movie(card))
  print()
save(movies)
print()
print("scrapping finish")
