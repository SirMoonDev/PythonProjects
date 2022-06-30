## Pytrends application to get the x amount of trendy words.
## https://towardsdatascience.com/google-trends-api-for-python-a84bc25db88f


import pandas as pd
from pytrends.request import TrendReq


#Object that is used to query
pytrend = TrendReq()



# Interest by Region
pytrend.build_payload(kw_list=["Tesla"])
df = pytrend.interest_by_region()
df.head(20)

# Get Google top daily search data in the USA
df = pytrend.trending_searches(pn="united_states")
df.head(20)



# Get Google top daily search data world wide
df = pytrend.trending_searches()
df.head(20)


# Get Google's today’s trending topics
df = pytrend.today_searches(pn="US")


# Get Google's trending topics on a year
df = pytrend.top_charts(2019, hl='en-US', tz=300, geo='GLOBAL')
df.head()




# Get Google Keyword Suggestions As you Type
keywords = pytrend.suggestions(keyword='Tesla')
df = pd.DataFrame(keywords)
df.head(10)


# Related queries to the payload.
pytrend.build_payload(kw_list=['Coronavirus'])
related_queries = pytrend.related_queries()
related_queries.values()


# Related topics to the payload.
pytrend.build_payload(kw_list=['Coronavirus', 'Tesla'])
related_topic = pytrend.related_topics()
related_topic.values()




kw_list = ["Blockchain"]
pytrend.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')