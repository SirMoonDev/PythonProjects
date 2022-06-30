## Pytrends application to get the x amount of trendy words.
## https://towardsdatascience.com/google-trends-api-for-python-a84bc25db88f



import pandas as pd
from pytrends.request import TrendReq

class PytrendController: 

    def __init__(self):
        self.pytrend = TrendReq()

    def GetRelatedTopicsFor(self, ikw_list, itimeframe='today 5-y', igeo='', igprop=''):
        
        self.pytrend.build_payload(kw_list=ikw_list, cat=0, timeframe=itimeframe, geo=igeo, gprop=igprop)
        related_topic = self.pytrend.related_queries()
        return related_topic.values()

    def GetRelatedQueriesFor(self, ikw_list, itimeframe='today 5-y', igeo='', igprop=''):

        self.pytrend.build_payload(kw_list=ikw_list, cat=0, timeframe=itimeframe, geo=igeo, gprop=igprop)
        related_topic = self.pytrend.related_topics()
        return related_topic.values()

    def GetTrendingSearches(self,location):
        pl = self.pytrend.trending_searches(pn=location)
        return pl.head(20)

        

    def GetRootTopAndRising_RelatedToTopic_FromSingleTopic(self, singleTopic, iterateAmount):
    
        globalRelTop = self.GetRelatedTopicsFor(ikw_list=[singleTopic])
        globalRelTopicDict = [ x for x in globalRelTop][0]

        toConcatTopicRisingSearched = []
        toConcatTopicTopSearched = []

        topicTopFrame = None
        topicTopRisingFrame = None

        try:
            globalRelTopicDict['top']['parent'] = singleTopic
            toConcatTopicTop = [globalRelTopicDict['top']]
            

            for loop in range(iterateAmount):
                
                for topTopic in list(toConcatTopicTop[loop]['query']):
                    globalRelTopSubset = self.GetRelatedTopicsFor(ikw_list=[topTopic])
                    globalRelTopSubsetDict = [ x for x in globalRelTopSubset][0]
                    globalRelTopSubsetDict['top']['parent'] = topTopic

                    if topTopic not in toConcatTopicTopSearched:
                        toConcatTopicTop.append(globalRelTopSubsetDict['top'])
                        toConcatTopicTopSearched.append(topTopic)

            topicTopFrame = pd.concat(toConcatTopicTop)
        except:
            print("Didn't have top elements for " + singleTopic)


        try:
            globalRelTopicDict['rising']['parent'] = singleTopic
            toConcatTopicRising = [globalRelTopicDict['rising']]
            
            
            for loop in range(iterateAmount):
                for topTopic in list(toConcatTopicRising[loop]['query']):
                    globalRelTopSubset = self.GetRelatedTopicsFor(ikw_list=[topTopic])
                    globalRelTopSubsetDict = [ x for x in globalRelTop][0]

                    if topTopic not in toConcatTopicRisingSearched:
                        globalRelTopSubsetDict['rising']['parent'] = topTopic
                        toConcatTopicRising.append(globalRelTopSubsetDict['rising'])
                        toConcatTopicRisingSearched.append(topTopic)
            topicTopRisingFrame = pd.concat(toConcatTopicRising)
        except:
            print("Didn't have rising elements for " + singleTopic)

        
        


        return [topicTopFrame, topicTopRisingFrame]


    def ExportTrendyTopicItems_AndSimilars(self, filename, similaritySearchLoop):
        maxTrendsReturned = pc.GetTrendingSearches("united_states")


        maxTrendsReturned.rename(columns={maxTrendsReturned.columns.values[0]: 'Trending Topics'},inplace=True)

    

        with pd.ExcelWriter(filename) as writer:
            toConcatTopicTop= []
            toConcatTopicRising = []
            
            maxTrendsReturned.to_excel(writer, sheet_name='Top Trending Today')

            for trendyTopic in list(maxTrendsReturned['Trending Topics']):
                print("Word:"+ str(trendyTopic))
                searchItems =  pc.GetRootTopAndRising_RelatedToTopic_FromSingleTopic(trendyTopic, similaritySearchLoop)

                if type(searchItems[0]) != None:
                    toConcatTopicTop.append(searchItems[0])  

                if type(searchItems[1]) !=  None:
                    toConcatTopicRising.append(searchItems[1])

            if len(toConcatTopicRising) > 0:
                topicTopFrame = pd.concat(toConcatTopicTop)
                topicTopFrame.to_excel(writer, sheet_name='Related - Top')

            if len(toConcatTopicRising) > 0:
                topicTopRisingFrame = pd.concat(toConcatTopicRising)
                topicTopRisingFrame.to_excel(writer, sheet_name='Related - Rising')

    # def GetRootTopAndRisingFromRelated(self, iterateAmount):
    
    #     self.globalRelTop = self.GetTrendingSearches("united_states")
    #     self.globalRelTopicDict = [ x for x in self.globalRelTop][0]
    #     return self.RunGetRootTopAndRising(iterateAmount)
        
        


if __name__=='__main__':

    import pandas as pd
    from pytrends.request import TrendReq


    filename = 'output.xlsx'
    similaritySearchLoop = 0



    pc = PytrendController()
    pc.ExportTrendyTopicItems_AndSimilars(filename, similaritySearchLoop)
    

    #GetRelatedTopicsFor(ikw_list=kw_list, icat=0, itimeframe='today 5-y', igeo='US', igprop='')
    #GetRelatedTopicsFor(ikw_list=kw_list, icat=0, itimeframe='today 5-y', igeo='US', igprop='news')
    #GetRelatedTopicsFor(ikw_list=kw_list, icat=0, itimeframe='today 5-y', igeo='US', igprop='froogle ')

