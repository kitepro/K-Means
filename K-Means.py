# Number of groups to be created
num_groups = 3

# Initialize group centers
groups = [0] * num_groups

# Initialize group counts
grp_count = [0] * num_groups

# Trainer set
trainer = [1,2,3,4,5,6,7,8,9,10]

# Temporary variable to perform mid-way transfers.
# Eg : A member may have found to be closer to some other group's center after its allocation to a different group.
#      So to carve the distribution we have to re-calculate the center of both previous and new group after transfer.
temp = [0] * len(trainer)

# Initial setup
# Put everythin in 1st group itself then later carve it.
groups[0] = sum(trainer)/len(trainer)
grp_count[0] = len(trainer)

# Keep carving till we are stable.
change = True
while change:
    change = False
    for i in range(len(trainer)):
        closest = 0
        for j in range(1,num_groups):
            if abs(trainer[i]-groups[closest]) > abs(trainer[i]-groups[j]):
                closest = j
        if closest != temp[i] and grp_count[temp[i]] > 1:
            groups[temp[i]] = ((groups[temp[i]]*grp_count[temp[i]])-trainer[i])/(grp_count[temp[i]]-1)
            grp_count[temp[i]] -= 1
            groups[closest] = ((groups[closest]*grp_count[closest])+trainer[i])/(grp_count[closest]+1)
            grp_count[closest] += 1
            temp[i] = closest
            change = True

print("Group Centers : ",groups)
print("Group Counts : ",grp_count)
print("Trainer Groups : ",temp)



