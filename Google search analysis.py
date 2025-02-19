!pip install pytrends

!pip install --upgrade pip

!pip install matplotlib

!pip install pandas

!pip install numpy

from pytrends.request import TrendReq

import matplotlib.pyplot as plt

# Only need to run this once, the rest of request will use the next session.
PyTrend = TrendReq()

#Create payload and Capture API tokens. Only needed for interest over time()
PyTrend.build_payload(kw_list=["Machine Learning"])

#Interest over time
interest_over_time_df=PyTrend.interest_over_time()

print(interest_over_time_df.head())

print(interest_over_time_df.tail())


fig,ax=plt.subplots(figsize=(10,6))
interest_over_time_df['Machine Learning'].plot()
plt.title('Total Google Searches for Machine Learning',fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Total Count')
plt.show()


!pip install backoff


from pytrends.request import TrendReq
import time
import backoff
from pytrends import exceptions # Import the exceptions module from pytrends


# Initialize pytrends
PyTrend = TrendReq(hl='en-US', tz=360)  # hl: language, tz: timezone

# Set the keyword(s)
keywords = ['your keyword']  # Replace with your actual keyword(s)


@backoff.on_exception(backoff.expo, exceptions.TooManyRequestsError, max_tries=10, factor=2) # Use pytrends.exceptions
def get_trends_data():
    PyTrend.build_payload(kw_list=keywords, timeframe='today 5-y', geo='', gprop='') #build the payload
    return PyTrend.interest_by_region()

# Get interest by region with backoff and retry logic
interest_by_region_df = get_trends_data()

print(interest_by_region_df)



interest_by_region_df=interest_by_region_df.sort_values(by='Machine Learning',ascending=False)


print(interest_by_region_df.head(10))


top_5_countries = interest_by_region_df.nlargest(10, 'Machine Learning')
top_5_countries = top_5_countries.reset_index()  # Reset index for plotting
top_5_countries.plot.bar(x='geoName', y='Machine Learning', figsize=(10, 6))
plt.show()


related_queries_dict=PyTrend.related_queries()
print(related_queries_dict)


from pytrends.request import TrendReq

PyTrend = TrendReq(hl='en-US', tz=360)
keywords = ['Machine Learning']  # Example keyword
PyTrend.build_payload(kw_list=keywords, timeframe='today 5-y', geo='', gprop='')

try:
    related_queries_dict = PyTrend.related_queries()
    print(related_queries_dict)
except IndexError:
    print(f"No related queries found for {keywords}")
    related_queries_dict = {}

# Accessing the "top" and "rising" related queries (if available):
if related_queries_dict: # Check if the dictionary is not empty
    top_queries = related_queries_dict.get(keywords[0], {}).get('top', {}) # Safe access with .get
    rising_queries = related_queries_dict.get(keywords[0], {}).get('rising', {}) # Safe access with .get

    print("Top Queries:", top_queries)
    print("Rising Queries:", rising_queries)


trending_searches_df=PyTrend.trending_searches()

print(trending_searches_df.head(10))


from pytrends.request import TrendReq
import time
import backoff
from pytrends import exceptions  # Import the exceptions module from pytrends

PyTrend = TrendReq(hl='en-US', tz=360)

@backoff.on_exception(backoff.expo, (exceptions.TooManyRequestsError, exceptions.ResponseError), max_tries=10, factor=2)
def get_trending_searches():
    try:
        return PyTrend.trending_searches(pn='united_states') # Specify country using 'pn' argument
    except exceptions.ResponseError as e:
        if e.response.status_code == 404:
            print("Trending searches endpoint might have changed. Check pytrends documentation.")
        raise

# Call the function to get trending searches
trending_searches_df = get_trending_searches()

print(trending_searches_df.head(10))

today_searches_df=PyTrend.today_searches()
print(today_searches_df)



top_charts_df=PyTrend.top_charts(date=2023, hl='en-US', tz=300, geo='GLOBAL')
print(top_charts_df.head())















