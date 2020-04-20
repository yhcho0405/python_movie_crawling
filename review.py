import requests
from bs4 import BeautifulSoup

def extract_page(linkp):
  result = requests.get(linkp)
  soup = BeautifulSoup(result.text, "html.parser")
  pagelist = []
  try:
    paging = soup.find("div", {"class": "paging"})
    pages = paging.find_all("span")
    for page in pages:
      pagelist.append(int(page.string))
  except:
    pagelist.append(0)
  max_page = pagelist[-1]
  return max_page



def extract_review(link, max_comment_page):
  original_link = link.replace("basic", "pointWriteFormList")
  max_page = extract_page(original_link)
  reviews = []
  max_page = min(max_page, max_comment_page)
  
  for page in range(1, max_page + 1):
    link = f"{original_link}&page={page}"
    print(f"scrapping comment page {page}/{max_page}")
    result = requests.get(link)
    soup = BeautifulSoup(result.text, "html.parser")

    reples = soup.find_all("div", {"class": "score_reple"})
    cnt = 0
    for reple in reples:
      try:
        try:
          tmp = reple.find("span", {"id": f"_filtered_ment_{cnt}"}).string.strip()
        except:
          tmp = reple.find("span", {"id": f"_filtered_ment_{cnt}"}).find("a")["data-src"]
      except:
        tmp = str(reple.find("span", {"id": f"_filtered_ment_{cnt}"}))
        tmp = tmp[40:-60].strip()
        print("ico_penel exception")
      reviews.append(tmp)
      cnt += 1
  return reviews
  

 

  