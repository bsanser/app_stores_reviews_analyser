import requests
from dataclasses import dataclass
from rich import print
import pandas as pd
import datetime

# APP_IDS = {
#   'ELVIE' : '1349263624',
#   'MEDELA' : '909275386',
#   'WILLOW_G0' : '1579004074',
#   'WILLOW_3' : '1489872855',
#   'TOMMEE_TIPPEE' : '1522124003',
#   'LANSINOH' : '1670282806',
#   'HUCKLEBERRY' : '1169136078',
#   'BABY_TRACKER': '779656557',
#   'DAIRY_BAR':'1439107604'
# }

APP_IDS = {
   'DAIRY_BAR':'1439107604'
}

COUNTRY_CODES = ['us']

reviews_list = []
app_info_list = []



@dataclass
class Review:
  date: str
  user_rating: int
  avg_rating: float
  title: str
  body: str
  vote_sum: int
  vote_count: int
  app_version: str

@dataclass
class AppInfo:
  avg_rating: float
  reviews_count: int
  latest_release_date: str
  latest_release_version: str
  latest_release_avg_user_rating: float
  latest_release_reviews_count: int
  description: str
  min_os_version: str
  languages_supported: list
 
 


def get_reviews(country_code,app_id, page_number):
  r = requests.get(f'https://itunes.apple.com/{country_code}/rss/customerreviews/page={page_number}/id={app_id}/sortby=mostrecent/json?urlDesc=/customerreviews/id={app_id}/sortby=mostrecent/json').json()
  try:
    reviews = r['feed']['entry']
    return reviews
  except:
    return

def get_app_info(app_id):
  r = requests.get(f'http://itunes.apple.com/lookup?id={app_id}').json() 
  app_info = r['results']
  return app_info


def parse_reviews_data(reviews_data, app_data):
  for review_item in reviews_data:
    review = Review (
      date= review_item['updated']['label'].split("T")[0],
      app_version = review_item['im:version']['label'],
      avg_rating = round(app_data[0].avg_rating,2),
      user_rating = int(review_item['im:rating']['label']),
      title = review_item['title']['label'],
      body =  review_item['content']['label'],
      vote_sum = int(review_item['im:voteSum']['label']),
      vote_count = int(review_item['im:voteCount']['label'])  
    )
    reviews_list.append(review)
  return(reviews_list)

def parse_app_data(data):
  for app in data:
    app_info = AppInfo (
      avg_rating =  app['averageUserRating'],
      reviews_count = app['userRatingCount'],
      latest_release_date = app['currentVersionReleaseDate'],
      latest_release_version = app['version'],
      latest_release_avg_user_rating = app['averageUserRatingForCurrentVersion'],
      latest_release_reviews_count =  app['userRatingCountForCurrentVersion'],
      min_os_version =  app['minimumOsVersion'], 
      description =  app['description'],
      languages_supported = app['languageCodesISO2A'], 

    )
    app_info_list.append(app_info)
  print(data)
  return(app_info_list)

def save_reviews(results, app_name, country_code):
  df = pd.DataFrame(results)
  df.to_excel(f'ios-{app_name}-{country_code}-reviews.xlsx', index = False)

def save_app_info(results, app_name):
  df = pd.DataFrame(results)
  df.to_excel(f'ios-{app_name}-info.xlsx', index = False)


  # (excel_writer, sheet_name='Sheet1', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, startrow=0, startcol=0, engine=None, merge_cells=True, inf_rep='inf', freeze_panes=None, storage_options=None, engine_kwargs=None)[source]



def main():
  for country_code in COUNTRY_CODES:
     for app_id in APP_IDS.values():
      app_name = list(APP_IDS.keys())[list(APP_IDS.values()).index(app_id)].lower()
      data_response = get_app_info(app_id)
      parsed_app_data = parse_app_data(data_response)
      save_app_info(parsed_app_data, app_name)
      # TODO: Fix pagination
      for x in range(1):
        reviews_response = get_reviews(country_code, app_id,x+1)
        parsed_reviews = parse_reviews_data(reviews_response, parsed_app_data)

      
      df = pd.DataFrame(parsed_reviews)
      # print(df['user_rating'].value_counts().sort_index())
      save_reviews(parsed_reviews,app_name, country_code)

        
      print(f'Added {len(parsed_reviews)} reviews')
 
   


main()