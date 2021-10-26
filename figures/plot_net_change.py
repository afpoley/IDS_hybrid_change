import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# Load file
fp = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\FINAL_1980_1995\\hybrid_1985_1995_filter.shp'
# output = 'D:\\Users\\afpoley\\Desktop\\IDS_TEMP\\FINAL_1980_1990\\hybrid_final_1980_1990_summary.csv'
year1 = '1980'
year2 = '1990'

data = gpd.read_file(fp)
data['area_ha'] = data['geometry'].area*1e-4    #Convert to ha


def reclass(data, gridcode, summarize_class, gridcodeNum, changeNames):
    data[gridcode] = data[gridcode].replace(gridcodeNum, changeNames)
    change = data.groupby(gridcode)[summarize_class].sum().reset_index()
    return change


def split_year(change, area):
    #change.gridcode = change['change'].astype(str)
    change[[year1, year2]] = change['gridcode'].str.split(" - ", expand=True)
    sumy1 = change.groupby([year1])[area].sum().reset_index()
    sumy1 = sumy1.rename(columns={year1: "class", area: year1 + '-loss'})
    sumy2 = change.groupby([year2])[area].sum().reset_index()
    sumy2 = sumy2.rename(columns={year2: "class", area: year2 + '-gain'})
    return sumy1, sumy2


classNumber = [1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012,
               2001, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
               3001, 3002, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 3011, 3012,
               4001, 4002, 4003, 4005, 4006, 4007, 4008, 4009, 4010, 4011, 4012,
               5001, 5002, 5003, 5004, 5006, 5007, 5008, 5009, 5010, 5011, 5012,
               6001, 6002, 6003, 6004, 6005, 6007, 6008, 6009, 6010, 6011, 6012,
               7001, 7002, 7003, 7004, 7005, 7006, 7008, 7009, 7010, 7011, 7012,
               8001, 8002, 8003, 8004, 8005, 8006, 8007, 8009, 8010, 8011, 8012,
               9001, 9002, 9003, 9004, 9005, 9006, 9007, 9008, 9010, 9011, 9012,
               10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009, 10011, 10012,
               11001, 11002, 11003, 11004, 11005, 11006, 11007, 11008, 11009, 11010, 11012,
               12001, 12002, 12003, 12004, 12005, 12006, 12007, 12008, 12009, 12010, 12011]

className = ['urban - suburban', 'urban - barren', 'urban - agriculture', 'urban - grasslands', 'urban - deciduous',
             'urban - evergreen', 'urban - shrubs', 'urban - woody wetlands', 'urban - wetlands',
             'urban - floating aquatic', 'urban - water',

             'suburban - urban', 'suburban - barren', 'suburban - agriculture', 'suburban - grasslands',
             'suburban - deciduous', 'suburban - evergreen', 'suburban - shrubs', 'suburban - woody wetlands',
             'suburban - wetlands', 'suburban - floating aquatic', 'suburban - water',

             'barren - urban', 'barren - suburban', 'barren - agriculture', 'barren - grasslands',
             'barren - deciduous', 'barren - evergreen', 'barren - shrubs', 'barren - woody wetlands',
             'barren - wetlands', 'barren - floating aquatic', 'barren - water',

             'agriculture - urban', 'agriculture - suburban', 'agriculture - barren', 'agriculture - grasslands',
             'agriculture - deciduous', 'agriculture - evergreen', 'agriculture - shrubs',
             'agriculture - woody wetlands', 'agriculture - wetlands', 'agriculture - floating aquatic',
             'agriculture - water',

             'grasslands - urban', 'grasslands - suburban', 'grasslands - barren', 'grasslands - agriculture',
             'grasslands - deciduous', 'grasslands - evergreen', 'grasslands - shrubs', 'grasslands - woody wetlands',
             'grasslands - wetlands', 'grasslands - floating aquatic', 'grasslands - water',

             'deciduous - urban', 'deciduous - suburban', 'deciduous - barren', 'deciduous - agriculture',
             'deciduous - grasslands', 'deciduous - evergreen', 'deciduous - shrubs',
             'deciduous - woody wetlands', 'deciduous - wetlands', 'deciduous - floating aquatic',
             'deciduous - water',

             'evergreen - urban', 'evergreen - suburban', 'evergreen - barren', 'evergreen - agriculture',
             'evergreen - grasslands', 'evergreen - deciduous', 'evergreen - shrubs',
             'evergreen - woody wetlands', 'evergreen - wetlands', 'evergreen - floating aquatic',
             'evergreen - water',

             'shrubs - urban', 'shrubs - suburban', 'shrubs - barren', 'shrubs - agriculture',
             'shrubs - grasslands', 'shrubs - deciduous', 'shrubs - evergreen',
             'shrubs - woody wetlands', 'shrubs - wetlands', 'shrubs - floating aquatic',
             'shrubs - water',

             'woody wetlands - urban', 'woody wetlands - suburban', 'woody wetlands - barren',
             'woody wetlands - agriculture', 'woody wetlands - grasslands', 'woody wetlands - deciduous',
             'woody wetlands - evergreen', 'woody wetlands - shrubs', 'woody wetlands - wetlands',
             'woody wetlands - floating aquatic', 'woody wetlands - water',

             'wetlands - urban', 'wetlands - suburban', 'wetlands - barren',
             'wetlands - agriculture', 'wetlands - grasslands', 'wetlands - deciduous', 'wetlands - evergreen',
             'wetlands - shrubs', 'wetlands - woody wetlands', 'wetlands - floating aquatic', 'wetlands - water',

             'floating aquatic - urban', 'floating aquatic - suburban', 'floating aquatic - barren',
             'floating aquatic - agriculture', 'floating aquatic - grasslands', 'floating aquatic - deciduous',
             'floating aquatic - evergreen', 'floating aquatic - shrubs', 'floating aquatic - woody wetlands',
             'floating aquatic - wetlands', 'floating aquatic - water',

             'water - urban', 'water - suburban', 'water - barren',
             'water - agriculture', 'water - grasslands', 'water - deciduous',
             'water - evergreen', 'water - shrubs', 'water - woody wetlands',
             'water - wetlands', 'water - floating aquatic']

gridcode = 'gridcode'
summarize_class = 'area_ha'

data2 = reclass(data, gridcode, summarize_class, classNumber, className)
sum1980, sum1990 = split_year(data2, summarize_class)

data3 = pd.merge(sum1980, sum1990, on='class')
data3['net'] = data3[year2 + '-gain']-data3[year1 + '-loss']

#%%
num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

ax2 = data3['net'].plot.bar()
plt.xticks(ticks=num, labels=data3['class'], rotation=45, ha='right')
plt.ylabel('ha')
ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.title('Net land cover change c.' + year1 + ' - c.' + year2)
plt.axhline(y=0, color='black', linewidth=1)
plt.gcf().subplots_adjust(bottom=.3, left=.2, top=.9)
plt.show()
