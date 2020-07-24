import pandas as pd, numpy as np, operator
import matplotlib.pyplot as plt
from textwrap import wrap
data = pd.read_csv("googleplaystore.csv")

#### Data Cleaning
data = data[data.Rating <= 5]					#Removing any rows with rating>5
data['Price']=data['Price'].apply(lambda x: str(x).replace('$','')if '$' in str(x) else str(x))		#Removing $ sign
data['Price']=data['Price'].apply(lambda x: float(x))			#Conversion to float
data['Reviews']=data['Reviews'].apply(lambda x: int(x))			#Conversion to integer
data['Current_Ver'].fillna(str(data['Current_Ver'].mode().values[0]), inplace=True)			#Removing NULL values
data['Android_Ver'].fillna(str(data['Android_Ver'].mode().values[0]), inplace=True)			#Removing NULL values
data['Installs'] = data['Installs'].apply(lambda x: str(x).replace('+', '') if '+' in str(x) else str(x))
data['Installs'] = data['Installs'].apply(lambda x: str(x).replace(',', '') if ',' in str(x) else str(x))
data['Installs'] = data['Installs'].apply(lambda x: int(x))		#Conversion to integer

categories = list(data.Category.unique())		#Getting Categories
category_wise_free = list()
category_wise_paid = list()
for category in categories:
	new_df = data[data.Category == category]
	free_count=0
	paid_count=0
	for ind in new_df.index:
		if new_df["Type"][ind]=="Free":
			free_count+=1
		else:
			paid_count+=1
	category_wise_free.append(free_count)
	category_wise_paid.append(paid_count)

def autolabel(rects):
	for rect in rects:
		height = rect.get_height()
		ax.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

x = np.arange(len(categories[:8]))
width = 0.35
fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, category_wise_free[:8], width, label='Free')
rects2 = ax.bar(x + width/2, category_wise_paid[:8], width, label='Paid')
ax.set_ylabel('Number of Apps')
ax.set_title('Category-wise Free and Paid Apps')
ax.set_xticks(x)
ax.set_xticklabels(categories[:8])
ax.legend()
autolabel(rects1)
autolabel(rects2)
plt.show()

#### Apps based on Android Version
android_dict = dict()
for ind in data.index:
	try:
		android_dict[data["Android_Ver"][ind]] += 1
	except:
		android_dict[data["Android_Ver"][ind]] = 1
sorted_d = dict(sorted(android_dict.items(), key=operator.itemgetter(1),reverse=True))
android_names = list(sorted_d.keys())
apps_based_on_versions = list(sorted_d.values())
plt.plot(android_names[:15],apps_based_on_versions[:15])
plt.title("Applications based on Android Version")
plt.xticks(rotation=45)
plt.show()

#### Most Popular Apps
installs_df = data[["App","Installs"]]
top_10_installs = installs_df.nlargest(10,"Installs",keep="all")
app_name=list()
installs=list()
for ind in top_10_installs.index:
	app_name.append(top_10_installs["App"][ind])
	installs.append(top_10_installs["Installs"][ind])
app_name = [ '\n'.join(wrap(l, 20)) for l in app_name ]
plt.bar(app_name,installs)
plt.ticklabel_format(axis='y', style='plain')
plt.title("Most Popular Apps")
plt.xticks(rotation=90)
plt.show()

#### For Deveopers
application = input("Enter App Name: ")
for ind in data.index:
	if data["App"][ind].lower() == application.lower():
		print("\nDetails:-\nApp Name  :", data["App"][ind])
		print("Rating    : ", data["Rating"][ind], "out of 5")
		print("Feedback  : ",end="")
		if data["Rating"][ind] < 2:
			print("Needs improvement. We recommend you to read reviews to improve the app.")
		elif data["Rating"][ind] < 3:
			print("This app is rated average. There is scope for improvement.")
		elif data["Rating"][ind] < 4:
			print("This app is rated above average! You may read reviews for further enhancements.")
		else:
			print("Good job developers! This app is rated very good. You may go through reviews for future updates.")
		break
else:
	print("\nApp not found... Please try again...")