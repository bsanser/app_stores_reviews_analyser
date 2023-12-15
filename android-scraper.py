from google_play_scraper import app, Sort, reviews_all
import pandas as pd
import numpy as np
from rich import print


COUNTRY_CODE = 'us'

# APP_IDS = {
#   'ELVIE' : 'com.chiaro.elviepump',
#   'MEDELA' : 'com.medela.mymedela.live',
#   'WILLOW_G0' : 'com.willow.go',
#   'WILLOW_3' : 'com.willowpump.willow',
#   'TOMMEE_TIPPEE' : 'com.tommeetippee.smart',
#   'LANSINOH' : 'com.lansinoh.babyapp'
# }

APP_IDS = {
   'ELVIE' : 'com.chiaro.elviepump'
}


def save_reviews(results, app_name):
  df = pd.DataFrame(results)
  df.to_excel(f'android-{app_name}-{COUNTRY_CODE}-reviews.xlsx', index = False)

g_reviews = reviews_all(
        'com.willowpump.willow',
        sleep_milliseconds=0, # defaults to 0
        lang='en', # defaults to 'en'
        country=COUNTRY_CODE, # defaults to 'us'
        sort=Sort.NEWEST, # defaults to Sort.MOST_RELEVANT
    )

g_df = pd.DataFrame(np.array(g_reviews),columns=['review'])
g_df2 = g_df.join(pd.DataFrame(g_df.pop('review').tolist()))

g_df2.drop(columns={'userImage', 'reviewCreatedVersion'},inplace = True)
g_df2.rename(columns= {'score': 'rating','userName': 'user_name', 'reviewId': 'review_id', 'content': 'review_description', 'at': 'review_date', 'replyContent': 'developer_response', 'repliedAt': 'developer_response_date', 'thumbsUpCount': 'thumbs_up'},inplace = True)
g_df2.insert(loc=0, column='source', value='Google Play')
g_df2.insert(loc=3, column='review_title', value=None)
g_df2['laguage_code'] = 'en'
g_df2['country_code'] = 'us'
results = g_df2

save_reviews(results, 'willow_3.0')
