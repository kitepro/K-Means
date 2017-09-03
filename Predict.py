import Cluster
import sqlite3

## MANUAL SETTINGS
group_count = 3
batch_size = 100

table_name = str(input("Table Name : "))
target_row = str(input("Target Class : "))
src_n = int(input("Number of Src Classes : "))
src_rows = []
print("Classes : ")
for i in range(src_n):
	src_rows.append(str(input()))
need_clustering = []
print("Classes that need clustering : ")
for i in src_rows:
	if int(input(str(i) + " : ")):
		need_clustering.append(str(i))
predict_tuple = {}
print("Predict Tuple : ")
for i in src_rows:
	if i in need_clustering:
		predict_tuple[i] = (float(input(str(i) + " : ")))
	else:
		predict_tuple[i] = (str(input(str(i) + " : ")))	

conn = sqlite3.connect('train.db')

## GET CLASS PROBABILITES
distinct_targets = []
res = conn.execute("SELECT COUNT(*) FROM " + table_name)
x = res.fetchall()[0]
total_rows = x[0]

res = conn.execute("SELECT DISTINCT(" + target_row + ") FROM " + table_name)
target_row_count = {}
for row in res:
	distinct_targets.append(row[0])
	target_row_count[row[0]] = conn.execute("SELECT COUNT(*) FROM " + table_name + " WHERE " + target_row + " = '" + row[0] + "'").fetchall()[0][0]

## CLUSTERING
clusters = {}
for i in need_clustering:
	class_count = {}
	for j in distinct_targets:
		class_count[j] = {}
	res = conn.execute("SELECT " + i + " , " + target_row + " FROM " + table_name + " LIMIT " + str(batch_size) + " OFFSET 0").fetchall()
	group_means, assigned_groups = Cluster.KNN([0] * group_count, [z[0] for z in res])
	for j in res:
		if(assigned_groups[j[0]] in class_count[j[1]]):
			class_count[j[1]][assigned_groups[j[0]]] += 1
		else:
			class_count[j[1]][assigned_groups[j[0]]] = 1
	offset = batch_size
	while len(res) == batch_size:
		res = conn.execute("SELECT " + i + " , " + target_row + " FROM " + table_name + " LIMIT " + str(batch_size) + " OFFSET " + offset).fetchall()
		offset += batch_size
		group_means, group_members = Cluster.KNN(group_means, [z[0] for z in res])
		for j in res:
			if(assigned_groups[j[0]] in class_count[j[1]]):
				class_count[j[1]][assigned_groups[j[0]]] += 1
			else:
				class_count[j[1]][assigned_groups[j[0]]] = 1
	clusters[i] = [group_means,class_count]
	
## NON CLUSTERED GROUPS
non_clusters = {}
for i in (set(src_rows)-set(need_clustering)):
	res = conn.execute("SELECT " + i + "," + target_row + " FROM " + table_name + " LIMIT " + str(batch_size) + " OFFSET 0").fetchall()
	class_count = {}
	for j in distinct_targets:
		class_count[j] = {}
	for j in res:
		if(j[0] in class_count[j[1]]):
			class_count[j[1]][j[0]] += 1
		else:
			class_count[j[1]][j[0]] = 1
	offset = batch_size
	while(len(res) == batch_size):
		res = conn.execute("SELECT " + i + "," + target_row + " FROM " + table_name + " LIMIT " + str(batch_size) + " OFFSET " + offset).fetchall()	
		for j in res:
			if(j[0] in class_count[j[1]]):
				class_count[j[1]][j[0]] += 1
			else:
				class_count[j[1]][j[0]] = 1
		offset += batch_size
	non_clusters[i] = class_count		

## CHECK PREDICT TUPLE GROUPS
my_groups = {}
for i in src_rows:
	if i in clusters:
		my_grp = 0
		for j in range(group_count):
			if abs(clusters[i][0][my_grp] - predict_tuple[i]) > abs(clusters[i][0][j] - predict_tuple[i]):
				my_grp = j
		my_groups[i] = my_grp
	else:
		my_groups[i] = predict_tuple[i]

final = {}
for i in distinct_targets:
	final[i] = 1
for i in src_rows:
	if i in clusters:
		for j in distinct_targets:
			if my_groups[i] in clusters[i][1][j]:
				final[j] *= clusters[i][1][j][my_groups[i]]
			else:
				final[j] *= 0
	else:
		for j in distinct_targets:
			if my_groups[i] in non_clusters[i][j]:
				final[j] *= non_clusters[i][j][my_groups[i]]
			else:
				final[j] *= 0	
s = 0
for i in final:
	final[i] = ((final[i]/(target_row_count[i] ** (len(src_rows)-1)))/total_rows)
	s += final[i]
for i in final:
	print(i,":",final[i]*100/s,"%")
conn.close()

